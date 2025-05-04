from django.shortcuts import render

from .models import AboutCompany, FAQ, Vacancy, Contact, PromoCode, Policy, Review, News


def home(request):
    last_news = News.objects.first()

    return render(request, "home.html", {"last_news": last_news if last_news else None})


def about(request):
    about_info = AboutCompany.objects.first()

    return render(request, "about.html", {"about_info": about_info})


def news(request):
    news_list = News.objects.all()

    return render(request, "news.html", {"news_list": news_list})


def faq(request):
    faq_list = FAQ.objects.all()

    return render(request, "faq.html", {"faq_list": faq_list})


def contact(request):
    contacts = Contact.objects.all()

    return render(request, "contacts.html", {"contacts": contacts})


def promo(request):
    active_promos = PromoCode.objects.filter(status=True)
    archived_promos = PromoCode.objects.filter(status=False)

    return render(
        request,
        "promo-codes.html",
        {"active_promos": active_promos, "archived_promos": archived_promos},
    )
