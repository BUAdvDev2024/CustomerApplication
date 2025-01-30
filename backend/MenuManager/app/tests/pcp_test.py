from app.database import db, Product, AddOn, PreCustomisedProduct, PreCustomisedProductAddOnLink
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def test_pre_customized_products():
    """Test and display the relationships of pre-customized products."""
    with app.app_context():
        print("\n--- Testing Pre-Customized Products ---")
        pre_customized_products = PreCustomisedProduct.query.all()

        if not pre_customized_products:
            print("No pre-customized products found.")
            return

        for pc_product in pre_customized_products:
            print(f"\nPre-Customized Product: {pc_product.name} (Token: {pc_product.token})")
            print(f"  - Description: {pc_product.description}")
            print(f"  - Base Product: {pc_product.product.name}")

            if pc_product.addons:
                print(f"  - Add-Ons:")
                for link in pc_product.addons:
                    print(f"    * {link.addon.name} (Quantity: {link.quantity})")
            else:
                print("  - No add-ons linked.")

if __name__ == "__main__":
    test_pre_customized_products()
