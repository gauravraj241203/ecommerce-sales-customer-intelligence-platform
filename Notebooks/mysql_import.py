import pandas as pd
from sqlalchemy import create_engine, URL

connection_url = URL.create(
    "mysql+pymysql",
    username="root",
    password="Gaurav@123",
    host="localhost",
    database="ecommerce_analytics"
)

engine = create_engine(connection_url)

print("MySQL connection successful!")

# CSV file path
file_path = r"D:\E-commerce Analystics\Data\olist_orders_dataset.csv"

# Read CSV
orders = pd.read_csv(file_path)

print("CSV loaded!")
print("Rows:", len(orders))

# Import into MySQL
orders.to_sql(
    "orders",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=5000
)

print("Orders imported successfully!")

# Load customers CSV
customers = pd.read_csv(
    r"D:\E-commerce Analystics\Data\olist_customers_dataset.csv"
)

print("Customers loaded!")
print("Rows:", len(customers))

# Import into MySQL
customers.to_sql(
    "customers",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=5000
)

print("Customers imported successfully!")

# Load order items CSV
order_items = pd.read_csv(
    r"D:\E-commerce Analystics\Data\olist_order_items_dataset.csv"
)

print("Order items loaded!")
print("Rows:", len(order_items))

# Import into MySQL
order_items.to_sql(
    "order_items",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=5000
)

print("Order items imported successfully!")
# Load products CSV
products = pd.read_csv(
    r"D:\E-commerce Analystics\Data\olist_products_dataset.csv"
)

print("Products loaded!")
print("Rows:", len(products))

# Import into MySQL
products.to_sql(
    "products",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=5000
)

print("Products imported successfully!")

# Load payments CSV
payments = pd.read_csv(
    r"D:\E-commerce Analystics\Data\olist_order_payments_dataset.csv"
)

print("Payments loaded!")
print("Rows:", len(payments))

# Import into MySQL
payments.to_sql(
    "payments",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=5000
)

print("Payments imported successfully!")

# Load reviews CSV
reviews = pd.read_csv(
    r"D:\E-commerce Analystics\Data\olist_order_reviews_dataset.csv"
)

print("Reviews loaded!")
print("Rows:", len(reviews))

# Import into MySQL
reviews.to_sql(
    "reviews",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=5000
)

print("Reviews imported successfully!")


# Load sellers CSV
sellers = pd.read_csv(
    r"D:\E-commerce Analystics\Data\olist_sellers_dataset.csv"
)

print("Sellers loaded!")
print("Rows:", len(sellers))

# Import into MySQL
sellers.to_sql(
    "sellers",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=5000
)

print("Sellers imported successfully!")