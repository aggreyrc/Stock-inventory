#!/usr/bin/env python3

# Remote library imports
from flask import request, Flask,jsonify,make_response
from flask_restful import Resource, Api, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS


from models import db, Product, Supplier, Customer, Sale, SaleDetail

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

CORS(app)

# Views go here!

class Home(Resource):
    def get(self):
        return '<h1>Project Server</h1>'
    
# Get products
class Products(Resource):
    def get(self, id=None):
        products = Product.query.all()
        response = {'products': [product.to_dict() for product in products]}
        return response, 200
    
# Product by id
class ProductById(Resource):
    def get(self, id):
        product = Product.query.filter_by(id=id).first()
        if product:
            return product.to_dict(), 200
        else:
            return {'message': 'No products found. Please add some.'}, 404

    # Edit a product
    def patch(self, id):
        product = Product.query.filter_by(id=id).first()
        if product:
            data = request.get_json()
            for attr, value in data.items():
                setattr(product, attr, value)
            db.session.commit()
            return product.to_dict(), 200
        else:
            return {'message': 'No product found'}, 404
        
    # Delete a product
    def delete(self, id):
        product = Product.query.filter_by(id=id).first()
        if product:
            db.session.delete(product)
            db.session.commit()
            return {'message': 'Product deleted successfully.'}, 200
        else:
            return {'message': 'No product found'}, 404
    
# Create a new product
class CreateProduct(Resource):
    def post(self):
        data = request.get_json()
        
        new_product = Product(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            quantity=data['quantity'],
            supplier_id=data['supplier_id']
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product.to_dict(), 201
    
    
api.add_resource(Home, '/')
api.add_resource(Products, '/products')
api.add_resource(ProductById, '/products/<int:id>')
api.add_resource(CreateProduct, '/products')




if __name__ == '__main__':
    app.run(port=5555, debug=True)

