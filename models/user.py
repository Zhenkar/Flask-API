from variables import variables

class UserModel(variables.Model):
    __tablename__ = "user"

    id = variables.Column(variables.Integer , primary_key = True)
    name = variables.Column(variables.String , unique = True , nullable = False)
    password = variables.Column(variables.String , nullable = False)
