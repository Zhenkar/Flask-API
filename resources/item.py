from flask_smorest import Blueprint , abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required

#for marshmallow validation of the data incoming and outgoing
from schema import Itemsvalidate , ItemsUpdate

#for sql alchemy - database object and sqlalchemy error
from variables import variables
from sqlalchemy.exc import SQLAlchemyError , IntegrityError
from models import ItemModel



blp = Blueprint("Items" , __name__ , description = "Operations on Item")


@blp.route("/items/<int:item_id>") #string , int etc
class Item(MethodView):

    @jwt_required()
    @blp.response(200 , Itemsvalidate)                                                      # this line @blp.response uses scheme that we defined and show the values that are defined in the scheme , you define with status code what message you want
    def get(self, item_id):                                                                                                                              
        item = ItemModel.query.get_or_404(item_id)                                          # ItemModel.query function is flask-sqlalchemy exclusive only, you won't get it in normal sqlalchemy 
                                                                                            # query takes only the ""primary key""" value form the request and search the database , if not found it'll return 404 error
        return item

    @jwt_required(fresh=True)
    def delete(self, item_id):                                                              
        item = ItemModel.query.get_or_404(item_id)
        variables.session.delete(item)
        variables.session.commit()
        return {"message":"Item deleted successfully"}


    @jwt_required()
    #order of argument and response matters
    @blp.arguments(ItemsUpdate)                 
    @blp.response(200 , Itemsvalidate)
    def put(self, request_data , item_id):                                                  # update_item , the request_data shoule be first because its the rule for arguments keyword                              
        item = ItemModel.query.get(item_id) 
        if item:
            item.name = request_data["name"]
            item.price = request_data["price"]
        else:
            item = ItemModel(id = item_id ,**request_data)
        variables.session.add(item)
        variables.session.commit()
        return item
        
        




@blp.route("/items")
class Items_new(MethodView):


    #the above schemas were for single item, but for multiple items 
    @blp.response(200 , Itemsvalidate(many = True))
    def get(self):
        return ItemModel.query.all()
    
    @jwt_required(fresh=True)
    @blp.doc(description = "Testing doc")
    @blp.arguments(Itemsvalidate)                                                           # this line is making sure that the json text contains all the necessary fields mentioned in the schema , and returns a dcitonary (in our case request_data) no need for request_dat = reqest.get_json()
    @blp.response(201,Itemsvalidate)
    def post(self, request_data):                                              
        item = ItemModel(**request_data)                                                    #Object/Instance of ItemModel class, **request_data says that the dictionary value which I will receive will be seperated as variable & value respectively with the table columns defined in the item table 

        try:
            variables.session.add(item)
            variables.session.commit()
        
        except IntegrityError:
            abort (400, message="A Item with the same name already exists")

        except SQLAlchemyError:
            abort ( 500 , message = " Someting went wrong while inserting the data ")

        return item
    


