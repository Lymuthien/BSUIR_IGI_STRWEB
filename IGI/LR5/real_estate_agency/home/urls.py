from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('news/', views.news, name='news'),
    path('faq/', views.faq, name='faq'),
    path('contacts/', views.contact, name='contacts'),
    path('promo-codes/', views.promo, name='promo-codes'),
    path('policy/', views.policy, name='policy'),
    path('vacancies/', views.vacancy, name='vacancies'),
    path('reviews/', views.review, name='reviews'),
]
