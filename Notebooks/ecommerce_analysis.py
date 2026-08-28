import pandas as pd

orders = pd.read_csv("Data/olist_orders_dataset.csv")

print(orders.head())
print(orders.columns)
print(orders.shape)
print(orders.dtypes)
print(orders.isnull().sum())
print(orders.groupby("order_status").size())

delivery_rate = (orders["order_status"] == "delivered").mean() * 100

print(f"Delivery Rate: {delivery_rate:.2f}%")

print("Total rows:", len(orders))
print("Unique orders:", orders["order_id"].nunique())

print(orders.info())

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_columns:
    orders[col] = pd.to_datetime(orders[col])

print(orders.dtypes)   

order_items = pd.read_csv("Data/olist_order_items_dataset.csv")

print(order_items.head())
print(order_items.shape)
print(order_items.columns)
print(order_items.dtypes)

print(order_items.isnull().sum())

print("Total rows:", len(order_items))
print("Duplicate rows:", order_items.duplicated().sum())

order_items["shipping_limit_date"] = pd.to_datetime(
    order_items["shipping_limit_date"]
)

print(order_items.dtypes)
print(order_items["price"].describe())

print(order_items["freight_value"].describe())

total_revenue = order_items["price"].sum()

print(f"Total Revenue: R$ {total_revenue:,.2f}")

total_freight = order_items["freight_value"].sum()

print(f"Total Freight: R$ {total_freight:,.2f}")

total_orders = orders["order_id"].nunique()

aov = total_revenue / total_orders

print(f"Total Orders: {total_orders:,}")
print(f"Average Order Value: R$ {aov:,.2f}")

total_customers = orders["customer_id"].nunique()

print(f"Total Customers: {total_customers:,}")

orders_per_customer = orders.groupby("customer_id")["order_id"].nunique()

repeat_customers = (orders_per_customer > 1).sum()

print(f"Repeat Customers: {repeat_customers:,}")

customers = pd.read_csv("Data/olist_customers_dataset.csv")

print(customers.head())
print(customers.shape)
print(customers.dtypes)

orders_customers = orders.merge(
    customers[["customer_id", "customer_unique_id"]],
    on="customer_id",
    how="left"
)

print(orders_customers.head())


total_unique_customers = orders_customers["customer_unique_id"].nunique()

print(f"Real Total Customers: {total_unique_customers:,}")

orders_per_customer = (
    orders_customers
    .groupby("customer_unique_id")["order_id"]
    .nunique()
)

repeat_customers = (orders_per_customer > 1).sum()

print(f"Repeat Customers: {repeat_customers:,}")

repeat_customer_rate = (
    repeat_customers / total_unique_customers
) * 100

print(f"Repeat Customer Rate: {repeat_customer_rate:.2f}%")


product_revenue = (
    order_items
    .groupby("product_id")["price"]
    .sum()
    .sort_values(ascending=False)
)

print(product_revenue.head(10))



products = pd.read_csv("Data/olist_products_dataset.csv")

print(products.head())

print(products.shape)
print(products.isnull().sum())
print(products.dtypes)
print(
    products[
        products["product_category_name"].isnull()
    ].head()
)

order_items_products = order_items.merge(
    products[["product_id", "product_category_name"]],
    on="product_id",
    how="left"
)

print(order_items_products.head())

category_revenue = (
    order_items_products
    .groupby("product_category_name")["price"]
    .sum()
    .sort_values(ascending=False)
)

print(category_revenue.head(10))

order_items_analysis = order_items.merge(
    orders[["order_id", "order_purchase_timestamp"]],
    on="order_id",
    how="left"
)

print(order_items_analysis.head())

order_items_analysis["month"] = (
    order_items_analysis["order_purchase_timestamp"]
    .dt.to_period("M")
)

print(order_items_analysis[["order_purchase_timestamp", "month"]].head())

monthly_revenue = (
    order_items_analysis
    .groupby("month")["price"]
    .sum()
)

print(monthly_revenue)

best_month = monthly_revenue.idxmax()
best_month_revenue = monthly_revenue.max()

print(f"Best Revenue Month: {best_month}")
print(f"Revenue: R$ {best_month_revenue:,.2f}")


