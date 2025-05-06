from django.views.generic import ListView
from .models import ServiceCategory, Service


class ServiceListView(ListView):
    model = Service
    template_name = "service_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        service_category = self.request.GET.get('service_category')
        if service_category:
            queryset = queryset.filter(category_id=service_category)

        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if min_price:
            queryset = queryset.filter(cost__gte=min_price)
        if max_price:
            queryset = queryset.filter(cost__lte=max_price)

        return queryset.select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_categories'] = ServiceCategory.objects.all()
        return context
