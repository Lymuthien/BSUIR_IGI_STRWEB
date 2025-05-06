from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^services/$', views.CategoryListView.as_view(), name='services'),

]