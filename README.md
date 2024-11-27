# Indoor Plant Store

A Django-based e-commerce platform for buying and selling indoor plants. Features include user authentication, shopping cart, order management, and an admin dashboard.

## Features

- User Authentication (Customer & Seller)
- Product Catalog with Categories
- Shopping Cart
- Order Management
- Admin Dashboard
- Secure Payment Integration
- Responsive Design

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Virtual environment

## Installation

### 1. Clone the repository
git clone https://github.com/yourusername/Indoor-Plant.git

cd Indoor-Plant

### 2. Create virtual environment
python -m venv venv

### 3. Activate virtual environment
#### For macOS/Linux:
source venv/bin/activate
#### For Windows:
venv\Scripts\activate

### 4. Install dependencies
pip install -r requirements.txt

### 5. Database Setup
python manage.py migrate

### 6. Run the development server
python manage.py runserver
