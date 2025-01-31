#!/usr/bin/env python3

from app.database import db, Product, AddOn, PreCustomisedProduct, ProductAddOnLink, PreCustomisedProductAddOnLink
from flask import Flask
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

# Initialize Flask app and database globally
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Function to set up the database
def setup_db():
    with app.app_context():
        db.create_all()
        print("Database setup complete.")

# Function to clear all existing data
def clear_existing_data():
    with app.app_context():
        db.session.query(ProductAddOnLink).delete()
        db.session.query(PreCustomisedProductAddOnLink).delete()
        db.session.query(PreCustomisedProduct).delete()
        db.session.query(AddOn).delete()
        db.session.query(Product).delete()
        db.session.commit()
        print("Existing data cleared.")

# Function to populate database with sample data
def populate_db():
    with app.app_context():
        try:
            # Clear existing data to prevent duplicates
            clear_existing_data()

            # Add products
            product1 = Product(token="prod_small_pizza", name="Small Pizza", price=8.99)
            product2 = Product(token="prod_medium_pizza", name="Medium Pizza", price=12.99)

            # Add add-ons
            addon1 = AddOn(token="addon_cheese", name="Extra Cheese")
            addon2 = AddOn(token="addon_pepperoni", name="Pepperoni")
            addon3 = AddOn(token="addon_mushrooms", name="Mushrooms")

            # Add pre-customized product
            preconfigured1 = PreCustomisedProduct(
                token="custom_meat_lovers",
                name="Meat Lovers Pizza",
                product=product2,  # Based on Medium Pizza
            )

            # Link products with add-ons
            link1 = ProductAddOnLink(product=product1, addon=addon1, addonPrice=1.50)
            link2 = ProductAddOnLink(product=product1, addon=addon2, addonPrice=2.00)
            link3 = ProductAddOnLink(product=product2, addon=addon3, addonPrice=1.75)

            # Link pre-customized products with add-ons
            pre_link1 = PreCustomisedProductAddOnLink(precustomised_product=preconfigured1, addon=addon1, quantity=2)
            pre_link2 = PreCustomisedProductAddOnLink(precustomised_product=preconfigured1, addon=addon2, quantity=1)

            # Add to session and commit
            db.session.add_all([product1, product2, addon1, addon2, addon3, preconfigured1, link1, link2, link3, pre_link1, pre_link2])
            db.session.commit()

            print("Sample data added successfully.")

        except IntegrityError as e:
            db.session.rollback()
            print(f"Error adding sample data: {e}")

# Function to test database queries
def test_queries():
    with app.app_context():
        print("\n--- Fetching All Products and Their Add-Ons ---")
        products = Product.query.all()
        for product in products:
            print(f"Product: {product.name} (ID: {product.productID})")
            for link in product.addons:
                print(f"  - AddOn: {link.addon.name}, Price: ${link.addonPrice}")

        print("\n--- Fetching Pre-Customized Products and Their Add-Ons ---")
        precustomised_products = PreCustomisedProduct.query.all()
        for custom_product in precustomised_products:
            print(f"Pre-Customized Product: {custom_product.name} (ID: {custom_product.configurationID})")
            for link in custom_product.addons:
                print(f"  - AddOn: {link.addon.name}, Quantity: {link.quantity}")

# Function to clean up database
def cleanup_db():
    with app.app_context():
        db.drop_all()  # Drop all tables to leave the database in a clean state
        print("Database tables dropped. Cleanup complete.")

# Main script execution
if __name__ == "__main__":
    print("Setting up database...")
    setup_db()

    print("Populating database...")
    populate_db()

    print("\n--- Verifying Tables ---")
    with app.app_context():
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            for row in result.fetchall():
                print(f"Table: {row[0]}")

    print("Running queries...")
    test_queries()

    print("Cleaning up database...")
    cleanup_db()
