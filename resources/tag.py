from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from db import db
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from models import TagModel,StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint('Tags','tags',description='Operations on tags')

@blp.route('/store/<int:store_id>/tag')
class TagsInStore(MethodView):
    @blp.response(200,TagSchema(many=True))
    def get(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201,TagSchema)
    def post(self,tag_data,store_id):
        # if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data['name']).first():
        #     abort(400,message='Tag with same name already exists')
        # store = StoreModel.query.get_or_404(store_id)
        tag = TagModel(**tag_data,store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message=str(e))
        return tag

@blp.route('/tag/<int:tag_id>')
class TagsInStore(MethodView):
    @blp.response(200,TagSchema)
    def get(self,tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    @blp.response(202,
                  description="Deletes a tag if no item is linked",
                  example={"message": "Tag deleted"}
                  )
    @blp.alt_response(404,description="Tag not found")
    @blp.alt_response(400,description="Tag is linked to many items")
    def delete(self,tag_id):
        tag = StoreModel.query.get_or_404(tag_id)

        if not tag.items: 
            db.session.delete(tag)
            db.session.commit()
            return {"message":"Success"},200
        abort(400,message='Could not delete')

@blp.route('/item/<int:item_id>/tag/<int:tag_id>')
class LinkTagsToItem(MethodView):    
    @blp.response(200,TagSchema)
    def post(self,item_id,tag_id):
        try:
            item = ItemModel.query.get_or_404(item_id)
            tag = TagModel.query.get_or_404(tag_id)
            item.tags.append(tag)
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message='Something went wrong')
        return tag
   
    @blp.response(200,TagAndItemSchema)
    def delete(self,item_id,tag_id):
        try:
            item = ItemModel.query.get_or_404(item_id)
            tag = TagModel.query.get_or_404(tag_id)
            item.tags.remove(tag)
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message='Something went wrong')
        return {"message": "item removed from tags", 'item': item,"tag": tag}





