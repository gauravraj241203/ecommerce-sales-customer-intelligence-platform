import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns   

orders = pd.read_csv("Data/olist_orders_dataset.csv")
order_items = pd.read_csv("Data/olist_order_items_dataset.csv")

print("Data loaded successfully!")
print(orders.shape)
print(order_items.shape)

# Convert order purchase date to datetime
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

# Create month column
orders["month"] = orders["order_purchase_timestamp"].dt.to_period("M").astype(str)

# Merge orders with order items
sales = order_items.merge(
    orders[["order_id", "month"]],
    on="order_id",
    how="left"
)

# Calculate monthly revenue
monthly_revenue = (
    sales.groupby("month")["price"]
    .sum()
)

# Plot
plt.figure(figsize=(12, 6))

sns.lineplot(
    x=monthly_revenue.index,
    y=monthly_revenue.values,
    marker="o"
)

plt.title("Monthly Revenue Trend", fontsize=16)
plt.xlabel("Month")
plt.ylabel("Revenue (R$)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("Charts/monthly_revenue_trend.png", dpi=300, bbox_inches="tight")
plt.show()


# Load products
products = pd.read_csv("Data/olist_products_dataset.csv")

# Merge product category with sales data
category_sales = sales.merge(
    products[["product_id", "product_category_name"]],
    on="product_id",
    how="left"
)

# Calculate revenue by category
category_revenue = (
    category_sales
    .groupby("product_category_name")["price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# Plot
plt.figure(figsize=(12, 6))

sns.barplot(
    x=category_revenue.values,
    y=category_revenue.index
)

plt.title("Top 10 Product Categories by Revenue", fontsize=16)
plt.xlabel("Revenue (R$)")
plt.ylabel("Product Category")
plt.tight_layout()
plt.savefig("Charts/top_categories_revenue.png", dpi=300, bbox_inches="tight")
plt.show()

# Calculate units sold by category
category_units = (
    category_sales
    .groupby("product_category_name")["order_item_id"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

# Plot
plt.figure(figsize=(12, 6))

sns.barplot(
    x=category_units.values,
    y=category_units.index
)

plt.title("Top 10 Product Categories by Units Sold", fontsize=16)
plt.xlabel("Units Sold")
plt.ylabel("Product Category")
plt.tight_layout()
plt.savefig("Charts/top_categories_units.png", dpi=300, bbox_inches="tight")
plt.show()

# Load payments
payments = pd.read_csv("Data/olist_order_payments_dataset.csv")

# Count payment methods
payment_counts = (
    payments["payment_type"]
    .value_counts()
)

# Plot
plt.figure(figsize=(10, 6))

sns.barplot(
    x=payment_counts.index,
    y=payment_counts.values
)

plt.title("Payment Method Distribution", fontsize=16)
plt.xlabel("Payment Method")
plt.ylabel("Number of Payments")

plt.tight_layout()
plt.savefig("Charts/payment_method_distribution.png", dpi=300, bbox_inches="tight")
plt.show()

# Load reviews
reviews = pd.read_csv("Data/olist_order_reviews_dataset.csv")

# Count review scores
review_counts = (
    reviews["review_score"]
    .value_counts()
    .sort_index()
)

# Plot
plt.figure(figsize=(10, 6))

sns.barplot(
    x=review_counts.index,
    y=review_counts.values
)

plt.title("Customer Review Score Distribution", fontsize=16)
plt.xlabel("Review Score")
plt.ylabel("Number of Reviews")

plt.tight_layout()
plt.savefig("Charts/review_score_distribution.png", dpi=300, bbox_inches="tight")
plt.show()

# Calculate delivery time in days
orders["order_delivered_customer_date"] = pd.to_datetime(
    orders["order_delivered_customer_date"]
)

orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.total_seconds() / (60 * 60 * 24)

# Create delivery ranges
delivery_ranges = pd.cut(
    orders["delivery_days"],
    bins=[0, 7, 14, 30, float("inf")],
    labels=["0-7 days", "8-14 days", "15-30 days", "30+ days"]
)

delivery_counts = (
    delivery_ranges
    .value_counts()
    .sort_index()
)

# Plot
plt.figure(figsize=(10, 6))

sns.barplot(
    x=delivery_counts.index,
    y=delivery_counts.values
)

plt.title("Order Delivery Time Distribution", fontsize=16)
plt.xlabel("Delivery Time")
plt.ylabel("Number of Orders")

plt.tight_layout()
plt.savefig("charts/delivery_time_distribution.png", dpi=300, bbox_inches="tight")
plt.show()

# Load sellers
sellers = pd.read_csv("Data/olist_sellers_dataset.csv")
# Merge seller information with order items
seller_data = order_items.merge(
    sellers[["seller_id", "seller_state"]],
    on="seller_id",
    how="left"
)

# Calculate revenue by seller state
state_revenue = (
    seller_data
    .groupby("seller_state")["price"]
    .sum()
    .sort_values(ascending=False)
)

# Plot
plt.figure(figsize=(12, 7))

sns.barplot(
    x=state_revenue.values,
    y=state_revenue.index
)

plt.title("Revenue by Seller State", fontsize=16)
plt.xlabel("Revenue (R$)")
plt.ylabel("Seller State")

plt.tight_layout()
plt.savefig("Charts/revenue_by_seller_state.png", dpi=300, bbox_inches="tight")
plt.show()