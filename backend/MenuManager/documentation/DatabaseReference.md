# Menu Manager Documentation

This documentation outlines the design, structure, and testing of the Menu Manager database system. The goal is to provide a clear understanding of its components, functionality, and tests.

---

## **Overview**

The Menu Manager database system is designed to manage products, add-ons, ingredients, and pre-customized products in a flexible, relational manner. It supports dynamic features such as availability tracking, ingredient stock management, and product customization. Below, you will find details of the database schema, its relationships, and the associated test scripts.

---

## **Database Schema**

### **Products Table**
- **Purpose:** Stores information about all the products available in the menu.
- **Key Fields:**
  - `productID`: Unique identifier.
  - `token`: Short, unique string for referencing.
  - `name`: Product name.
  - `price`: Product price.
  - `isAvailable`: Boolean to indicate availability.

### **AddOns Table**
- **Purpose:** Stores information about optional add-ons for products.
- **Key Fields:**
  - `addonID`: Unique identifier.
  - `token`: Short, unique string for referencing.
  - `name`: Add-on name.
  - `isAvailable`: Boolean to indicate availability.

### **Ingredients Table**
- **Purpose:** Stores ingredient details, including stock levels and allergen information.
- **Key Fields:**
  - `ingredientID`: Unique identifier.
  - `token`: Short, unique string for referencing.
  - `inventoryStock`: Current stock of the ingredient.
  - `isAllergen`: Boolean to indicate allergen presence.

### **PreCustomizedProducts Table**
- **Purpose:** Defines products with pre-applied add-ons for easier ordering.
- **Key Fields:**
  - `configurationID`: Unique identifier.
  - `productID`: Linked base product.
  - `name`: Name of the pre-customized product.

### **Link Tables**
1. **ProductAddOnLink:** Links products and add-ons with pricing.
2. **IngredientProductLink:** Links ingredients to products with quantity used.
3. **IngredientAddOnLink:** Links ingredients to add-ons with quantity used.
4. **PreCustomisedProductAddOnLink:** Links pre-customized products to add-ons with quantity required.

---

## **Core Functionalities**

### **1. Availability Tracking**
- Products and add-ons are marked "In Stock" or "Out of Stock" based on ingredient availability.
- Helper functions:
  - `update_availability()`: Updates availability for all products and add-ons.
  - `update_stock(ingredient_id, new_stock)`: Updates stock levels for ingredients and rechecks availability.

### **2. Search Functionality**
- Allows searching for products and add-ons by token, name, or description.
- Function:
  - `search_items(search_term)`: Returns matching products and add-ons.

---

## **Testing**

Testing ensures that the database system functions as intended and handles edge cases.

### **1. `available_test.py`**
#### **Purpose:**
Tests the availability tracking system.

#### **Steps:**
1. Reset the database.
2. Add ingredients with varying stock levels.
3. Add products and link them to ingredients.
4. Verify availability before and after updating ingredient stock levels.

#### **Key Functions:**
- `update_availability()`
- `update_stock()`

#### **Sample Output:**
```plaintext
--- Verifying Availability ---
Product: Margherita Pizza, Availability: In Stock
Product: Meat Lovers Pizza, Availability: Out of Stock

--- Verifying Availability After Restock ---
Product: Meat Lovers Pizza, Availability: In Stock
```

---

### **2. `ingredient_test.py`**
#### **Purpose:**
Validates the linking of ingredients to products and add-ons, and ensures queries work correctly.

#### **Steps:**
1. Clear and reset the database.
2. Add products, add-ons, and ingredients.
3. Link ingredients to products and add-ons.
4. Query and display the relationships.

#### **Sample Output:**
```plaintext
--- Products and Their Ingredients ---
Product: Small Pizza
  - Ingredient: Cheese, Quantity Used: 2 units

--- AddOns and Their Ingredients ---
AddOn: Pepperoni Topping
  - Ingredient: Pepperoni, Quantity Used: 3 units
```

---

### **3. `pcp_test.py`**
#### **Purpose:**
Tests the relationships of pre-customized products, base products, and their add-ons.

#### **Steps:**
1. Query pre-customized products.
2. Display their base product and linked add-ons.

#### **Sample Output:**
```plaintext
--- Testing Pre-Customized Products ---
Pre-Customized Product: Meat Lovers Pizza (Token: custom_meat_lovers)
  - Base Product: Medium Pizza
  - Add-Ons:
    * Extra Cheese (Quantity: 2)
    * Pepperoni (Quantity: 1)
```

---

### **4. `search_test.py`**
#### **Purpose:**
Verifies that the search functionality works as intended.

#### **Steps:**
1. Populate the database with sample data.
2. Search for products and add-ons using keywords.

#### **Sample Output:**
```plaintext
--- Running Search Test ---
Searching for: 'pepperoni'

Search Results:
Products:
  - No matching products found.

AddOns:
  - Pepperoni (Token: addon_pepperoni)
```

---

### **5. `queries_test.py`**
#### **Purpose:**
Tests advanced queries for products, add-ons, and pre-customized products.

#### **Steps:**
1. Populate the database.
2. Query products and their linked add-ons.
3. Query pre-customized products and their add-ons.

#### **Sample Output:**
```plaintext
--- Fetching All Products and Their Add-Ons ---
Product: Small Pizza
  - AddOn: Extra Cheese, Price: $1.50

--- Fetching Pre-Customized Products and Their Add-Ons ---
Pre-Customized Product: Meat Lovers Pizza
  - AddOn: Extra Cheese, Quantity: 2
```

---

## **Future Improvements**
- Add API endpoints for external module integration.
- Develop a web interface for easier management.
- Implement notifications for low ingredient stock levels.
- Add nutritional information for products and add-ons.

---

This documentation provides a comprehensive overview of the Menu Manager system and its testing. Feel free to expand as new features are developed.
