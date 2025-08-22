from django.contrib.auth.views import LoginView, LogoutView
from django.urls import re_path, path

from . import views, views_admin


urlpatterns = [
    re_path(r'^login/$', LoginView.as_view(template_name='login.html'), name='login'),
    re_path(r'^logout/$', LogoutView.as_view(next_page='home'), name='logout'),
    re_path(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    re_path(r'^profile/(?P<pk>\d+)$', views.ProfileView.as_view(), name='profile'),
]

urlpatterns += [
    # существующие маршруты
    path('admin/clients/', views_admin.AdminClientListView.as_view(), name='admin_clients'),
    path('admin/employees/', views_admin.AdminEmployeeListView.as_view(), name='admin_employees'),
    path('admin/client/<int:pk>/edit/', views_admin.AdminClientUpdateView.as_view(), name='admin_client_edit'),
    path('admin/employee/<int:pk>/edit/', views_admin.AdminEmployeeUpdateView.as_view(), name='admin_employee_edit'),
    path('admin/employee/create/', views_admin.AdminEmployeeCreateView.as_view(), name='admin_employee_create'),
    path('admin/employee/<int:pk>/delete/', views_admin.AdminEmployeeDeleteView.as_view(), name='admin_employee_delete'),
    path('admin/client/<int:pk>/toggle-status/', views_admin.toggle_client_status, name='admin_toggle_client_status'),
]

