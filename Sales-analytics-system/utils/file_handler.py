def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw lines (strings)
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()

            # remove header and empty lines
            clean_lines = []
            for line in lines[1:]:
                line = line.strip()
                if line:
                    clean_lines.append(line)

            return clean_lines

        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    print("Error: Unable to read file with supported encodings.")
    return []

def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    Returns: list of dictionaries
    """
    transactions = []

    for line in raw_lines:
        parts = line.split('|')

        # skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = parts

        # clean product name
        product_name = product_name.replace(',', '').strip()

        # clean numeric fields
        try:
            quantity = int(quantity.replace(',', '').strip())
            unit_price = float(unit_price.replace(',', '').strip())
        except ValueError:
            continue

        transaction = {
            'TransactionID': transaction_id.strip(),
            'Date': date.strip(),
            'ProductID': product_id.strip(),
            'ProductName': product_name,
            'Quantity': quantity,
            'UnitPrice': unit_price,
            'CustomerID': customer_id.strip(),
            'Region': region.strip()
        }

        transactions.append(transaction)

    return transactions
    
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    Returns: (valid_transactions, invalid_count, summary)
    """
    valid_transactions = []
    invalid_count = 0

    # collect available regions and amount range
    regions = set()
    amounts = []

    for txn in transactions:
        try:
            # validation rules
            if txn['Quantity'] <= 0:
                raise ValueError
            if txn['UnitPrice'] <= 0:
                raise ValueError
            if not txn['TransactionID'].startswith('T'):
                raise ValueError
            if not txn['ProductID'].startswith('P'):
                raise ValueError
            if not txn['CustomerID'].startswith('C'):
                raise ValueError

            amount = txn['Quantity'] * txn['UnitPrice']
            regions.add(txn['Region'])
            amounts.append(amount)

            valid_transactions.append(txn)

        except Exception:
            invalid_count += 1

    # display filter options
    if amounts:
        print("Available Regions:", ', '.join(sorted(regions)))
        print(f"Transaction Amount Range: {min(amounts)} - {max(amounts)}")

    # apply filters
    filtered = valid_transactions

    if region:
        filtered = [t for t in filtered if t['Region'] == region]

    if min_amount is not None:
        filtered = [t for t in filtered if t['Quantity'] * t['UnitPrice'] >= min_amount]

    if max_amount is not None:
        filtered = [t for t in filtered if t['Quantity'] * t['UnitPrice'] <= max_amount]

    summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'final_count': len(filtered)
    }

    return filtered, invalid_count, summary

