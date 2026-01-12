import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get('products', [])

        result = []
        for product in products:
            result.append({
                'id': product.get('id'),
                'title': product.get('title'),
                'category': product.get('category'),
                'brand': product.get('brand'),
                'price': product.get('price'),
                'rating': product.get('rating')
            })

        print(f"✓ Fetched {len(result)} products from API")
        return result

    except Exception as e:
        print("Error: Failed to fetch products from API")
        return []

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    Returns: dictionary
    """
    product_map = {}

    for product in api_products:
        product_id = product.get('id')
        if product_id is None:
            continue

        product_map[product_id] = {
            'title': product.get('title'),
            'category': product.get('category'),
            'brand': product.get('brand'),
            'rating': product.get('rating')
        }

    return product_map

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    Returns: list of enriched transactions
    """
    enriched = []

    for txn in transactions:
        enriched_txn = txn.copy()

        # extract numeric product id (P101 -> 101)
        product_id = txn.get('ProductID', '')
        try:
            numeric_id = int(product_id.replace('P', ''))
        except Exception:
            numeric_id = None

        if numeric_id and numeric_id in product_mapping:
            api_product = product_mapping[numeric_id]
            enriched_txn['API_Category'] = api_product.get('category')
            enriched_txn['API_Brand'] = api_product.get('brand')
            enriched_txn['API_Rating'] = api_product.get('rating')
            enriched_txn['API_Match'] = True
        else:
            enriched_txn['API_Category'] = None
            enriched_txn['API_Brand'] = None
            enriched_txn['API_Rating'] = None
            enriched_txn['API_Match'] = False

        enriched.append(enriched_txn)

    return enriched
    
def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file
    """
    if not enriched_transactions:
        print("No enriched data to save.")
        return

    headers = [
        'TransactionID', 'Date', 'ProductID', 'ProductName',
        'Quantity', 'UnitPrice', 'CustomerID', 'Region',
        'API_Category', 'API_Brand', 'API_Rating', 'API_Match'
    ]

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            # write header
            file.write('|'.join(headers) + '\n')

            # write rows
            for txn in enriched_transactions:
                row = []
                for key in headers:
                    value = txn.get(key)
                    if value is None:
                        value = ''
                    row.append(str(value))

                file.write('|'.join(row) + '\n')

        print(f"✓ Enriched data saved to {filename}")

    except Exception as e:
        print("Error: Failed to save enriched data")

