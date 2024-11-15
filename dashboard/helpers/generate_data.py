import random
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from dashboard.models import Receipt, ReceiptItem

# Random data for store names and addresses
STORE_NAMES = ["SuperMart", "QuickShop", "Grocery World", "Retailer X", "Daily Needs"]
STORE_ADDRESSES = [
    "123 Main Street",
    "456 Market Road",
    "789 Broadway",
    "101 Elm Street",
    "202 Maple Avenue"
]

CATEGORIES = ["Snacks", "Drinks", "Groceries", "Household", "Electronics"]

def generate_random_date():
    """Generate a random datetime for the current year."""
    start_date = datetime(datetime.now().year, 1, 1)  # Start of the year
    end_date = datetime(datetime.now().year, 12, 31)  # End of the year
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return make_aware(random_date)

def generate_receipts(num_receipts=100):
    """Generate random receipts with random items."""
    for _ in range(num_receipts):
        # Create a random receipt
        receipt = Receipt.objects.create(
            store_name=random.choice(STORE_NAMES),
            store_address=random.choice(STORE_ADDRESSES),
            store_postcode=str(random.randint(10000, 99999)),
            transaction_date=generate_random_date(),
            check_number=str(random.randint(1000, 9999)),
            payment_type=random.choice(['Card', 'Cash', 'Other']),
            card_last_four_digits=str(random.randint(1000, 9999)) if random.choice([True, False]) else None,
            change_due=random.uniform(0, 10),
            vat_amount=None,  # You can calculate this based on items if needed
            vat_percentage=None,  # You can calculate this based on items if needed
        )

        # Generate random receipt items
        num_items = random.randint(1, 5)  # Each receipt will have 1-5 items
        for _ in range(num_items):
            price = round(random.uniform(1.0, 100.0), 2)
            quantity = random.randint(1, 5)
            ReceiptItem.objects.create(
                receipt=receipt,
                description=f"Item {random.randint(1, 100)}",
                quantity=quantity,
                price=price,
                total_price=round(price * quantity, 2),
                category=random.choice(CATEGORIES)
            )

        # Optionally calculate VAT based on receipt items and save
        total = sum(item.total_price for item in receipt.items.all())
        receipt.payment_total = total
        receipt.vat_percentage = 15.00  # Example: 15% VAT
        receipt.vat_amount = round(float(total) * receipt.vat_percentage / 100, 2)
        receipt.save()

# Generate 100 random receipts

