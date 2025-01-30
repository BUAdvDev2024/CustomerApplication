#!/usr/bin/env python3

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Product Table
class Product(db.Model):
    __tablename__ = 'products'

    productID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(500), nullable=True, default="")
    images = db.Column(db.String(200), nullable=True, default="static/images/default.jpg")
    image_thumbnails = db.Column(db.String(200), nullable=True, default="static/images/default_thumb.jpg")
    image_metadata = db.Column(db.String(200), nullable=True, default="static/images/default_metadata.json")
    isAvailable = db.Column(db.Boolean, nullable=False, default=True)  

    addons = db.relationship('ProductAddOnLink', back_populates='product', cascade="all, delete-orphan")
    precustomised_products = db.relationship('PreCustomisedProduct', back_populates='product', cascade="all, delete-orphan")
    ingredient_links = db.relationship('IngredientProductLink', back_populates='product', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product {self.name} (ID: {self.productID})>"


# AddOn Table
class AddOn(db.Model):
    __tablename__ = 'addons'

    addonID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.String(500), nullable=True, default="")
    images = db.Column(db.String(200), nullable=True, default="static/images/default.jpg")
    image_thumbnails = db.Column(db.String(200), nullable=True, default="static/images/default_thumb.jpg")
    image_metadata = db.Column(db.String(200), nullable=True, default="static/images/default_metadata.json")
    isAvailable = db.Column(db.Boolean, nullable=False, default=True)

    products = db.relationship('ProductAddOnLink', back_populates='addon', cascade="all, delete-orphan")
    precustomised_links = db.relationship('PreCustomisedProductAddOnLink', back_populates='addon', cascade="all, delete-orphan")
    ingredient_links = db.relationship('IngredientAddOnLink', back_populates='addon', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AddOn {self.name} (ID: {self.addonID})>"


# PreCustomisedProduct Table
class PreCustomisedProduct(db.Model):
    __tablename__ = 'precustomised_products'

    configurationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(50), unique=True, nullable=False, index=True)
    productID = db.Column(db.Integer, db.ForeignKey('products.productID', ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.String(500), nullable=True, default="")
    images = db.Column(db.String(200), nullable=True, default="static/images/default.jpg")
    image_thumbnails = db.Column(db.String(200), nullable=True, default="static/images/default_thumb.jpg")
    image_metadata = db.Column(db.String(200), nullable=True, default="static/images/default_metadata.json")

    product = db.relationship('Product', back_populates='precustomised_products')
    addons = db.relationship('PreCustomisedProductAddOnLink', back_populates='precustomised_product', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<PreCustomisedProduct {self.name} (ID: {self.configurationID})>"


# Ingredient Table
class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    ingredientID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    inventoryStock = db.Column(db.Integer, nullable=False, default=0)
    isAllergen = db.Column(db.Boolean, nullable=False, default=False)
    description = db.Column(db.String(500), nullable=True, default="")

    product_links = db.relationship('IngredientProductLink', back_populates='ingredient', cascade="all, delete-orphan")
    addon_links = db.relationship('IngredientAddOnLink', back_populates='ingredient', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Ingredient {self.name} (ID: {self.ingredientID})>"


# Link Table: Product_AddOn_Link
class ProductAddOnLink(db.Model):
    __tablename__ = 'product_addon_links'

    AddOnLinkID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    productID = db.Column(db.Integer, db.ForeignKey('products.productID', ondelete="CASCADE"), nullable=False)
    addonID = db.Column(db.Integer, db.ForeignKey('addons.addonID', ondelete="CASCADE"), nullable=False)
    addonPrice = db.Column(db.Numeric(10, 2), nullable=False)

    product = db.relationship('Product', back_populates='addons')
    addon = db.relationship('AddOn', back_populates='products')

    __table_args__ = (db.UniqueConstraint('productID', 'addonID', name='uq_product_addon'),)

    def __repr__(self):
        return f"<ProductAddOnLink ProductID: {self.productID}, AddOnID: {self.addonID}>"


# Link Table: PreCustomisedProduct_AddOn_Link
class PreCustomisedProductAddOnLink(db.Model):
    __tablename__ = 'precustomised_product_addon_links'

    AddOnLinkID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    preConfiguredID = db.Column(db.Integer, db.ForeignKey('precustomised_products.configurationID', ondelete="CASCADE"), nullable=False)
    addonID = db.Column(db.Integer, db.ForeignKey('addons.addonID', ondelete="CASCADE"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    precustomised_product = db.relationship('PreCustomisedProduct', back_populates='addons')
    addon = db.relationship('AddOn', back_populates='precustomised_links')

    __table_args__ = (db.UniqueConstraint('preConfiguredID', 'addonID', name='uq_precustomised_addon'),)

    def __repr__(self):
        return f"<PreCustomisedProductAddOnLink PreConfiguredID: {self.preConfiguredID}, AddOnID: {self.addonID}, Quantity: {self.quantity}>"


# Link Table: Ingredient-Product
class IngredientProductLink(db.Model):
    __tablename__ = 'ingredient_product_links'

    linkID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ingredientID = db.Column(db.Integer, db.ForeignKey('ingredients.ingredientID', ondelete="CASCADE"), nullable=False)
    productID = db.Column(db.Integer, db.ForeignKey('products.productID', ondelete="CASCADE"), nullable=False)
    quantityUsed = db.Column(db.Integer, nullable=False)

    ingredient = db.relationship('Ingredient', back_populates='product_links')
    product = db.relationship('Product', back_populates='ingredient_links')

    def __repr__(self):
        return f"<IngredientProductLink IngredientID: {self.ingredientID}, ProductID: {self.productID}, Quantity: {self.quantityUsed}>"


# Link Table: Ingredient-AddOn
class IngredientAddOnLink(db.Model):
    __tablename__ = 'ingredient_addon_links'

    linkID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ingredientID = db.Column(db.Integer, db.ForeignKey('ingredients.ingredientID', ondelete="CASCADE"), nullable=False)
    addonID = db.Column(db.Integer, db.ForeignKey('addons.addonID', ondelete="CASCADE"), nullable=False)
    quantityUsed = db.Column(db.Integer, nullable=False)

    ingredient = db.relationship('Ingredient', back_populates='addon_links')
    addon = db.relationship('AddOn', back_populates='ingredient_links')

    def __repr__(self):
        return f"<IngredientAddOnLink IngredientID: {self.ingredientID}, AddOnID: {self.addonID}, Quantity: {self.quantityUsed}>"

def search_items(search_term):
    """
    Search for products or add-ons by token, name, or description.

    :param search_term: The search keyword to match token, name, or description.
    :return: A dictionary with matching products and add-ons.
    """
    try:
        search_term = f"%{search_term.lower()}%"
        print(f"Searching for: {search_term}")

        # Query Products
        products = Product.query.filter(
            (Product.token.ilike(search_term)) |
            (Product.name.ilike(search_term)) |
            (Product.description.ilike(search_term))
        ).all()
        print(f"Products Found: {[product.name for product in products]}")

        # Query AddOns
        addons = AddOn.query.filter(
            (AddOn.token.ilike(search_term)) |
            (AddOn.name.ilike(search_term)) |
            (AddOn.description.ilike(search_term))
        ).all()
        print(f"AddOns Found: {[addon.name for addon in addons]}")

        return {
            "products": products,
            "addons": addons,
        }
    except Exception as e:
        print(f"Error during search: {e}")
        return {"products": [], "addons": []}
    
def update_availability():
    """
    Update the availability of products and add-ons based on ingredient stock levels.
    """
    # Update Product Availability
    products = Product.query.all()
    for product in products:
        is_available = True
        for link in product.ingredient_links:
            if link.quantityUsed > link.ingredient.inventoryStock:
                is_available = False
                break
        product.isAvailable = is_available

    # Update AddOn Availability
    addons = AddOn.query.all()
    for addon in addons:
        is_available = True
        for link in addon.ingredient_links:
            if link.quantityUsed > link.ingredient.inventoryStock:
                is_available = False
                break
        addon.isAvailable = is_available

    db.session.commit()
    print("Availability updated.")


def update_stock(ingredient_id, new_stock):
    """
    Update the stock for an ingredient and reevaluate availability.
    :param ingredient_id: The ID of the ingredient to update.
    :param new_stock: The new stock level.
    """
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        print(f"Ingredient with ID {ingredient_id} not found.")
        return

    ingredient.inventoryStock = new_stock
    print(f"Stock for {ingredient.name} updated to {new_stock}.")

    # Reevaluate availability
    update_availability()


print("Database setup complete.")