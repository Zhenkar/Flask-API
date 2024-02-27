from variables import variables


class TagItem(variables.Model):
    __tablename__ = "tag_item"

    id = variables.Column(variables.Integer, primary_key = True)
    item_id = variables.Column(variables.Integer , variables.ForeignKey("items.id"))
    tag_id = variables.Column(variables.Integer , variables.ForeignKey("tag.id"))