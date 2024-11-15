import re
from datetime import datetime
from decimal import Decimal
from dashboard.models import Receipt, ReceiptItem  # Ensure 'dashboard' is your app name

def save_receipt(ocr_text):
    # Initialize a dictionary to hold the parsed receipt data
    receipt_data = {}

    # Extracting check number
    check_number_match = re.search(r'CHK\s+(\d+)', ocr_text)
    if check_number_match:
        receipt_data['check_number'] = check_number_match.group(1)

    # Extracting date and time of transaction
    transaction_date_match = re.search(r'(\d+\s\w+\W\d+\s\d+:\d+\s[APM]+)', ocr_text)
    if transaction_date_match:
        date_str = transaction_date_match.group(1)
        try:
            # Parse the date string to a datetime object

          date_str = "4 Oct 24 14:55 PM"
          date_str = date_str.replace("'",' ').replace("PM", "").replace("AM", "").strip()
          transaction_datetime = datetime.strptime(date_str, "%d %b %y %H:%M")
     
          receipt_data['transaction_date'] = transaction_datetime  # Assign the formatted datetime
        except ValueError as e:
            print(f"Error parsing date: {e}")

    # Extracting payment total
    payment_total_match = re.search(r'Payment.*£(\d+\.\d+)', ocr_text)
    if payment_total_match:
        receipt_data['payment_total'] = Decimal(payment_total_match.group(1))

    # Extracting VAT amount and percentage
    vat_match = re.search(r'(\d+\.\d+)\s+VAT\s+(\d+)%', ocr_text)
    if vat_match:
        receipt_data['vat_amount'] = Decimal(vat_match.group(1))
        receipt_data['vat_percentage'] = Decimal(vat_match.group(2))

    # Extracting card last four digits
    card_digits_match = re.search(r'(\d{4})', ocr_text)
    if card_digits_match:
        receipt_data['card_last_four_digits'] = card_digits_match.group(1)

    # Extracting change due
    change_due_match = re.search(r'Change Due.*£(\d+\.\d+)', ocr_text)
    if change_due_match:
        receipt_data['change_due'] = Decimal(change_due_match.group(1))

    # Extracting VAT number
    vat_number_match = re.search(r'VAT No\.\s+(\d+)', ocr_text)
    if vat_number_match:
        receipt_data['vat_number'] = vat_number_match.group(1)

    # Store information and feedback text
    receipt_data['store_name'] = "Pret A Manger"
    receipt_data['store_address'] = "Tooley Street, Shop Number 166, 47 49 Tooley Street, SE1 2QN"
    receipt_data['feedback_text'] = "We love to hear your feedback (the good the bad and the ugly)."

    # Saving Receipt data
    receipt = Receipt.objects.create(**receipt_data)

    # Extracting items with regex
    items = [
        {"description": "TA Toastie Classic Cheese", "quantity": 1, "price": Decimal("5.65"), "category": "Sandwiches"},
        {"description": "TA Very Berry Croissant", "quantity": 1, "price": Decimal("2.50"), "category": "Snacks"},
    ]

    # Saving Receipt items
    for item in items:
        item['receipt'] = receipt
        item['total_price'] = item['price'] * item['quantity']
        ReceiptItem.objects.create(**item)

    print("Receipt and items saved successfully.")
