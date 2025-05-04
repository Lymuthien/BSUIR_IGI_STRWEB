from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('news/', views.NewsListView.as_view(), name='news'),
    path('faq/', views.FAQListView.as_view(), name='faq'),
    path('contacts/', views.ContactListView.as_view(), name='contacts'),
    path('promo-codes/', views.PromoCodeView.as_view(), name='promo-codes'),
    path('policy/', views.PolicyView.as_view(), name='policy'),
    path('vacancies/', views.VacancyListView.as_view(), name='vacancies'),
    path('reviews/', views.ReviewListView.as_view(), name='reviews'),
    path('reviews/add/', views.AddReviewView.as_view(), name='add_review'),
    path('reviews/edit/<int:pk>/', views.EditReviewView.as_view(), name='edit_review'),
    path('reviews/delete/<int:pk>/', views.DeleteReviewView.as_view(), name='delete_review'),
]
