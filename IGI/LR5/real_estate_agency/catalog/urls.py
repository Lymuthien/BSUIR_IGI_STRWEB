from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.AvailableEstateListView.as_view(), name='estates'),
    re_path(r'^services/$', views.ServiceListView.as_view(), name='services'),
    re_path(r'^estate/(?P<pk>\d+)/$', views.EstateDetailView.as_view(), name='estate_detail'),
    re_path(r'^estate/(?P<pk>\d+)/request/$', views.CreatePurchaseRequestView.as_view(), name='create_request'),
    re_path(r'^client-dashboard/$', views.ClientDashboardView.as_view(), name='client_dashboard'),
    re_path(r'^employee-dashboard/$', views.EmployeeDashboardView.as_view(), name='employee_dashboard'),
]