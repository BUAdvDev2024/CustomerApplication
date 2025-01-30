# Menu Management API Requirements

| #       | Requirement                                                                                                            | Complete |
| ------- | ---------------------------------------------------------------------------------------------------------------------- | -------- |
| 1       | There will be an API, providing access to all features                                                                 |          |
| 1.1     | Read only access will be provided without any authentication                                                           |          |
| 1.2     | Write operations will require an authentication token of an authorised user                                            |          |
| 2       | There will be a Web Interface, providing access to all features                                                        |          |
| 2.1     | Users must log in, and be a member of staff, to access the web interface                                               |    x     |
| 3       | There will be a database of products                                                                                   |    x     |
| 3.1     | There will be a table of available products, eg. small pizza, medium pizza                                             |    x     |
| 3.1.1   | Price, description, nutritional information, and images, will be stored                                                |    x     |
| 3.1.2   | There will be a search functionality for products                                                                      |    x     |
| 3.2     | There will be a table of available extras, per product, e.g. for optional pizza toppings                               |    x     |
| 3.2.1   | Price, description, nutritional information, and images, will be stored                                                |    x     |
| 3.2.2   | The same topping will be available on multiple pizza sizes, but different prices will be possible for the same topping |    x     |
| 3.2.3   | There will be a table for pre-customised pizzas, with their own unique images and descriptions                         |    x     |
| 3.3     | There will be a table of ingredients                                                                                   |    x     |
| 3.3.1   | Ingredients can be added for a topping or product                                                                      |    x     |
| 3.3.2   | Ingredients can exist purely to provide allergen information for individual ingredients                                |    x     |
| 3.3.3   | Ingredients can have an in-stock quantity, and products/toppings specify how much of that ingredient they use          |    x     |
| 3.3.3.1 | When an ingredient with this configuration is out of stock, the product or topping will be marked as unavailable       |    x     |

