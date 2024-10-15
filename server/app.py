#!/usr/bin/env python3

# Remote library imports
from flask import request, Flask,jsonify,make_response
from flask_restful import Resource, Api, reqparse
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
    # List all products
    def get(self):
        products = Product.query.all()
        response = {'products': [product.to_dict() for product in products]}
        return response, 200
    
    # Create a new product
    def post(self):
    
        parser = reqparse.RequestParser()
        
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('description', type=str)
        parser.add_argument('price', type=float, required=True, help='Price is required')
        parser.add_argument('quantity', type=int, required=True, help='Quantity is required')
        parser.add_argument('supplier_id', type=int, required=True, help='Supplier ID is required')
        
        args = parser.parse_args()
        
        new_product = Product(
            name=args['name'],
            description=args['description'],
            price=args['price'],
            quantity=args['quantity'],
            supplier_id=args['supplier_id'])
        
        db.session.add(new_product)
        db.session.commit()
        
        response_dict = "Product created successfully.", new_product.to_dict()
        
        return response_dict, 201
    
# Product by id
class ProductById(Resource):
    def get(self, id):
        product = Product.query.filter_by(id=id).first()
        if product:
            return product.to_dict(), 200
        else:
            return {'message': 'No products found. Please add some.'}, 404

    # Update a product
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
    
    
    
api.add_resource(Home, '/')
api.add_resource(Products, '/products')
api.add_resource(ProductById, '/products/<int:id>')


# Suppliers Resources
class Suppliers(Resource):
    
    # Get all suppliers
    def get(self):
        suppliers = Supplier.query.all()
        response = {'suppliers': [supplier.to_dict() for supplier in suppliers]}
        return response, 200
    
    # Create a new supplier
    def post(self):
        
        parser = reqparse.RequestParser()
        
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('contact_person', type=str, required=True, help='Contact person is required')
        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('phone', type=str, required=True, help='Phone is required')
        
        args = parser.parse_args()
        
        new_supplier = Supplier(
            name=args['name'],
            contact_person=args['contact_person'],
            email=args['email'],
            phone=args['phone'])
        
        db.session.add(new_supplier)
        db.session.commit()
        
        response_dict = "Supplier created successfully.", new_supplier.to_dict()
        
        return response_dict, 201
    
api.add_resource(Suppliers, '/suppliers')


# Customers Resources
class Customers(Resource):
    
    # Get all customers
    def get(self):
        customers = Customer.query.all()
        response = {'customers': [customer.to_dict() for customer in customers]}
        return response, 200
    
    # Create a new customer
    def post(self):
        
        parser = reqparse.RequestParser()
        
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('phone', type=str, required=True, help='Phone is required')
        
        args = parser.parse_args()
        
        new_customer = Customer(
            name=args['name'],
            email=args['email'],
            phone=args['phone'])
        
        db.session.add(new_customer)
        db.session.commit()
        
        response_dict = "Customer created successfully.", new_customer.to_dict()
        
        return response_dict, 201
    

api.add_resource(Customers, '/customers')


# Sales Resources
class Sales(Resource):
    
    # Get all sales
    def get(self):
        sales = Sale.query.all()
        response = {'sales': [sale.to_dict() for sale in sales]}
        return response, 200
    
    # Create a new sale
    def post(self):
        
        parser = reqparse.RequestParser()
        
        parser.add_argument('customer_id', type=int, required=True, help='Customer ID is required')
        parser.add_argument('total_amount', type=float, required=True, help='Total amount is required')
        
        args = parser.parse_args()
        
        new_sale = Sale(
            customer_id=args['customer_id'],
            total_amount=args['total_amount'])
        
        db.session.add(new_sale)
        db.session.commit()
        
        response_dict = "Sale created successfully.", new_sale.to_dict()
        
        return response_dict, 201
    

api.add_resource(Sales, '/sales')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

