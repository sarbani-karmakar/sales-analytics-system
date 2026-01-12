from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)

from datetime import datetime


def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report
    """
    total_transactions = len(transactions)

    # overall calculations
    total_revenue = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = [t['Date'] for t in transactions]
    start_date = min(dates) if dates else ''
    end_date = max(dates) if dates else ''

    # API enrichment summary
    enriched_count = sum(1 for t in enriched_transactions if t.get('API_Match'))
    success_rate = (enriched_count / len(enriched_transactions) * 100) if enriched_transactions else 0

    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("=" * 44 + "\n")
            file.write("           SALES ANALYTICS REPORT\n")
            file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"Records Processed: {total_transactions}\n")
            file.write("=" * 44 + "\n\n")

            file.write("OVERALL SUMMARY\n")
            file.write("-" * 44 + "\n")
            file.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
            file.write(f"Total Transactions:   {total_transactions}\n")
            file.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
            file.write(f"Date Range:           {start_date} to {end_date}\n\n")

            file.write("API ENRICHMENT SUMMARY\n")
            file.write("-" * 44 + "\n")
            file.write(f"Total Enriched Records: {enriched_count}\n")
            file.write(f"Success Rate: {success_rate:.2f}%\n")

        print(f"✓ Report generated at {output_file}")

    except Exception:
        print("Error: Failed to generate report")

def main():
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        print("[1/10] Reading sales data...")
        raw_lines = read_sales_data('data/sales_data.txt')
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        print("[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")

        print("[3/10] Validating transactions...")
        valid_transactions, invalid_count, summary = validate_and_filter(transactions)
        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")

        print("[4/10] Analyzing sales data...")
        total_revenue = calculate_total_revenue(valid_transactions)
        region_stats = region_wise_sales(valid_transactions)
        top_products = top_selling_products(valid_transactions)
        customer_stats = customer_analysis(valid_transactions)
        daily_trend = daily_sales_trend(valid_transactions)
        peak_day = find_peak_sales_day(valid_transactions)
        low_products = low_performing_products(valid_transactions)
        print("✓ Analysis complete")

        print("[5/10] Fetching product data from API...")
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)

        print("[6/10] Enriching sales data...")
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
        enriched_count = sum(1 for t in enriched_transactions if t.get('API_Match'))
        print(f"✓ Enriched {enriched_count}/{len(enriched_transactions)} transactions")

        print("[7/10] Saving enriched data...")
        save_enriched_data(enriched_transactions)

        print("[8/10] Generating report...")
        generate_sales_report(valid_transactions, enriched_transactions)

        print("[9/10] Process complete!")
        print("=" * 40)

    except Exception as e:
        print("Unexpected error occurred:", str(e))

if __name__ == "__main__":
    main()
