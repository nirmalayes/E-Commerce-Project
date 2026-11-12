# E-Commerce Sales & Customer Segmentation Dashboard

An end-to-end analysis of a UK-based online retailer's transaction data, combining Python (EDA, data cleaning, RFM segmentation) and Power BI (interactive dashboard), covering one year of real transactional data.

## Business Problem

Online retailers need to understand not just how much they're selling, but which customers actually drive the business, and where revenue is being lost to cancellations. This project analyzes 541,909 transactions to answer:

- What does the monthly sales trend look like, and what's driving peaks and dips?
- How much revenue is lost to order cancellations, and does this vary meaningfully by country?
- Which customers are most valuable, and how much of total revenue do they represent?

## Data Source

[Online Retail Dataset](https://archive.ics.uci.edu/ml/datasets/online+retail) (UCI Machine Learning Repository) — real transactions from a UK-based online retailer, December 2010–December 2011. 541,909 rows: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country. Invoices starting with "C" are cancellations. ~25% of rows have no CustomerID (guest/unidentified transactions).

## Data Cleaning

- Converted `InvoiceDate` from text to a proper date/time type (handled in Python, since Power Query's locale-based date parsing proved unreliable across the full dataset — see note below)
- Created `TotalPrice` = Quantity × UnitPrice
- Identified 9,288 cancellation rows (InvoiceNo starting with "C")
- Built a dedicated Date table in Power BI for time intelligence, with a date-only column added to the Sales table to enable a working relationship (timestamps vs. plain dates don't match automatically)

**A note on cancellation rate calculations:** an early version of the cancellation-rate-by-country calculation used net sales (purchases minus cancellations already netted out) as the denominator, which produced mathematically invalid results — some countries showed cancellation rates over 100%. This was corrected to use gross purchases only (positive-quantity rows) as the denominator, which is the mathematically correct approach and matches standard return-rate calculations.

## Python EDA — Key Steps

- Calculated monthly sales trend and total sales/cancellation figures
- Investigated and corrected the gross-vs-net cancellation rate issue described above
- Built full RFM (Recency, Frequency, Monetary) customer segmentation, scoring each customer 1–4 on each dimension using quartiles, then classifying into segments (Champions, Loyal Customers, Needs Attention, At Risk)
- Exported cleaned data and RFM segment table for use in Power BI

## Power BI Dashboard

**Page 1 — Sales Overview:** KPI cards (Total Sales, Total Cancellations, Cancellation Rate %), monthly sales trend line chart.

**Page 2 — Returns Analysis:** Cancellation Rate % by country (Top 10) and Total Cancellations by country (Top 10) — shown side by side to highlight that raw cancellation amount and cancellation rate tell very different stories.

**Page 3 — Customer Segmentation (RFM):** Total Revenue, Customer Count, and Average Revenue per customer, all broken down by RFM segment.

## Key Insights

- **November 2011 was the peak sales month (£1.46M)**, likely driven by Black Friday and the start of the Christmas shopping season. December 2011 shows the lowest figure (£433,668), but this is misleading — the dataset only covers the first 9 days of December, not the full month.
- **Cancellations represent 8.4% of gross sales** (£896,812 of roughly £10.64M in gross purchases) — a meaningful but not alarming share of revenue.
- **UK's cancellation rate (9.1%) is low and highly stable**, backed by ~495,000 transactions. Singapore (57.1%), USA (51.7%), and Hong Kong (35.5%) show much higher rates, but each is based on fewer than 300 transactions — worth flagging as a signal for investigation, not a confirmed trend, given the small sample sizes.
- **RFM segmentation reveals a small group of high-value customers drives most revenue.** Champions (608 customers, the smallest segment) generate £4.58M — more than the other three segments combined (£4.34M across 3,731 customers). Average spend per Champion (~£7,526) is nearly 15x that of an At Risk customer (~£510).
- **At Risk is the largest segment by customer count (1,504)** but contributes the least revenue — a natural target for re-engagement campaigns given the volume of customers involved.
- Approximately 25% of transactions have no CustomerID and were excluded from the RFM segmentation specifically (all other analyses use the full dataset).

## Tools Used

Python (Pandas) • Power BI Desktop • Power Query • DAX • RFM Customer Segmentation

## Files in this Repository

- `eda.py` — Python cleaning, analysis, and RFM segmentation script
- `E-Commerce_Dashboard.pbix` — Power BI dashboard
- `screenshots/` — dashboard page exports
- `README.md` — this file

Note: raw and cleaned dataset files are not included here due to size — the original dataset is linked above, and `eda.py` reproduces the cleaning and RFM segmentation output when run against it.
