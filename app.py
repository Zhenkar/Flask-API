from flask import Flask , jsonify
from flask_smorest import Api
import os
from flask_jwt_extended import JWTManager
from blocklist import Blocklist
#Hello Git Hub

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

import models
from models import BlockModel
from variables import variables


def create_app(db_url=None):
    app = Flask(__name__)

    #these configurations over-ride the default config when a new app is created
    app.config["PROPOGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] ="/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")         # the sqlite:///data.db will create a file called data.db , and our data will be stored there
    app.config["SQLALCHEMY_TRACK_NOTIFICATION"] = False                                                     # increases the spped of sqlalchemy
    variables.init_app(app)                                                                                 # creates a connection between the sqlalchemy object and the app , so that sqlalchemy can make connection between sqlite and app.


    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "338541722931426044653050095336200886611"                                 # secret key is used for signing the jwt[using the secret key] , when a attacker creates his own jwt and sends it to the server , the server checks the jwt with it's own secret key. Since the attacker didn't know the key the server rejects the request, therefore making the application safe.
    jwt = JWTManager(app)     

    @jwt.token_in_blocklist_loader
    def block(jwt_header , jwt_payload):
        if BlockModel.query.filter(BlockModel.block == jwt_payload["jti"]).first():
            return True
        else:
            return False
        #return jwt_payload["jti"] in Blocklist  #if true then the below decorator will run
    
    @jwt.revoked_token_loader
    def revoked(jwt_header , jwt_payload):
        return(
            jsonify(
                {"message" : "The token has been expired"}
            ),401
        )

    @jwt.expired_token_loader
    def expired(jwt_header , jwt_payload):
        return (
            jsonify ({"message":"The token has expired"}),401,
        )  

    @jwt.invalid_token_loader
    def invalid(error):
        return(
            jsonify(
                {"message":"Verification failed", "error" :"invalid token"}
            ),401,
        )
    
    @jwt.unauthorized_loader
    def unauthorized(error):
        return(
            jsonify(
                {"description":"Request does not contain access token",
                 "error":"authorization_required"}
            ),401
        )


    with app.app_context():
        variables.create_all()  #if the tables does not exitst , this'll run or else it'll not run
                                #sqlalchemy know what models to create because we have imported ItemModel and Storemodel

    #you can do api.route also
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app