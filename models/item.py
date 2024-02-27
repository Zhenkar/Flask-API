# Models folder came into picture after the marshmello(schema) , for sqlalchemy

from variables import variables

class ItemModel(variables.Model):
    __tablename__= "items"


    id = variables.Column(variables.Integer , primary_key = True)
    name = variables.Column(variables.String(50) , unique = True ,nullable = False)
    price = variables.Column(variables.Float(precision=2) , unique = False , nullable = False)

    store_id = variables.Column(variables.Integer ,variables.ForeignKey("stores.id")  , unique= False , nullable = False)  # Foregin key - tablename . column name (id)

    # explination in the paper.
    store = variables.relationship("StoreModel" , back_populates = "items")
    tags = variables.relationship("TagsModel", back_populates="items" , secondary="tag_item")