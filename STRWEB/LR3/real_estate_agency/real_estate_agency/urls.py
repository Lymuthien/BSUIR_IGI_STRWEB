"""
URL configuration for real_estate_agency project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic import RedirectView
from django.views.generic import TemplateView

# LR3 static-pages integration
lr3_patterns = [
    path('lr3/', TemplateView.as_view(template_name='lr3/index.html'), name='lr3_index'),
    path('lr3/formgen/', TemplateView.as_view(template_name='lr3/formgen.html'), name='lr3_formgen'),
    path('lr3/dates/', TemplateView.as_view(template_name='lr3/dates.html'), name='lr3_classes'),
    path('lr3/chart/', TemplateView.as_view(template_name='lr3/chart.html'), name='lr3_chart'),
]


urlpatterns = [
    path("admin/", admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('home/', include('home.urls')),
    path('accounts/', include('users.urls')),
    path('', RedirectView.as_view(url='/home/', permanent=True)),
]
urlpatterns += lr3_patterns

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)