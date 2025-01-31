<div align='center'>

# Order Management System

_The order management system responsible for handling customer orders, from restaurant based orders to smartphone orders._<br>

[![Tech Stack](https://img.shields.io/badge/tech%20stack-Python,Docker,MySQL-blue)](https://shields.io) [![License](https://img.shields.io/badge/license-MIT-blue)](https://shields.io)
</div> <br>

> _Link as a pull request or contact the Lead Developers to make changes to this repo_

---

### Key Responsibilities

- **Manage Orders:** Efficiently create, retrieve, store, update and delete customer orders.
- **Order Storage:** Maintain accurate records of customer orders, ensuring data integrity and reliability.
- **Provide Endpoints:** Develop well-defined endpoints for seamless interaction with orders, customers, and menu items.
- **Ensure Security:** Implement secure data transmission through encryption and compliance with GDPR regulations.
- **Authenticate Access:** Perform secure authentication for sub-systems interacting with this microservice using API keys.

### Additional Responsibilities
_These are additional responsibilities added to our system based upon the request of other modules and issue enhancements._

- **Metric Enhancements:** Provide metric data endpoints to other modules on customer orders stored within the database, such as average spendature, peak traffic time etc. 
- **Sales Reporting:** Provide sales report endpoints to other modules such as sales data on a given day, calculated by our system.

### Platforms Supported:
- Web, restaurant interfaces, smartphone apps, and more.

### Sub-System Communication

This system interacts with the following sub-systems for specific tasks such as submitting, reviewing, tracking orders, retrieving menu-item data, and more:

- [Menu Manager](https://github.com/BUAdvDev2024/MenuManager)
- [Logistics Management System](https://github.com/BUAdvDev2024/Logistics-Management-System)
- [Kitchen Interface](https://github.com/BUAdvDev2024/KitchenInterface)
- [Waiter Interface](https://github.com/BUAdvDev2024/WaiterInterface)

The following modules interact with our system by either providing data (DummyDataAPI) or consuming analysis data for their own consumption (Financial and Restuarant Monitoring System)
- [Dummy Data API](https://github.com/BUAdvDev2024/DummyDataAPI)
- [Financial Analysis System](https://github.com/BUAdvDev2024/Financial-Analysis-System)
- [Restuarant Monitoring System](https://github.com/BUAdvDev2024/Restaurant-Monitoring-System)

More sub-systems will be added for interactions as the project progresses.

---

# Consuming our API

### Run the Application

1. Assuming you have retrieved our docker-image / package already, run the repository by exposing port 5002.

2. Assuming this has been configured correctly, our API will be available at:

```
http://localhost:5002/api
```
3. When calling our API, you will need our API key passed as a bearer within the header of your request, else you WILL be denied entry / access to the information. If you want to see how this is achieved, you can check out our [get.py](https://github.com/BUAdvDev2024/Order-Management-System/blob/main/app/config/get.py) file which utilises this.

_Please scroll towards the bottom of the page for our API Endpoints. It is also important to note that you will need an API key, which we will contact you as needs be and update the instructions ASAP._

# System Requirements

| **Priority** | **Requirement**                                                                                                    | **Description**                                                                                                                                     |
|--------------|--------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| **Must**     | Data Verification                                                                                                 | The API **must** verify incoming data for privacy and security, ensuring data integrity.                                                             |
| **Must**     | External Database Interaction                                                                                     | The system **must** securely interact with an external menu database (or internal mock database for testing).                                        |
| **Must**     | Order Management                                                                                                  | The system **must** be able to push, manage, and update orders, including customer information, items in the order, and modifications to said items.  |
| **Must**     | Order Updates                                                                                                     | The system **must** support updates for existing orders, including their contents and order status.                                                  |
| **Must**     | Custom Order Fetching                                                                                             | The system **must** allow customized fetching of customer orders, such as specific items or by customer ID.                                          |
| **Must**     | Optimized Data Storage                                                                                            | Stored data **must** conform to the highest applicable normal form for database optimization and integrity.                                           |
| **Must**     | Multiple Items per Request                                                                                        | The API **must** support the passing of multiple items per request to optimize order creation.                                                       |
| **Must**     | API Key Authentication                                                                                            | Access to the system **must** be secured by an API key to ensure proper authentication and authorization.                                            |
| **Must**     | Statistics Tracking                                                                                               | The system **must** track order statistics, such as the number of orders created, completed, etc, for the LogisticsManagementSystem.                 |
| **Must**     | Consistency in Design                                                                                             | The system **must** be consistent in its design and handling across platforms and interfaces.                                                        |
| **Must**     | GDPR Compliance                                                                                                   | The system **must** comply with GDPR regulations, ensuring proper data handling and storage.                                                         |
| **Should**   | Encrypt Customer Information                                                                                      | The system **should** encrypt customer information for secure storage.                                                                               |
| **Should**   | Cross-Platform Usability                                                                                          | The system **should** ensure ease of use across different platforms.                                                                                 |
| **Could**    | Optimized Performance                                                                                             | The system **could** be optimized for faster performance and load times across platforms.                                                            |
| **Would**    | Advanced Analytics                                                                                                | The system **would** benefit from providing advanced analytics, such as customer behavior trends, for business insights.                              |

---

_More to be defined as progress continues_

Any further questions on the requirements or design feel free to contact any of the Lead Developers of this particular module. We aim to also work on the visual integration of this system into it's various use cases (such as the KitchenInterface and WaiterInterface)

# Use Case Diagram

![UseCaseOMS drawio](https://github.com/user-attachments/assets/c183731a-1be5-4dfb-b001-fc9fa2052d77)

# Development Journey

_Below is a list of the specified steps to achieve the full functionality of this sub-system_

---

1. [x] **Initial Setup**
   - [x] Define project structure
   - [x] Set up version control (Git)
   - [x] Install necessary libraries and dependencies
   - [x] Set up Docker for consistent environments

2. [x] **Database Integration**
   - [x] Establish connection to the Menu Database (or mock)
   - [x] Implement data retrieval for menu items
   - [x] Ensure secure handling of order and customer data
   - [x] Encrypt stored customer information (GDPR compliance)

3. [x] **API Integration**
   - [x] Set up the API and connection to the database
   - [x] Create basic CRUD functions for the API to interact with the database
   - [x] Integrate the API with web pages
   - [x] Connect the API to communicate with other subsystems

4. [x] **Server-based Functionality**
   - [x] Integrate the API with WaiterInterface

5. [ ] **Smartphone Ordering System**
   - [ ] AWAITING: Integrate the API with the Smarphone Application Ordering System

6. [x] **Remote Orders via Website**
   - [x] Integrate the API with a WebsiteOrderingInterface

7. [x] **Security and Compliance**
   - [x] Ensure GDPR-compliant data storage
   - [x] OBSOLETE: Encrypt customer payment information **(not required to store anymore)**
   - [x] Perform regular security audits and testing

8. [x] **UI/UX and Quality of Life Improvements**
   - [x] Ensure cross-platform consistency in design / interaction
   - [x] Optimize for clean and efficient user interactions
   - [x] Perform usability testing for different user flows

9. [ ] **Testing and Debugging**
   - [x] Write unit and integration tests for order handling
   - [ ] Conduct cross-platform testing (smartphone, restaurant, remote)
   - [x] Ensure load handling and performance optimization

---

# Our API Endpoints

Here are our API's Endpoints, please contact us if there needs to be more interaction possibilities.

Also, here is a reminder of the URL needed as a PREFIX to the following URLS:

```
http://localhost:5002/api
```
*To ensure clear clarification, if you'd like to use the Create Order endpoint, you will need to head to `http://localhost:5002/api/orders/create` with our API key in the header.*

### **Create Order**
```
POST /orders/create
```
The create order endpoint allows users to submit a new order with details including items, quantities, and any modifications.

##### **REQUEST BODY**
```json
{
  "user_id": 1,
  "order_type": "Eat In",
  "table_number": 5,
  "price":13.99,
  "branch_id":23981,
  "items": [
    {"item_id": 1, "quantity": 2},
    {"item_id": 2, "quantity": 1, "modifications": "extra cheese"}
  ]
}
```
- `user_id`: The ID of the waiter or customer placing the order.
- `order_type`: Either `Eat In`, `Takeaway`, or `Delivery`.
- `table_number`: For dine-in orders, specify the table number (optional for takeaway or delivery).
- `price`: The total price of the order in real format (£)
- `branch_id`: The branch id of the restuarant at which the order was placed.
- `items`: An array of items with their ID, quantity, and optional modifications.

##### **RESPONSE**  
**Success**  
```json
{
  "message": "Order has been created successfully",
  "order_id": 1,
  "order_type": "Eat In",
  "order_date": "2023-12-01T12:00:00Z",
  "status": "PENDING",
  "table_number": 5,
  "price": 13.99,
  "branch_id": 23981,
  "items": [
    {"item_id": 1, "quantity": 2},
    {"item_id": 2, "quantity": 1, "modifications": "extra cheese"}
  ]
}
```
**Failure**  
```json
{"error": "Invalid input data"}
```

---

### **View All Orders**
#### UPDATE: Now has an optional route to view all orders by a specific branch.
```
GET /orders
GET /orders/<branch_id>
```
Retrieve all orders, including their details and associated items. Optionally, retrieve all orders related to a specific branch, with the `branch_id` passed as an argument in the request.

##### **RESPONSE**  
**Success**  
```json
[
  {
    "order_id": 1,
    "user_id": 1,
    "order_date": "2023-12-01T12:00:00Z",
    "status": "Pending",
    "order_type": "Eat In",
    "table_number": 5,
    "price": 13.99,
    "branch_id": 23981,
    "items": [
      {"item_id": 1, "quantity": 2, "modifications": ""},
      {"item_id": 2, "quantity": 1, "modifications": "extra cheese"}
    ]
  }
// additional orders will also be encapsulated in here
]
```

---

### **View a Specific Order**
```
GET /orders/<order_id>
```
Fetch the details of a specific order by its ID either as an order_id. You will need the `order_id` of the order.

##### **RESPONSE**  
**Success**  
```json
{
  "order_id": 1,
  "user_id": 1,
  "order_date": "2023-12-01T12:00:00Z",
  "status": "Pending",
  "order_type": "Eat In",
  "table_number": 5,
  "price": 13.99,
  "branch_id": 23981,
  "items": [
    {"item_id": 1, "quantity": 2, "modifications": ""},
    {"item_id": 2, "quantity": 1, "modifications": "extra cheese"}
  ]
}
```
**Failure**  
```json
{"error": "Order not found"}
```

---

### **Update Order Status**
```
PUT /orders/<order_id>/status
```
Update the status of an existing order. You will need the `order_id` of the order to update it's specific status.

##### **REQUEST BODY**
```json
{
  "new_status": "In Progress"
}
```

- `new_status`: The new status for the order, which must be one of `Pending`, `In Progress`, or `Completed`

##### **RESPONSE**  
**Success**  
```json
{
  "message": "Order Status has been updated successfully",
  "order_id": 1,
  "new_status": "In Progress"
}
```
**Failure**  
```json
{"error": "Order not found or update failed"}
```

---

### **Amend Order Items**
```
PUT /orders/<order_id>/items
```
Replace the items of an existing order with a new set of items. You will need the `order_id` of the order to update it's items.

##### **REQUEST BODY**
```json
{
  "items": [
    {"item_id": 2, "quantity": 2},
    {"item_id": 3, "quantity": 1, "modifications": "no onions"}
  ]
}
```
- `items`: A new array of items for the order.

##### **RESPONSE**  
**Success**  
```json
{
  "message": "Order items have been amended successfully",
  "order_id": 1,
  "items": [
    {"item_id": 2, "quantity": 2},
    {"item_id": 3, "quantity": 1, "modifications": "no onions"}
  ]
}
```
**Failure**  
```json
{"error": "Invalid input data. New items for the order are required."}
```

---

### Additional Metric Data
We also provide additional metric data, such as, but not limited to:

- Calculating the most popular item per each individual branch.
- Calculating the percentage of beverage sales per each individual branch.
- Calculating the most popular order time slot per branch.
- Calculating the overall peak traffic hour of the business.
- Calculating the average time it takes for an order to be completed.
- Calculating the average value (price) per order per branch.
- Calculating the monthyl revenue per branch.

*Please contact any of the Lead Developers if your interested in these routes and how to retrieve them, or if your interested in suggesting additional metrics to measure.*

### **Notes for making Requests**
- All statuses for orders must be one of: `Pending`, `In Progress`, or `Completed`. Delivery Applications can update this status further with the likes of `Delivered` `Out for Delivery` `Failed` or `Cancelled`
- Ensure all IDs (e.g., `order_id`, `user_id`, and `item_id`) are valid and exist within the database.
- All endpoints are prefixed by the base URL where the application is running, e.g., `http://localhost:5002/api` so if you want to retrieve all orders this would be `http://localhost:5002/api/orders`
- Ensure the payloads match the expected formats to avoid `400 Bad Request` errors.

---

## Security

As of currently, our security considerations and discussions can be found [here](https://github.com/BUAdvDev2024/Order-Management-System/issues/18#issuecomment-2558664847) and our current, in place security methods shown below:

- Fernet Encryption and Decryption of relevant database data to comply with GDPR regulations (subject to all data)
- An API Key is required for the module to work. Sending requests without this API key for authorization as a header variable will cause the requests to fail.
- Integrated with the Security and Compliance module for IP address handling, checking and blacklisting.
- Looking into utilising HTTPS.

# Contacting to Contribute

If you can see any changes, ideas or tweaks to the existing product, or have made relevant programming to integrate with the full product, link as a pull request and contact the Lead Developers. All help is great help :>

# Lead Developers

 • [James Buttery](https://github.com/notsceptor)

 • [Harry Wilson](https://github.com/Wilhaz)
