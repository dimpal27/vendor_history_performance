# Vendor Management System with Performance Metrics

This project is a Vendor Management System built using Django and Django REST Framework. It allows users to manage vendor profiles, track purchase orders, and calculate vendor performance metrics.

## Features

1. **Vendor Profile Management**: Users can create, retrieve, update, and delete vendor profiles.
2. **Purchase Order Tracking**: Users can create, retrieve, update, and delete purchase orders. Purchase orders can be filtered by vendor.
3. **Vendor Performance Evaluation**: Performance metrics such as on-time delivery rate, quality rating average, average response time, and fulfillment rate are calculated and available for each vendor.

## Installation

1. Clone the repository:
git clone "<rpositoryurl>"

2. Install dependencies:
pip install -r requirements.txt

3. Apply migrations:
python manage.py makemigrations

python manage.py migrate

4. Run the development server:
python manage.py runserver

5. Run TestCase :
python manage.py test vendor_app

## Usage

1. **API Endpoints**:

   - **Vendor Endpoints**:
     - `GET /api/vendors/`: List all vendors (requires authentication).
     - `POST /api/vendors/`: Create a new vendor (requires authentication).
     - `GET /api/vendors/{vendor_id}/`: Retrieve details of a specific vendor.
     - `PUT /api/vendors/{vendor_id}/`: Update a vendor.
     - `DELETE /api/vendors/{vendor_id}/`: Delete a vendor.

   - **Purchase Order Endpoints**:
     - `GET /api/purchase_orders/`: List all purchase orders (requires authentication).
     - `POST /api/purchase_orders/`: Create a new purchase order (requires authentication).
     - `GET /api/purchase_orders/{po_id}/`: Retrieve details of a specific purchase order.
     - `PUT /api/purchase_orders/{po_id}/`: Update a purchase order.
     - `DELETE /api/purchase_orders/{po_id}/`: Delete a purchase order.

   - **Performance Metrics Endpoints**:
     - `GET /api/vendors/{vendor_id}/performance/`: Retrieve performance metrics for a specific vendor.

   - **Acknowledgment Endpoint**:
     - `POST /api/purchase_orders/{po_id}/acknowledge/`: Acknowledge a purchase order.

2. **Authentication**:
   
   - Authentication is required to access certain endpoints. Use the `/api/token/` endpoint to obtain a JWT token by providing valid credentials (username and password). Include this token in the `Authorization` header of subsequent requests.

3. **Data Validation**:

   - The application performs data validation to ensure data integrity and handle scenarios like missing data points or division by zero in calculations.

4. **Real-time Updates**:

   - Django signals are used to trigger metric updates in real-time when related purchase order data is modified.

