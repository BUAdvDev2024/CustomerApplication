# Customer Application Module
<b>Purpose </b> <br>
The Customer Application Module is  supposed to replicate a unified mobile platform application that a customer would use to interact with various services such as ordering food, providing feedback, managing loyalty rewards, and more. This will be built to integrate multiple backend modules seamlessly to deliver a smooth user experience. 

---
# Requirement for Customer Application

## Must Have
- Menu Browsing
    - Display the full menu with categories (starters, mains, desserts, etc.).
    - Integration: MenuManager.
- Order Placement
    - Allow customers to place orders for delivery, takeaway, or dine-in.
    - Integration: Order-Management-System.
- User Authentication
    - Enable customers to register, log in, and manage their accounts.
    - Integration: Authentication.
- Order Tracking
    - Show order preparation and delivery status in real time.
    - Integration: KitchenManagementInterface, Logistics-Management-System.
- Payment
    - Include payment options (e.g., card or wallet-based).
    - Integration: Order-Management-System.
- Restaurant Finder
    - Use geolocation to display the nearest branches with hours and contact info.
## Should Have
- Loyalty Program
    - Display loyalty points and redemption options.
    - Integration: Loyalty Program Integration.
- Feedback System
    - Enable customers to provide feedback or reviews on orders.
    - Integration: Customer-Feedback-System.
- Table Reservation
    - Allow customers to book tables via the app.
    - Integration: TableReservationSystem.
- Stock-Based Item Availability
    - Display real-time availability of menu items.
    - Integration: Stock Management System.
## Could Have
- Push Notifications
    - Notify users about order status, offers, or loyalty rewards.
    - Integration: Expo Notifications (standalone).
- Customizable Menu
    - Allow customers to customize dishes (e.g., toppings for pizzas).
- Offline Browsing
    - Cache the menu and loyalty data for offline access.
## Won't Have
- Employee-Focused Features
    - Modules like EmployeeManagementSystem, Payroll, or HMRC Interface are outside the app’s customer-focused scope.
- Complex Reporting
    - Advanced analytics or reporting modules for restaurant management.

--- 
## GDPR Relevance
This application is designed with user data privacy and security as a priority, aligning with the General Data Protection Regulation (GDPR) requirements. Key measures include:

- Data Minimization:
    - The application collects only essential user information required to deliver its services (e.g., order details, feedback, and loyalty program data).
- User Consent:
    - Users must explicitly consent to data collection and usage when signing up or providing feedback.
    - Clear and transparent explanations are provided about how their data will be used.
- Data Access and Portability:
    - Users can access their data through the app, including order history and loyalty points.
    - Options are available for users to request their data in a portable format.
- Right to Erasure:
    - Users can request the deletion of their personal data at any time by contacting support or using in-app options.
- Data Security:
    - All personal data is encrypted both in transit and at rest.
    - Backend modules are deployed using secure environments and follow best practices for data protection.
- Third-Party Services:
    - Any third-party integrations (e.g., email services, payment providers) are reviewed for GDPR compliance to ensure the protection of user data.

By adhering to these principles, the application ensures compliance with GDPR and fosters trust and transparency with its users. For any GDPR-related queries or requests, users can contact the designated Data Protection Officer (DPO) via the app’s support system.

---
This module integrates with: 
- [Customer Feedback System](https://github.com/BUAdvDev2024/CustomerFeedbackSystem)
- [Menu Manager](https://github.com/BUAdvDev2024/MenuManager)
- [Order Management System](https://github.com/BUAdvDev2024/Order-Management-System)
- [Table Reservation System](https://github.com/BUAdvDev2024/TableReservationSystem)