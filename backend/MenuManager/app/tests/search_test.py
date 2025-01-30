#!/usr/bin/env python3

from app.database import db, Product, AddOn, search_items
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def print_section_header(header):
    """Prints a formatted section header."""
    print(f"\n{'=' * 50}")
    print(f"{header:^50}")
    print(f"{'=' * 50}")

with app.app_context():
    # Verify the contents of the database
    try:
        print_section_header("Verifying Inserted Data")
        products = Product.query.all()
        addons = AddOn.query.all()

        print("Products:")
        if products:
            for product in products:
                print(f"  - {product.name} (Token: {product.token}, Price: ${product.price:.2f})")
        else:
            print("  No products found.")

        print("\nAddOns:")
        if addons:
            for addon in addons:
                print(f"  - {addon.name} (Token: {addon.token})")
        else:
            print("  No add-ons found.")
    except Exception as e:
        print(f"Error verifying data: {e}")

    # Run the search test
    try:
        print_section_header("Running Search Test")
        search_term = "pepperoni"
        print(f"Searching for: '{search_term}'")

        results = search_items(search_term)

        print("\nSearch Results:")
        print("Products:")
        if results["products"]:
            for product in results["products"]:
                print(f"  - {product.name} (Token: {product.token}, Price: ${product.price:.2f})")
        else:
            print("  No matching products found.")

        print("\nAddOns:")
        if results["addons"]:
            for addon in results["addons"]:
                print(f"  - {addon.name} (Token: {addon.token})")
        else:
            print("  No matching add-ons found.")
    except Exception as e:
        print(f"Error during search: {e}")
