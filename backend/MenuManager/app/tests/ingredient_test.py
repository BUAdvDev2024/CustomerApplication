from app.database import db, Product, AddOn, Ingredient, IngredientProductLink, IngredientAddOnLink
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    # Helper function to clear existing data
    def clear_existing_data():
        db.session.query(IngredientProductLink).delete()
        db.session.query(IngredientAddOnLink).delete()
        db.session.query(Ingredient).delete()
        db.session.query(Product).delete()
        db.session.query(AddOn).delete()
        db.session.commit()
        print("Existing data cleared.")

    # Create tables
    db.create_all()

    # Clear existing data to avoid duplicates
    clear_existing_data()

    # Helper function to get or create a product
    def get_or_create_product(token, name, price):
        existing_product = Product.query.filter_by(token=token).first()
        if existing_product:
            return existing_product
        new_product = Product(token=token, name=name, price=price)
        db.session.add(new_product)
        return new_product

    # Helper function to get or create an add-on
    def get_or_create_addon(token, name):
        existing_addon = AddOn.query.filter_by(token=token).first()
        if existing_addon:
            return existing_addon
        new_addon = AddOn(token=token, name=name)
        db.session.add(new_addon)
        return new_addon

    # Helper function to get or create an ingredient
    def get_or_create_ingredient(token, name, inventory_stock, is_allergen):
        existing_ingredient = Ingredient.query.filter_by(token=token).first()
        if existing_ingredient:
            return existing_ingredient
        new_ingredient = Ingredient(
            token=token,
            name=name,
            inventoryStock=inventory_stock,
            isAllergen=is_allergen
        )
        db.session.add(new_ingredient)
        return new_ingredient

    # Helper function to get or create a link between ingredients and products
    def get_or_create_ingredient_product_link(ingredient_id, product_id, quantity_used):
        existing_link = IngredientProductLink.query.filter_by(
            ingredientID=ingredient_id,
            productID=product_id
        ).first()
        if existing_link:
            return existing_link
        new_link = IngredientProductLink(
            ingredientID=ingredient_id,
            productID=product_id,
            quantityUsed=quantity_used
        )
        db.session.add(new_link)
        return new_link

    # Helper function to get or create a link between ingredients and add-ons
    def get_or_create_ingredient_addon_link(ingredient_id, addon_id, quantity_used):
        existing_link = IngredientAddOnLink.query.filter_by(
            ingredientID=ingredient_id,
            addonID=addon_id
        ).first()
        if existing_link:
            return existing_link
        new_link = IngredientAddOnLink(
            ingredientID=ingredient_id,
            addonID=addon_id,
            quantityUsed=quantity_used
        )
        db.session.add(new_link)
        return new_link

    # Add ingredients
    cheese = get_or_create_ingredient("cheese", "Cheese", 100, False)
    pepperoni = get_or_create_ingredient("pepperoni", "Pepperoni", 50, False)
    db.session.commit()

    # Add products and add-ons
    small_pizza = get_or_create_product("small_pizza", "Small Pizza", 8.99)
    pepperoni_topping = get_or_create_addon("pepperoni_topping", "Pepperoni Topping")
    db.session.commit()

    # Link ingredients to products and add-ons
    get_or_create_ingredient_product_link(cheese.ingredientID, small_pizza.productID, 2)
    get_or_create_ingredient_addon_link(pepperoni.ingredientID, pepperoni_topping.addonID, 3)
    db.session.commit()

    # Improved Query Output
    print("\n--- Products and Their Ingredients ---")
    for product in Product.query.all():
        print(f"Product: {product.name}")
        for link in product.ingredient_links:
            ingredient = db.session.get(Ingredient, link.ingredientID)
            print(f"  - Ingredient: {ingredient.name}, Quantity Used: {link.quantityUsed} units")

    print("\n--- AddOns and Their Ingredients ---")
    for addon in AddOn.query.all():
        print(f"AddOn: {addon.name}")
        for link in addon.ingredient_links:
            ingredient = db.session.get(Ingredient, link.ingredientID)
            print(f"  - Ingredient: {ingredient.name}, Quantity Used: {link.quantityUsed} units")
