#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc
import random

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, Customer, Product, Sale, SaleDetail, Supplier


if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        
        Customer.query.delete()
        Product.query.delete()
        Sale.query.delete()
        SaleDetail.query.delete()
        Supplier.query.delete()
        
        print("Starting seed...")
        # Seed code goes here!
        products = []
        customers = []
        sales = []
        saledetails = []
        suppliers = []
        
        for _ in range(10):
            product = Product(
                name=fake.name(),
                description=fake.text(max_nb_chars=200),
                price=fake.random_int(min=1, max=100, step=1) + round(random.uniform(0, 1), 2),
                quantity=randint(1, 100),
                supplier_id=randint(1, 5)
            )
            db.session.add(product)
            products.append(product)
            
        for _ in range(20):
            customer = Customer(
                name=fake.name(),
                email=fake.email(),
                phone=fake.phone_number()
            )
            db.session.add(customer)
            customers.append(customer)
            
        for _ in range(20):
            sale = Sale(
                customer_id=randint(1, 20),
                date=fake.date_this_year(),
                total_amount=fake.random_int(min=10, max=500, step=1) + round(random.uniform(0, 1), 2)
            )
            db.session.add(sale)
            sales.append(sale)
            
        for _ in range(20):
            saledetail = SaleDetail(
                sale_id=randint(1, 20),
                product_id=randint(1, 10),
                quantity=randint(1, 10),
                unit_price=randint(1, 20)
            )
            db.session.add(saledetail)
            saledetails.append(saledetail)
            
        for _ in range(20):
            supplier = Supplier(
                name=fake.name(),
                contact_person=fake.name(),
                email=fake.email(),
                phone=fake.phone_number()
            )
            db.session.add(supplier)
            suppliers.append(supplier)
            
            
        db.session.commit()
        print("Database seeded successfully with random data.")

        
