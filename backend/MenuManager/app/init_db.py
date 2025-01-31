#!/usr/bin/env python3

from app.database import (
    db,
    Product,
    AddOn,
    Ingredient,
    ProductAddOnLink,
    IngredientProductLink,
    IngredientAddOnLink,
    PreCustomisedProduct,
    PreCustomisedProductAddOnLink
)
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def create_file_paths(base_path, token):
    """
    This function generates a path for an image, thumbnail, and respective metadata.
    paramter = base_path: Base directory path (e.g., 'products', 'addons', 'precustomisedProducts').
    parameter = token: Unique token for the object.
    returns a dictionary with paths for image, thumbnail, and metadata.
    """
    return {
        "images": f"static/images/{base_path}/{token}/img.jpg",
        "image_thumbnails": f"static/images/{base_path}/{token}/thumbnail.jpg",
        "image_metadata": f"static/images/{base_path}/{token}/metadata.json"
    }

def create_and_seed_database():
    """initialize and seed the database with data."""
    with app.app_context():
        # Drop and recreate tables so data isnt carried over
        print("Resetting database...")
        db.drop_all()
        db.create_all()

        try:
            # Add products
            print("Adding products...")
            small_pizza_paths = create_file_paths("products", "pizza_small")
            large_pizza_paths = create_file_paths("products", "pizza_large")

            small_pizza = Product(
                token="pizza_small",
                name="Small Pizza",
                price=8.99,
                description="A small pizza with delicious toppings.",
                **small_pizza_paths
            )
            large_pizza = Product(
                token="pizza_large",
                name="Large Pizza",
                price=12.99,
                description="A large pizza for sharing.",
                **large_pizza_paths
            )
            db.session.add_all([small_pizza, large_pizza])
            db.session.commit()

            # Add add-ons
            print("Adding add-ons...")
            extra_cheese_paths = create_file_paths("addons", "addon_cheese")
            pepperoni_topping_paths = create_file_paths("addons", "addon_pepperoni")

            extra_cheese = AddOn(
                token="addon_cheese",
                name="Extra Cheese",
                description="Add more cheese to your pizza.",
                **extra_cheese_paths
            )
            pepperoni_topping = AddOn(
                token="addon_pepperoni",
                name="Pepperoni",
                description="Add pepperoni slices to your pizza.",
                **pepperoni_topping_paths
            )
            db.session.add_all([extra_cheese, pepperoni_topping])
            db.session.commit()

            # Add pre-customized products
            print("Adding pre-customized products...")
            meat_lovers_paths = create_file_paths("precustomisedProducts", "meat_lovers")

            meat_lovers_pizza = PreCustomisedProduct(
                token="meat_lovers",
                productID=large_pizza.productID,
                name="Meat Lovers Pizza",
                description="A large pizza loaded with extra pepperoni and cheese.",
                **meat_lovers_paths
            )
            db.session.add(meat_lovers_pizza)
            db.session.commit()

            # Link pre-customized products to add-ons
            print("Linking pre-customized products to add-ons...")
            pre_link1 = PreCustomisedProductAddOnLink(
                preConfiguredID=meat_lovers_pizza.configurationID,
                addonID=extra_cheese.addonID,
                quantity=2
            )
            pre_link2 = PreCustomisedProductAddOnLink(
                preConfiguredID=meat_lovers_pizza.configurationID,
                addonID=pepperoni_topping.addonID,
                quantity=3
            )
            db.session.add_all([pre_link1, pre_link2])
            db.session.commit()

            print("Database initialized and seeded successfully.")

        except Exception as e:
            db.session.rollback()
            print(f"Error seeding database: {e}")

if __name__ == "__main__":
    create_and_seed_database()
