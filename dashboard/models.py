from django.db import models

class Receipt(models.Model):
    # Basic receipt information
    store_name = models.CharField(max_length=100, blank=True, null=True)
    store_address = models.CharField(max_length=255, blank=True, null=True)
    store_postcode = models.CharField(max_length=20, blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    
    # Transaction details
    check_number = models.CharField(max_length=20, blank=True, null=True)
    card_type = models.CharField(max_length=20, blank=True, null=True)  # e.g., "Visa", "MasterCard"
    card_last_four_digits = models.CharField(max_length=4, blank=True, null=True)
    payment_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    change_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    # VAT and other charges
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vat_percentage = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    # Optional fields for additional metadata
    feedback_text = models.TextField(blank=True, null=True)
    vat_number = models.CharField(max_length=50, blank=True, null=True)  # e.g., VAT No. 927137420

    # Timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



class ReceiptItem(models.Model):
     # Linking each item to its receipt
     receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='items')

     # Item details
     description = models.CharField(max_length=255)  # e.g., "TA Toastie Classic Cheese"
     quantity = models.IntegerField(default=1)
     price = models.DecimalField(max_digits=10, decimal_places=2)  # price per item
     total_price = models.DecimalField(max_digits=10, decimal_places=2)  # quantity * price

    # Optional categorization, e.g., "Sandwiches" or "Snacks"
     category = models.CharField(max_length=50, blank=True, null=True)
     created = models.DateTimeField(auto_now_add=True)
     updated = models.DateTimeField(auto_now=True)



