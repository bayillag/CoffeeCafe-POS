# CoffeeCafe-POS

A modern Point of Sale system for coffee shops and cafes.

## Features

- **Inventory Management**: Track stock levels in real-time
- **Loyalty Program**: Reward frequent customers
- **Employee Management**: Role-based access control
- **Reporting**: Sales analytics and insights
- **Receipt Printing**: USB thermal printer support

## Setup

1. Clone the repository
2. Create a `.env` file based on `.env.example`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `python -m app.main`

## Supabase Setup

Create the following tables in your Supabase project:

- `products`
- `orders`
- `order_items`
- `inventory`
- `employees`
- `customers`

## License

MIT