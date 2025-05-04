from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, re_path

from . import views


urlpatterns = [
    re_path(r'^login/$', LoginView.as_view(template_name='login.html'), name='login'),
    re_path(r'^logout/$', LogoutView.as_view(next_page='home'), name='logout'),
    re_path(r'^signup/$', views.SignUpView.as_view(), name='signup'),
]
