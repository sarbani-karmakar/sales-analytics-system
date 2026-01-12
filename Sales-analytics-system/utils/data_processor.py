def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    Returns: float
    """
    total_revenue = 0.0

    for txn in transactions:
        total_revenue += txn['Quantity'] * txn['UnitPrice']

    return total_revenue
    
def region_wise_sales(transactions):
    """
    Analyzes sales by region
    Returns: dictionary with region statistics
    """
    region_data = {}
    total_sales = 0.0

    # calculate totals
    for txn in transactions:
        region = txn['Region']
        amount = txn['Quantity'] * txn['UnitPrice']
        total_sales += amount

        if region not in region_data:
            region_data[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }

        region_data[region]['total_sales'] += amount
        region_data[region]['transaction_count'] += 1

    # calculate percentages
    for region in region_data:
        if total_sales > 0:
            percentage = (region_data[region]['total_sales'] / total_sales) * 100
        else:
            percentage = 0

        region_data[region]['percentage'] = round(percentage, 2)

    # sort by total_sales descending
    sorted_regions = dict(
        sorted(
            region_data.items(),
            key=lambda item: item[1]['total_sales'],
            reverse=True
        )
    )

    return sorted_regions

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    Returns: list of tuples
    """
    product_data = {}

    for txn in transactions:
        product = txn['ProductName']
        quantity = txn['Quantity']
        revenue = txn['Quantity'] * txn['UnitPrice']

        if product not in product_data:
            product_data[product] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }

        product_data[product]['total_quantity'] += quantity
        product_data[product]['total_revenue'] += revenue

    # sort by total quantity descending
    sorted_products = sorted(
        product_data.items(),
        key=lambda item: item[1]['total_quantity'],
        reverse=True
    )

    # prepare result
    result = []
    for product, data in sorted_products[:n]:
        result.append(
            (product, data['total_quantity'], data['total_revenue'])
        )

    return result

def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    Returns: dictionary of customer statistics
    """
    customer_data = {}

    for txn in transactions:
        customer = txn['CustomerID']
        amount = txn['Quantity'] * txn['UnitPrice']
        product = txn['ProductName']

        if customer not in customer_data:
            customer_data[customer] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set()
            }

        customer_data[customer]['total_spent'] += amount
        customer_data[customer]['purchase_count'] += 1
        customer_data[customer]['products_bought'].add(product)

    # calculate average order value and convert set to list
    for customer in customer_data:
        purchases = customer_data[customer]['purchase_count']
        if purchases > 0:
            avg_value = customer_data[customer]['total_spent'] / purchases
        else:
            avg_value = 0

        customer_data[customer]['avg_order_value'] = round(avg_value, 2)
        customer_data[customer]['products_bought'] = list(
            customer_data[customer]['products_bought']
        )

    # sort by total_spent descending
    sorted_customers = dict(
        sorted(
            customer_data.items(),
            key=lambda item: item[1]['total_spent'],
            reverse=True
        )
    )

    return sorted_customers

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    Returns: dictionary sorted by date
    """
    daily_data = {}

    for txn in transactions:
        date = txn['Date']
        amount = txn['Quantity'] * txn['UnitPrice']
        customer = txn['CustomerID']

        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'customers': set()
            }

        daily_data[date]['revenue'] += amount
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['customers'].add(customer)

    # prepare final structure
    result = {}
    for date in sorted(daily_data.keys()):
        result[date] = {
            'revenue': daily_data[date]['revenue'],
            'transaction_count': daily_data[date]['transaction_count'],
            'unique_customers': len(daily_data[date]['customers'])
        }

    return result

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    Returns: tuple (date, revenue, transaction_count)
    """
    daily_totals = {}

    for txn in transactions:
        date = txn['Date']
        amount = txn['Quantity'] * txn['UnitPrice']

        if date not in daily_totals:
            daily_totals[date] = {
                'revenue': 0.0,
                'transaction_count': 0
            }

        daily_totals[date]['revenue'] += amount
        daily_totals[date]['transaction_count'] += 1

    peak_date = None
    peak_revenue = 0.0
    peak_count = 0

    for date, data in daily_totals.items():
        if data['revenue'] > peak_revenue:
            peak_revenue = data['revenue']
            peak_date = date
            peak_count = data['transaction_count']

    return peak_date, peak_revenue, peak_count

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    Returns: list of tuples
    """
    product_data = {}

    for txn in transactions:
        product = txn['ProductName']
        quantity = txn['Quantity']
        revenue = txn['Quantity'] * txn['UnitPrice']

        if product not in product_data:
            product_data[product] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }

        product_data[product]['total_quantity'] += quantity
        product_data[product]['total_revenue'] += revenue

    # filter low performing products
    low_products = []
    for product, data in product_data.items():
        if data['total_quantity'] < threshold:
            low_products.append(
                (product, data['total_quantity'], data['total_revenue'])
            )

    # sort by total quantity ascending
    low_products.sort(key=lambda item: item[1])

    return low_products

