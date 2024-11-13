from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView
# from dashboard.helpers import get_dashboard_data

class DashboardListView(TemplateView):
    template_name = 'dashboard/index.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
     #    context['data'] = get_dashboard_data(self.request.user)
        return context

