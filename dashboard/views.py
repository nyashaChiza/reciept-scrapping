from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from dashboard.models import Receipt
from dashboard.helpers import get_monthly_sales, get_payment_type_percentages

class DashboardListView(TemplateView):
    template_name = 'dashboard/index.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        # Get the year from the GET request, default to the current year if not provided
        year = self.request.GET.get('year', timezone.now().year)
        
        # Convert year to integer
        year = int(year)
        
        # Get the totals for each payment type
        context['card_total'] = sum(receipt.get_total() for receipt in Receipt.objects.filter(payment_type='Card', transaction_date__year=year))
        context['cash_total'] = sum(receipt.get_total() for receipt in Receipt.objects.filter(payment_type='Cash', transaction_date__year=year))
        context['other_total'] = sum(receipt.get_total() for receipt in Receipt.objects.filter(payment_type='Other', transaction_date__year=year))
        
        # Get the latest receipts (you can adjust this as needed)
        context['receipts'] = Receipt.objects.filter(transaction_date__year=year)[:5]
        
        # Get the graph data
        context['graph_x_values'] = list(get_monthly_sales(year).values())
        context['graph_y_values'] = list(get_monthly_sales(year).keys())
        
        # Get the donut chart data for payment type percentages
        context['donut_values'] = get_payment_type_percentages(year)
        
        # Pass the selected year to the template
        context['selected_year'] = year
        
        return context
