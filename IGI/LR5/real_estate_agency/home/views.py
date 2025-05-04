from django.shortcuts import render

from .models import AboutCompany, FAQ, Vacancy, Contact, PromoCode, Policy, Review, News


def home(request):
    last_news = News.objects.first()

    return render(
        request, "home.html", {"last_news": last_news if last_news else None}
    )
