from marshmallow import Schema , fields

class PlainItemsvalidate(Schema):                       # this class only contains information related to items, no store information, for store_id I have created a new class called Itemsvalidate
    id = fields.Int(dump_only = True)                   # dump_only because , you are not receving id data from the user to be validated, you are generating the id and just want to send when there is a get requrest , so you only dump it when asked.
    name = fields.Str(required=True)                    # Must enter the data for the field when the client is sending the data. It is different form load_only , the data over here can be sent to the client but not the load_only data.
    price = fields.Float(required = True)


class PlainStorevalidate(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str(required = True)

class PlainTagvalidate(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str()# required is not there , why?


class ItemsUpdate(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()                              # this is used when the put request is going to create a new item, and creating a new item needs the store id so I have included store_id. If put is used to update, then the store_id does not have required, so this particular filed will be ignored

class Itemsvalidate(PlainItemsvalidate):
    store_id = fields.Int(requreied= True , load_only=True)                              #load only means the it can take store_id from the user. You cannot use it for sending the data to the client.
    store = fields.Nested(PlainStorevalidate() , dump_only=True)                        # Nested because, I am saying marshmallow that this(store, inside the Itemsvalidate class) variable has a relationship with the sotrevalidate class to get the store_id data
    tags = fields.List(fields.Nested(PlainTagvalidate()) , dump_only = True)

class Storevalidate(PlainStorevalidate):
    items = fields.List(fields.Nested(PlainItemsvalidate()),dump_only=True)            # I know that item variable in the StoreModel class will get me all the items connected to this particaluar store, so there will be a list of them, that's why fields.list()
    tags = fields.List(fields.Nested(PlainTagvalidate()) , dump_only = True)
                                                                                       # fields.List(fields.Nested(PlainItemsvalidate())) , nested because there is a relationship between StoreModel and  Itemvalidat(ItemModel) for getting all the data connected to that particular store 
class Tagvalidate(PlainTagvalidate):
    store_id = fields.Int( load_only = True)
    store = fields.Nested(PlainStorevalidate(), dump_only = True)
    items = fields.List(fields.Nested(PlainItemsvalidate()) , dump_only = True)

class TagItemvalidate(Schema):
    message = fields.Str()
    item = fields.Nested(Itemsvalidate)
    tag = fields.Nested(Tagvalidate)

class Uservalidate(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str(required=True)
    password = fields.Str(load_only= True)
    

