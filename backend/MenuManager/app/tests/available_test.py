from app.database import db, Product, AddOn, Ingredient, IngredientProductLink, IngredientAddOnLink, update_stock, update_availability
from flask import Flask

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def run_availability_test():
    """Test the availability functionality."""
    with app.app_context():
        # Step 1: Reset database
        print("Resetting database...")
        db.drop_all()
        db.create_all()

        # Step 2: Create ingredients
        print("Adding ingredients...")
        cheese = Ingredient(token="cheese", name="Cheese", inventoryStock=10, isAllergen=False)
        pepperoni = Ingredient(token="pepperoni", name="Pepperoni", inventoryStock=0, isAllergen=False)  # Out of stock
        olives = Ingredient(token="olives", name="Olives", inventoryStock=5, isAllergen=False)
        db.session.add_all([cheese, pepperoni, olives])
        db.session.commit()

        # Step 3: Create products
        print("Adding products...")
        margherita = Product(
            token="pizza_margherita",
            name="Margherita Pizza",
            price=8.99,
            description="A classic pizza with cheese and tomato."
        )
        meat_lovers = Product(
            token="pizza_meat_lovers",
            name="Meat Lovers Pizza",
            price=12.99,
            description="A pizza loaded with pepperoni and cheese."
        )
        db.session.add_all([margherita, meat_lovers])
        db.session.commit()

        # Step 4: Link ingredients to products
        print("Linking ingredients to products...")
        margherita_links = [
            IngredientProductLink(ingredientID=cheese.ingredientID, productID=margherita.productID, quantityUsed=5),
            IngredientProductLink(ingredientID=olives.ingredientID, productID=margherita.productID, quantityUsed=2)
        ]
        meat_lovers_links = [
            IngredientProductLink(ingredientID=cheese.ingredientID, productID=meat_lovers.productID, quantityUsed=3),
            IngredientProductLink(ingredientID=pepperoni.ingredientID, productID=meat_lovers.productID, quantityUsed=5)
        ]
        db.session.add_all(margherita_links + meat_lovers_links)
        db.session.commit()

        # Step 5: Update availability
        print("Updating availability...")
        update_availability()

        # Step 6: Verify availability
        print("\n--- Verifying Availability ---")
        products = Product.query.all()
        for product in products:
            availability_status = "In Stock" if product.isAvailable else "Out of Stock"
            print(f"Product: {product.name}, Availability: {availability_status}")

        # Step 7: Update stock and recheck availability
        print("\n--- Updating Stock Levels and Rechecking ---")
        update_stock(ingredient_id=pepperoni.ingredientID, new_stock=10)  # Restock pepperoni

        print("\n--- Verifying Availability After Restock ---")
        products = Product.query.all()
        for product in products:
            availability_status = "In Stock" if product.isAvailable else "Out of Stock"
            print(f"Product: {product.name}, Availability: {availability_status}")

        

if __name__ == "__main__":
    run_availability_test()
