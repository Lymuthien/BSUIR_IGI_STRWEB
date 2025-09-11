from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.HomeView.as_view(), name='home'),
    re_path(r'^about/$', views.AboutView.as_view(), name='about'),
    re_path(r'^news/$', views.NewsListView.as_view(), name='news'),
    re_path(r'^faq/$', views.FAQListView.as_view(), name='faq'),
    re_path(r'^contacts/$', views.ContactListView.as_view(), name='contacts'),
    re_path(r'^promo-codes/$', views.PromoCodeView.as_view(), name='promo-codes'),
    re_path(r'^policy/$', views.PolicyView.as_view(), name='policy'),
    re_path(r'^vacancies/$', views.VacancyListView.as_view(), name='vacancies'),
    re_path(r'^reviews/$', views.ReviewListView.as_view(), name='reviews'),
    re_path(r'^reviews/add/$', views.AddReviewView.as_view(), name='add_review'),
    re_path(r'^reviews/edit/(?P<pk>\d+)$', views.UpdateReviewView.as_view(), name='edit_review'),
    re_path(r'^reviews/delete/(?P<pk>\d+)$', views.DeleteReviewView.as_view(), name='delete_review'),
    re_path(r'^news_detail/(?P<pk>\d+)$', views.NewsView.as_view(), name='news_detail'),
]
