from variables import variables

class BlockModel(variables.Model):
    __tablename__ = "block"
    id = variables.Column(variables.Integer ,primary_key= True)
    block = variables.Column(variables.String , nullable = False)