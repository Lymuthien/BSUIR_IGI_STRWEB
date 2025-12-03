from django.urls import re_path, path
from . import views


urlpatterns = [
    re_path(r'^$', views.AvailableEstateListView.as_view(), name='estates'),
    re_path(r'^services/$', views.ServiceListView.as_view(), name='services'),
    re_path(r'^estate/(?P<pk>\d+)/$', views.EstateDetailView.as_view(), name='estate_detail'),
    re_path(r'^estate/(?P<pk>\d+)/request/$', views.CreatePurchaseRequestView.as_view(), name='create_request'),
    re_path(r'^client-dashboard/$', views.ClientDashboardView.as_view(), name='client_dashboard'),
    re_path(r'^employee-dashboard/$', views.EmployeeDashboardView.as_view(), name='employee_dashboard'),
    re_path(r'^statistics/$', views.StatisticsView.as_view(), name='statistics'),
    path('estate/create/', views.EstateCreateView.as_view(), name='estate_create'),
    path('estate/<int:pk>/update/', views.EstateUpdateView.as_view(), name='estate_update'),
    path('estate/<int:pk>/delete/', views.EstateDeleteView.as_view(), name='estate_delete'),
    path("payment/<int:sale_id>/", views.PaymentView.as_view(), name="payment"),
]