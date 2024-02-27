from variables import variables

class TagsModel(variables.Model):
    __tablename__ = "tag"

    id = variables.Column(variables.Integer , primary_key = True)
    name = variables.Column(variables.String , unique = True , nullable = False)
    store_id = variables.Column(variables.Integer , variables.ForeignKey("stores.id") , nullable = False , unique = False)

    store = variables.relationship("StoreModel" , back_populates = "tags")                          #here you are trying to get the entire store elements, thats why its realtionsip ig, and foreginkey
    items = variables.relationship("ItemModel" , back_populates = "tags" , secondary="tag_item")    # In SQLAlchemy, the secondary argument in the relationship method is used to define a many-to-many relationship between two classes (or tables) when there is an intermediary association table that links the two primary tables together.
    