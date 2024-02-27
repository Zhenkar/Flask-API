#__init__ file makes the directory as a library
# every time when I have to access the class inside this folder/files I would have to write ""from models.items import ItemModel"" [from outside of this folder]
# every time A file types " import models " the __init__ file will run first and we would have defined those long lines inside __init__ , therefore we can directly access the class ItemModel 

# example - import models                           [instead of writing this - from models.items import ItemModel] [every time you want to access a new class from the folder you'd have to write this lengthy line eveytime , over her just one line is enough]    
#           object =  models.ItemModel                     

from models.item import ItemModel
from models.store import StoreModel
from models.tags import TagsModel
from models.tag_item import TagItem
from models.user import UserModel
from models.blocklist import BlockModel
