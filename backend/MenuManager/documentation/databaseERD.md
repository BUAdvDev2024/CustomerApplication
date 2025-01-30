# Menu Manager Database Entity Relationship Diagram

## Main Table Diagram

These tables are the main functionality of the system, and will be implemented first.

```mermaid
erDiagram
    Product {
        int(pk) productID "not externally accessible"
        string token "Identifier used by other services"
        string name
        decimal price
        external description "DATA/descriptions/product/{token}.md"
        external images "DATA/images/product/{token}/{hash}.{filetype}"
        external image_thumbnails "DATA/images/product/{token}/{hash}.thumb.{filetype}"
        external image_metadata "DATA/images/product/{token}/images.json"
    }

    AddOn {
        int(PK) addonID
        string token
        string name
        external description "DATA/descriptions/addon/{token}.md"
        external images "DATA/images/addon/{token}/{hash}.{filetype}"
        external image_thumbnails "DATA/images/addon/{token}/{hash}.thumb.{filetype}"
        external image_metadata "DATA/images/addon/{token}/images.json"
    }

    PreCustomised_Product {
        int(PK) configurationID
        str token
        int(FK) productID
        str name
        external description "DATA/descriptions/custom/{token}.md"
        external images "DATA/images/custom/{token}/{hash}.{filetype}"
        external image_thumbnails "DATA/images/custom/{token}/{hash}.thumb.{filetype}"
        external image_metadata "DATA/images/custom/{token}/images.json"
    }
    
    Product }o--o{ AddOn: "[Product_AddOn_Link]<br />AddOn Price"
    PreCustomised_Product }o--|| Product: ""
    PreCustomised_Product }o--o{ AddOn: "[PreCustomised_Product_AddOn_Link]<br />Quantity"

```

## Link Table Diagram

These tables, only mentioned in the above section, are essential for a fully working relational database, and also store additional data about items that differ between links.

```mermaid
erDiagram
    Product_AddOn_Link {
        int(pk) AddOnLinkID
        int(fk) productID
        int(fk) addonID
        decimal addonPrice
    }

    PreCustomised_Product_AddOn_Link {
        int(PK) AddOnLinkID
        int(FK) preConfiguredID
        int(FK) addonID
        int quantity
    }
    
    Product ||--o{ Product_AddOn_Link: ""
    AddOn ||--o{ Product_AddOn_Link: ""
    Product ||--o{ PreCustomised_Product: ""
    PreCustomised_Product ||--o{ PreCustomised_Product_AddOn_Link: ""
    AddOn ||--o{ PreCustomised_Product_AddOn_Link: ""

```

## Future Planned Tables

These are the tables that *should* be implemented by this system, but are a lower priority, so will be added later on.

```mermaid
erDiagram
    Ingredient {
        int(PK) ingredientID
        str token
        str name
        int inventoryStock
        bool isAllergen
        external description "DATA/descriptions/ingredient/{token}.md"
    }

    Product ||--o{ Ingredient:  "[Product_Ingredient_Link]<br />Quantity used by Product"
```

This system is also needed to store the information about what is available at different franchise locations, prices if they differ from the default, and per-restaurants stock for the above table. The method for this is currently not determined, but may be done with a new table for storing information that differs on each item where it differs.
