from django.contrib import admin
from .models import Receipt, ReceiptItem

class ReceiptItemInline(admin.TabularInline):
    model = ReceiptItem
    extra = 1  # Number of empty fields to display for new ReceiptItems
    readonly_fields = ('total_price',)
    fields = ('description', 'category', 'quantity', 'price', 'total_price')

    def total_price(self, obj):
        return obj.quantity * obj.price
    total_price.short_description = 'Total Price'

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'transaction_date', 'payment_total', 'vat_amount', 'created', 'updated')
    list_filter = ('transaction_date', 'store_name', 'card_type')
    search_fields = ('store_name', 'store_address', 'check_number', 'vat_number')
    readonly_fields = ('created', 'updated')
    inlines = [ReceiptItemInline]

    fieldsets = (
        ('Store Information', {
            'fields': ('store_name', 'store_address', 'store_postcode')
        }),
        ('Transaction Details', {
            'fields': ('transaction_date', 'check_number', 'card_type', 'card_last_four_digits', 'payment_total', 'change_due')
        }),
        ('VAT Information', {
            'fields': ('vat_amount', 'vat_percentage', 'vat_number')
        }),
        ('Additional Information', {
            'fields': ('feedback_text',)
        }),
        ('Timestamps', {
            'fields': ('created', 'updated')
        }),
    )

@admin.register(ReceiptItem)
class ReceiptItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'quantity', 'price', 'total_price', 'category', 'receipt')
    list_filter = ('category',)
    search_fields = ('description',)
    readonly_fields = ('total_price', 'created', 'updated')

    def total_price(self, obj):
        return obj.quantity * obj.price
    total_price.short_description = 'Total Price'
