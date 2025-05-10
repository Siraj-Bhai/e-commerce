# E-Commerce Backend

This project is a basic e-commerce backend built using **Django**, **Django REST Framework (DRF)**, **JWT Authentication**, and **MySQL (via XAMPP)**. It allows users to register as buyers or sellers, manage products, and create orders.

## Project Setup

### Prerequisites

- Python 3.x
- Django 3.x or later
- Django REST Framework
- MySQL (via XAMPP)
- `pip` for installing dependencies
- **Postman** (for testing API endpoints)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone
   
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

3. **Database Setup**
   ```bash
   1. Start MySQL in XAMPP
   2. Create database as "ecommerce_db"
   3. Provide DB username and password in settings.py file

4. **Database Migrations**
   ```bash
   python manage.py makemigrations
   
   python manage.py migrate

5. **Run the Server**
   ```bash
   python manage.py runserver

### 📌 API Endpoints Documentation
#### 🧑‍💻 User Endpoints
Register (Buyer or Seller)

    POST /api/register/
    
    To register seller or buyer

Login (JWT Token)

    POST /api/token/
    
    Access Token Sent in Authorization: Bearer <token> header
    Refresh Token Used to renew expired access tokens.


#### 🛒 Product Endpoints
Add Product (Seller only)

    POST /api/products/
    
    To create a new product on the seller.

List Products

    GET /api/products/

    Optional Filters:
      - name — filter by name
      - price — filter by price
      - page — pagination

#### 📦 Order Endpoints
Create Order (Buyer only)

    POST /api/orders/
    
    To create order on the buyer

List Orders

    GET /api/orders/

    - Buyers see their own orders.
    - Sellers see orders that contain their products.

## 📚 Swagger/OpenAPI Docs
*    /swagger - For Swagger Documentation
*    /redoc - For Reference Documentation