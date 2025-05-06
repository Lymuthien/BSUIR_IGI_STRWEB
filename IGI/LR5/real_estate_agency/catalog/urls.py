from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.AvailableEstateListView.as_view(), name='estates'),
    re_path(r'^services/$', views.ServiceListView.as_view(), name='services'),
]