from flask_smorest import Blueprint , abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token ,create_refresh_token , get_jwt_identity , jwt_required , get_jwt
from sqlalchemy.exc import SQLAlchemyError , IntegrityError 
from passlib.hash import pbkdf2_sha256

from variables import variables
from schema import Uservalidate
from models import UserModel , BlockModel



blp = Blueprint("User" , "users" , description="Operations on Users")

@blp.route("/register")
class User (MethodView):
    @blp.arguments(Uservalidate)
    #@blp.response(201,Uservalidate)
    def post(self, user_data):
        user = UserModel(
            name = user_data["name"],
            password = pbkdf2_sha256.hash(user_data["password"])
        )

        if UserModel.query.filter(UserModel.name == user.name).first():
            abort (409, message = "An user with this name already exists")
        try:
            variables.session.add(user)
            variables.session.commit()
        except SQLAlchemyError:
            abort(400 , message = "An error occured when inserting the user")
        
        return {"message":"User created successfully"},201
        #return user
    #when you are adding @response you hav to add return user
    #when you are adding {message} you don't have to add @response

    @blp.response(200,Uservalidate(many=True))
    def get(self):
        user = UserModel.query.all()
        return user


@blp.route("/register/<int:user_id>")
class UserDel(MethodView):
    @jwt_required()
    def delete(self , user_id):
        user = UserModel.query.get_or_404(user_id)#remember that query takes only the primary key to check in the database
        variables.session.delete(user)
        variables.session.commit()
        return {"message":"user deleted successfully"},200
    
    
    @blp.response(200,Uservalidate)
    def get(self, user_id):
            user = UserModel.query.get_or_404(user_id)#remember that query takes only the primary key to check in the database
            return user
    

        
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(Uservalidate)
    def post(self, user_data):
        # user = UserModel.query.get(user_data) you cannot do this cause there will be no primary key mentioned in the request or in request body
        # that is why you are using UserModel.name to verify the name
        user = UserModel.query.filter(
            UserModel.name == user_data["name"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"] , user.password):
            access_token = create_access_token(identity = user.id , fresh=True)
            refresh_token = create_refresh_token(identity= user.id)
            return {"access token":access_token , "refresh token": refresh_token}
        
        abort(400 , message="Invalid password or user")


        
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jwi = get_jwt()["jti"]

        block = BlockModel()
        block.block = jwi
        variables.session.add(block)
        variables.session.commit()

        #Blocklist.add(jwi)
        return({"message":"Logged out successfully"})
    
@blp.route("/refresh")
class Refresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user , fresh = False)
        return {"access token" : new_token}
