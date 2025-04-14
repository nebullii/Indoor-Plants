# Indoor Plant Store

A Django-based e-commerce platform for buying and selling indoor plants. This project is designed to help plant enthusiasts and small businesses easily manage and explore a curated collection of indoor plants—with a clean interface and seamless payment integration via Stripe.

**Live Demo:** [indoorplant.store](https://nevus.pythonanywhere.com/)

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- **User Authentication:** Secure registration and login system.
- **Product Catalog:** Browse, search, and filter indoor plants.
- **Shopping Cart:** Easily add/remove products and proceed to checkout.
- **Stripe Integration:** Secure and smooth payment processing.
- **Admin Panel:** Manage plant listings, orders, and inventory.
- **Responsive Design:** Optimized for both desktop and mobile devices.

---

## Tech Stack

- ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
- ![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
- ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
- ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3)
- ![Stripe](https://img.shields.io/badge/Stripe-008CDD?style=flat&logo=stripe)
- ![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

---

## Prerequisites

- **Python 3.6+**
- **pip** (Python package installer)
- **Django** (Installed via pip)
- A Stripe account for payment integration (for testing and production)

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nebullii/Indoor-Plant.git
   cd Indoor-Plant
   ```

2. Set up a virtual environment (recommended):

   ```bash
   python -m venv myenv
   ```

3. Activate the virtual environment:

   - On macOS/Linux:

     ```bash
     source myenv/bin/activate
     ```

   - On Windows:

     ```bash
     myenv\Scripts\activate
     ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Apply migrations:

   ```bash
   python manage.py migrate
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

7. Open your browser and visit:

   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Usage

- **User Signup/Login:** Create an account to start shopping.
- **Browse Plants:** View detailed pages for each plant with descriptions and prices.
- **Add to Cart & Checkout:** Add products to your cart and proceed to a secure Stripe-powered checkout.
- **Admin Features:** Use the built-in admin panel (accessible at `/admin`) to manage product listings and view orders.
- **Live Demo:** Check out the hosted version [here](https://nevus.pythonanywhere.com/).

---

## Screenshots

**Homepage Banner:**

![Homepage Banner](https://github.com/user-attachments/assets/18460240-56d1-474c-a5b6-3c01eb365f00)

**Product Showcase:**

![Product Showcase](https://github.com/user-attachments/assets/8d454edc-4697-485c-9b80-ca90a35da004)

**User Dashboard:**

![User Dashboard](https://github.com/user-attachments/assets/a666188f-0042-4c11-928e-f3310018d971)

**Cart View:**

![Cart View](https://github.com/user-attachments/assets/5f6d5678-8135-4bc7-a25c-52184ee5a36c)

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature`)
6. Open a Pull Request

Feel free to submit issues for any bugs or feature requests.
