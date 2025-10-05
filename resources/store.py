import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from db import db
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from models.store import StoreModel
from schemas import StoreSchema, StoreUpdateSchema

blp = Blueprint('Stores',__name__,description="Operations on stores")

@blp.route('/store/<int:store_id>')
class Store(MethodView):
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
        # try:
        #     return stores[store_id],200
        # except KeyError:
        #     abort(404,message= "store not found") 

    def delete(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message":"Success"},200
    
    @blp.arguments(StoreUpdateSchema)
    @blp.response(201,StoreSchema)
    def put(self,store_data,store_id):
        store = StoreModel.query.get(store_id)
        if store:
            item.name = store_data['name']
        else: 
            item = StoreModel(id = store_id, **store_data)
        db.session.add(item)
        db.session.commit()
        return store

@blp.route('/store')
class StoreList(MethodView):
    @blp.response(200,StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
        
    
    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(self,store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort (400, message='Store already exists')
        except SQLAlchemyError:
            abort (500, message='An error ocuured while inserting data')
        return store

