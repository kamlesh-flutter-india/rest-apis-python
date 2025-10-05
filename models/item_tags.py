from db import db

class ItemTags(db.Model):
    __tablename__ = "items_tags"

    id = db.Column(db.Integer,primary_key = True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'),nullable = False,unique = False)
    # tags = db.relationship('TagModel',back_populates='tags')
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'),nullable = False,unique = False)
    # items = db.relationship('ItemModel',back_populates='items')