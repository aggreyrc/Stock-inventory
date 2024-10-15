from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime

# from config import db

db = SQLAlchemy()

# Models go here!

# Product table

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    
    # Relationship to Sale-detail
    sales = db.relationship('SaleDetail', back_populates='product')
    
    
    def __repr__(self):
        return f'Product(id={self.id}, ' + \
            f'name={self.name}, ' + \
            f'description={self.description}, ' + \
            f'price={self.price})' + \
            f'quantity={self.quantity}, ' + \
            f'supplier_id={self.supplier_id})'
                
   
# Suppliers table
 
class Supplier(db.Model, SerializerMixin):
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    
    # Relationship to Product
    products = db.relationship('Product', back_populates='supplier')
    
    def __repr__(self):
        return f'Supplier(supplier_id={self.id}, ' + \
                f'name = {self.name}, ' + \
                f'contact_person = {self.contact_person}, ' + \
                f'email = {self.email}, ' + \
                f'phone = {self.phone})'

# Customer table

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    
    # Relationship to Sale
    sales = db.relationship('Sale', back_populates='customer', lazy=True)
    
    def __repr__(self):
        return f'Customer(customer_id={self.id}, ' + \
            f'name={self.name}, ' + \
            f'phone={self.phone}' + \
            f'email={self.email})'

# Sale table

class Sale(db.Model, SerializerMixin):
    __tablename__ = 'sales'
     
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    
    # Relationship to Customer and Sale-detail
    sale_details = db.relationship('SaleDetail', back_populates='sale', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'Sale(id={self.id}, ' + \
                f'customer_id={self.customer_id}, ' + \
                f'date={self.date}, ' + \
                f'total_amount={self.total_amount})'

# Sale-detail table

class SaleDetail(db.Model, SerializerMixin):
    __tablename__ = 'sales_details'
    
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    
    # Relationship to Sale and Product
    sale = db.relationship('Sale', back_populates='sale_details')
    product = db.relationship('Product', back_populates='sales')
    
    def __repr__(self):
        return f'SaleDetail(id={self.id}, ' + \
                f'sale_id={self.sale_id}, ' + \
                f'product_id={self.product_id}, ' + \
                f'quantity={self.quantity}, ' + \
                f'unit_price={self.unit_price})'