worst_month = monthly_revenue.idxmin()
worst_month_revenue = monthly_revenue.min()

print(f"Lowest Revenue Month: {worst_month}")
print(f"Revenue: R$ {worst_month_revenue:,.2f}")

monthly_growth = monthly_revenue.pct_change() * 100


print(monthly_growth)


status_counts = orders["order_status"].value_counts()

print(status_counts)
delivered_rate = (
    orders["order_status"] == "delivered"
).mean() * 100

print(f"Delivered Rate: {delivered_rate:.2f}%")

payments = pd.read_csv("Data/olist_order_payments_dataset.csv")

print(payments.head())
print(payments.shape)
print(payments.columns)
print(payments.isnull().sum())
print(payments.dtypes)

print(payments["payment_type"].value_counts())

payment_revenue = (
    payments
    .groupby("payment_type")["payment_value"]
    .sum()
    .sort_values(ascending=False)
)

print(payment_revenue)

installments = (
    payments["payment_installments"]
    .value_counts()
    .sort_index()
)

print(installments)


average_payment = payments["payment_value"].mean()

print(f"Average Payment Value: R$ {average_payment:,.2f}")

reviews = pd.read_csv("Data/olist_order_reviews_dataset.csv")

print(reviews.head())
print(reviews.shape)
print(reviews.columns)

print(reviews.isnull().sum())
print(reviews["review_score"].value_counts().sort_index())

average_review = reviews["review_score"].mean()

print(f"Average Review Score: {average_review:.2f} / 5")

positive_review_rate = (
    reviews["review_score"].isin([4, 5]).mean()
) * 100

print(f"Positive Review Rate: {positive_review_rate:.2f}%")

orders_reviews = orders.merge(
    reviews[["order_id", "review_score"]],
    on="order_id",
    how="left"
)

print(orders_reviews.head())

status_review = (
    orders_reviews
    .groupby("order_status")["review_score"]
    .mean()
    .sort_values(ascending=False)
)

print(status_review)

orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.total_seconds() / (60 * 60 * 24)

print(orders["delivery_days"].describe())

slow_deliveries = orders[
    orders["delivery_days"] > 30
]

print(f"Orders over 30 days: {len(slow_deliveries):,}")

delivery_ranges = pd.cut(
    orders["delivery_days"],
    bins=[0, 7, 14, 30, float("inf")],
    labels=["0-7 days", "8-14 days", "15-30 days", "30+ days"]
)

print(delivery_ranges.value_counts().sort_index())

sellers = pd.read_csv("Data/olist_sellers_dataset.csv")

print(sellers.head())
print(sellers.shape)
print(sellers.columns)

print(sellers.isnull().sum())
print(sellers.duplicated().sum())

seller_revenue = (
    order_items
    .groupby("seller_id")["price"]
    .sum()
    .sort_values(ascending=False)
)

print(seller_revenue.head(10))

seller_analysis = order_items.merge(
    sellers[["seller_id", "seller_city", "seller_state"]],
    on="seller_id",
    how="left"
)

print(seller_analysis.head())


seller_state_revenue = (
    seller_analysis
    .groupby("seller_state")["price"]
    .sum()
    .sort_values(ascending=False)
)

print(seller_state_revenue)


seller_city_revenue = (
    seller_analysis
    .groupby("seller_city")["price"]
    .sum()
    .sort_values(ascending=False)
)

print(seller_city_revenue.head(10))

top_products = (
    order_items
    .groupby("product_id")["order_item_id"]
    .count()
    .sort_values(ascending=False)
)

print(top_products.head(10))



product_analysis = order_items.merge(
    products[["product_id", "product_category_name"]],
    on="product_id",
    how="left"
)

print(product_analysis.head())

category_units = (
    product_analysis
    .groupby("product_category_name")["order_item_id"]
    .count()
    .sort_values(ascending=False)
)

print(category_units.head(10))

category_avg_price = (
    product_analysis
    .groupby("product_category_name")["price"]
    .mean()
    .sort_values(ascending=False)
)

print(category_avg_price.head(10))

total_units = len(order_items)

print(f"Total Units Sold: {total_units:,}")
