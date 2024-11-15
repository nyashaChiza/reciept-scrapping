from collections import defaultdict
from django.db.models import Count
from dashboard.models import Receipt

def get_monthly_sales(year):
    """
    Get monthly sales totals filtered by the given year.

    Args:
        year (int): The year to filter receipts by.

    Returns:
        dict: A dictionary where keys are month names (e.g., 'Jan') and values are total sales for that month.
    """
    # Fetch receipts for the specified year
    receipts = Receipt.objects.filter(transaction_date__year=year)

    # Dictionary to store monthly totals
    monthly_totals = defaultdict(float)

    for receipt in receipts:
        if receipt.transaction_date:
            # Extract the month name (e.g., "Oct") from transaction_date
            month = receipt.transaction_date.strftime('%b')
            
            # Add the calculated total to the monthly total
            monthly_totals[month] += float(receipt.get_total())

    # Convert defaultdict to a standard dictionary
    sales_dict = dict(monthly_totals)

    return sales_dict


def get_payment_type_percentages(year):
    """
    Get percentages of payment types filtered by the given year.

    Args:
        year (int): The year to filter receipts by.

    Returns:
        list: A list of percentages corresponding to each payment type.
    """
    # Get total number of receipts for the specified year
    total_receipts = Receipt.objects.filter(transaction_date__year=year).count()

    if total_receipts == 0:
        return []

    # Count receipts by payment type for the specified year
    payment_type_counts = (
        Receipt.objects.filter(transaction_date__year=year)
        .values('payment_type')
        .annotate(count=Count('payment_type'))
    )

    # Calculate percentages
    percentages = [
        round((entry['count'] / total_receipts) * 100, 2) for entry in payment_type_counts
    ]

    return percentages
