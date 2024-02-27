from variables import variables
from flask_smorest import abort , Blueprint
from flask.views import MethodView

from models import ItemModel , StoreModel , TagsModel , TagItem
from sqlalchemy.exc import SQLAlchemyError , IntegrityError
from schema import Tagvalidate , TagItemvalidate


blp = Blueprint("Tags", __name__ , description = "Operation on Tags")

@blp.route("/store/<int:store_id>/tag")
class Tags(MethodView):
    
    @blp.response(200,Tagvalidate(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.response(201,Tagvalidate)
    @blp.arguments(Tagvalidate)
    def post(self,tag_data , store_id):
        # You can also do this
        if TagsModel.query.filter(TagsModel.store_id == "store_id" , TagsModel.name == tag_data["name"]).first():
            abort(400 , message = "A ta with that name aleready exists")
        tag = TagsModel(**tag_data , store_id = store_id)
        try:
            variables.session.add(tag)
            variables.session.commit()
        except SQLAlchemyError:
            abort(400 , message="Something went wrong while creating the tag")
        
        return tag


    

@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagToItem(MethodView):

    @blp.response(201, Tagvalidate)
    def post(self, item_id , tag_id):            
        item = ItemModel.query.get_or_404(item_id)
        tag = TagsModel.query.get_or_404(tag_id)

        item.tags.append(tag)# I am linking the item to tag , because of relationship the tag.item will also be updated (is what i think)

        try:
            variables.session.add(item)
            variables.session.commit()
        except SQLAlchemyError:
            abort(500 , message="Someting went wrong in linking the tag to item section")

        return tag

    @blp.response(200, TagItemvalidate)
    def delete(self , item_id , tag_id):# Unlinking the item and tag realtionship
        item = ItemModel.query.get_or_404(item_id)
        tag = TagsModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            variables.session.add(item)
            variables.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while deleting the relation of tag and item")
        
        return{"message" : "item and tag relation successfully seperated"}



@blp.route("/tag/<int:tag_id>")
class Tags2(MethodView):
    @blp.response(200, Tagvalidate)
    def get(self,tag_id):
        tag = TagsModel.query.get_or_404(tag_id)
        return tag
    
    @blp.response(200 , TagItemvalidate)
    def delete(self , tag_id):
        tag = TagsModel.query.get_or_404(tag_id)
        
        if not tag.items:
            variables.session.delete(tag)
            variables.session.commit()
            return {"message" : "Tag successfully deleted"}
        abort(400 , message="Could not delete tag as it had items attached to it")

@blp.route("/tag")
class Tags3(MethodView):
    @blp.response(200,Tagvalidate(many=True))  #It iterates through all of the tags and return each object , so many = True is a must   
    def get(self):  
        tags = TagsModel.query.all()

        return tags
