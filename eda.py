import pandas as pd

df = pd.read_csv("online_retail.csv")
print(df.shape)
print(df.head())
df.info()

cancellations = df[df["InvoiceNo"].astype(str).str.startswith("C")]
print(cancellations.shape)

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
print(df["InvoiceDate"].min(), df["InvoiceDate"].max())

df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
monthly_sales = df.groupby(df["InvoiceDate"].dt.to_period("M"))["TotalPrice"].sum()
print(monthly_sales)

cancellations["TotalPrice"] = cancellations["Quantity"] * cancellations["UnitPrice"]
print(cancellations["TotalPrice"].sum())

total_sales = df["TotalPrice"].sum()
print(total_sales)
print(abs(cancellations["TotalPrice"].sum()) / total_sales * 100)

country_cancellations = cancellations.groupby("Country")["TotalPrice"].sum().sort_values()
print(country_cancellations.head(10))

country_cancellations_rate= abs(country_cancellations) / df.groupby("Country")["TotalPrice"].sum() * 100
print(country_cancellations_rate.sort_values(ascending=False).head(10))

country_counts = df["Country"].value_counts()
print(country_counts.loc[["Singapore", "USA", "Hong Kong", "United Kingdom"]])

purchases_only = df[df["Quantity"] > 0]
purchase_totals = purchases_only.groupby("Country")["TotalPrice"].sum()

correct_cancel_rate = abs(country_cancellations) / purchase_totals * 100
print(correct_cancel_rate.sort_values(ascending=False).head(10))

rfm_data = df[(df["Quantity"] > 0) & (df["CustomerID"].notna())]

customer_summary = rfm_data.groupby("CustomerID").agg(
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("TotalPrice", "sum")
)
print(customer_summary.head())

snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

recency = rfm_data.groupby("CustomerID")["InvoiceDate"].max()
recency = (snapshot_date - recency).dt.days

customer_summary["Recency"] = recency
print(customer_summary.head())

customer_summary["R_Score"] = pd.qcut(customer_summary["Recency"], 4, labels=[4,3,2,1])
customer_summary["F_Score"] = pd.qcut(customer_summary["Frequency"].rank(method="first"), 4, labels=[1,2,3,4])
customer_summary["M_Score"] = pd.qcut(customer_summary["Monetary"], 4, labels=[1,2,3,4])

print(customer_summary.head())

customer_summary["RFM_Score"] = customer_summary["R_Score"].astype(str) + customer_summary["F_Score"].astype(str) + customer_summary["M_Score"].astype(str)

def segment_customer(row):
    if row["R_Score"] == 4 and row["F_Score"] == 4:
        return "Champions"
    elif row["R_Score"] >= 3 and row["F_Score"] >= 3:
        return "Loyal Customers"
    elif row["R_Score"] <= 2 and row["F_Score"] <= 2:
        return "At Risk"
    else:
        return "Needs Attention"

customer_summary["Segment"] = customer_summary.apply(segment_customer, axis=1)
print(customer_summary.head(10))

segment_summary = customer_summary.groupby("Segment").agg(
    Customer_Count=("Monetary", "count"),
    Total_Revenue=("Monetary", "sum"),
    Avg_Monetary=("Monetary", "mean")
)
print(segment_summary.sort_values("Total_Revenue", ascending=False))

df.to_csv("online_retail_cleaned.csv", index=False)

customer_summary.to_csv("customer_rfm_segments.csv")