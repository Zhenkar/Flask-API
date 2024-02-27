from variables import variables

# to make it one to many relationship( between store and item ), the store dosen't have a item_id column, if it had then you'd have to insert a store to a particular item id.
# you could have made it many to many relationship if you have item_id as a foregin key and making unique to false. By making this you could make multiple stores with the same item_id and they'd fall in that item
class StoreModel(variables.Model):
    __tablename__= "stores"

    id = variables.Column(variables.Integer, primary_key = True)
    name = variables.Column(variables.String(80) ,unique=True,  nullable = False)

    items = variables.relationship("ItemModel" , back_populates="store" , lazy="dynamic", cascade="all, delete")    #cascade all is used to delete the items within store when we delete the store.
    tags = variables.relationship("TagsModel" , back_populates = "store" , lazy="dynamic")




    # now we have a item attribute[column] in the StoreModel class , the string "stores"  [ item  = variable.relationship(back_populate = stores)] 
    # refers that to the attribute stores in the class ItemModel