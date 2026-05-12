# 🛒 Sales Analytics System

A Python-based Sales Data Analytics System built as part of Module 3 of the Python Programming course. The system reads and cleans messy sales transaction data, validates records, performs multi-dimensional sales analysis, fetches product information from an external API, and generates a comprehensive business report.

---

## 📁 Repository Structure

```
sales-analytics-system/
├── README.md
├── main.py
├── requirements.txt
├── utils/
│   ├── file_handler.py
│   ├── data_processor.py
│   └── api_handler.py
├── data/
│   ├── sales_data.txt               ← raw input file (provided)
│   └── enriched_sales_data.txt      ← auto-generated on run
└── output/
    └── sales_report.txt             ← auto-generated on run
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Step 1: Clone the Repository
```bash
git clone https://github.com/sarbani-karmakar/sales-analytics-system.git
cd sales-analytics-system
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

`requirements.txt` contains:
```
requests
```

### Step 3: Ensure Data File is in Place
Make sure `sales_data.txt` is inside the `data/` folder before running.

---

## ▶️ How to Run

```bash
python main.py
```

---

## 🖥️ Expected Console Output

```
========================================
SALES ANALYTICS SYSTEM
========================================
[1/10] Reading sales data...
✓ Successfully read 80 transactions

[2/10] Parsing and cleaning data...
✓ Parsed 78 records

[3/10] Validating transactions...
Available Regions: East, North, South, West
Transaction Amount Range: 149.0 - 818960.0
✓ Valid: 71 | Invalid: 7

[4/10] Analyzing sales data...
✓ Analysis complete

[5/10] Fetching product data from API...
✓ Fetched 100 products from API

[6/10] Enriching sales data...
✓ Enriched 0/71 transactions

[7/10] Saving enriched data...
✓ Enriched data saved to data/enriched_sales_data.txt

[8/10] Generating report...
✓ Report generated at output/sales_report.txt

[9/10] Process Complete!
========================================
```

---

## 📊 What the Program Does — Step by Step

| Step | What Happens |
|------|-------------|
| File Reading | Reads `sales_data.txt`, trying `utf-8` → `latin-1` → `cp1252` encodings until one works |
| Data Cleaning | Splits each row by `\|`, removes commas from product names and prices, converts types |
| Validation | Removes rows with invalid IDs, zero/negative quantity or price, missing CustomerID/Region |
| Analysis | Revenue totals, region breakdown, top products, customer stats, daily trends, peak day |
| API Call | Fetches up to 100 products from DummyJSON API |
| Enrichment | Matches `P101 → 101` to API product IDs; adds category, brand, rating to each transaction |
| File Output | Saves enriched data to `data/enriched_sales_data.txt` |
| Report | Writes formatted report with 2 sections to `output/sales_report.txt` |

---

## 📂 File Descriptions

### `main.py`
The main entry point. Runs the full 9-step pipeline by calling functions from all three utility modules. Wrapped in a `try-except` block so the program never crashes unexpectedly.

### `utils/file_handler.py`

| Function | What it does |
|----------|-------------|
| `read_sales_data(filename)` | Opens the file trying multiple encodings; skips header and empty lines; returns a list of raw string lines |
| `parse_transactions(raw_lines)` | Splits each line by `\|`; cleans commas from product names and numeric fields; converts Quantity to `int` and UnitPrice to `float`; skips malformed rows |
| `validate_and_filter(transactions, region, min_amount, max_amount)` | Validates each transaction against 5 rules; optionally filters by region or amount range; returns `(valid_list, invalid_count, summary_dict)` |

### `utils/data_processor.py`

| Function | What it does |
|----------|-------------|
| `calculate_total_revenue(transactions)` | Sums `Quantity × UnitPrice` across all transactions |
| `region_wise_sales(transactions)` | Groups by region; calculates total sales, transaction count, and % of total; sorted by sales descending |
| `top_selling_products(transactions, n=5)` | Aggregates by product name; returns top N by total quantity as list of `(name, qty, revenue)` tuples |
| `customer_analysis(transactions)` | Per-customer: total spent, purchase count, average order value, unique products bought; sorted by spend descending |
| `daily_sales_trend(transactions)` | Groups by date; calculates daily revenue, transaction count, unique customers; sorted chronologically |
| `find_peak_sales_day(transactions)` | Returns `(date, revenue, transaction_count)` for the highest-revenue day |
| `low_performing_products(transactions, threshold=10)` | Finds products whose total quantity sold is below threshold; sorted ascending by quantity |

### `utils/api_handler.py`

| Function | What it does |
|----------|-------------|
| `fetch_all_products()` | Calls `https://dummyjson.com/products?limit=100`; returns list of product dicts; returns `[]` on failure |
| `create_product_mapping(api_products)` | Converts product list into a dict keyed by numeric product ID |
| `enrich_sales_data(transactions, product_mapping)` | Strips 'P' from ProductID to get numeric ID; looks up in mapping; adds `API_Category`, `API_Brand`, `API_Rating`, `API_Match` to each transaction |
| `save_enriched_data(enriched_transactions, filename)` | Writes enriched transactions to pipe-delimited file with 12-column header |

---

## 📋 Input Data Format

`sales_data.txt` is pipe-delimited (`|`) with ~80 records covering December 2024:

```
TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region
T001|2024-12-01|P102|Mouse|5|801|C008|South
T059|2024-12-29|P102|Mouse,Wireless|4|1056|C010|South
T063|2024-12-07|P110|Laptop Charger|6|1,916|C022|East
```

**Data quality issues handled:**
- Commas inside product names (e.g. `Mouse,Wireless`) → commas removed, kept as valid
- Commas in prices (e.g. `1,916`) → converted to `1916.0`
- Missing CustomerID or Region → row removed
- Zero or negative Quantity/UnitPrice → row removed
- TransactionID not starting with `T` (e.g. `X2`, `X611`) → row removed
- Rows with wrong number of fields → row skipped

---

## 📤 Output Files

### `data/enriched_sales_data.txt`
All valid transactions with 4 extra API columns:
```
TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match
T001|2024-12-01|P102|Mouse|5|801.0|C008|South||||False
```
> Note: `API_Match` is `False` for all records because the DummyJSON product IDs (1–100) do not match the assignment's ProductIDs (P101–P110 → 101–110).

### `output/sales_report.txt`
A formatted text report containing:
1. **Header** — title, generation timestamp, total records processed
2. **Overall Summary** — total revenue, transaction count, average order value, date range
3. **API Enrichment Summary** — enriched record count and success rate

---

## 🔗 External API

- **API:** [DummyJSON Products API](https://dummyjson.com/products)
- **Endpoint used:** `https://dummyjson.com/products?limit=100`
- **No API key required**
- Provides: product `id`, `title`, `category`, `brand`, `price`, `rating`

---

## 🧰 Technologies Used

- **Python 3.8+**
- **`requests`** — external API calls
- **Built-in:** `datetime`, `os`

---

## 👤 Author

Sarbani Karmakar  
[https://github.com/sarbani-karmakar/sales-analytics-system](https://github.com/your-username/sales-analytics-system)
