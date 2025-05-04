from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import AboutCompany, FAQ, Vacancy, Contact, PromoCode, Review, News
from .forms import ReviewForm


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


def policy(request):
    return render(request, "policy.html")


def vacancy(request):
    vacancies = Vacancy.objects.all()

    return render(
        request,
        "vacancies.html",
        {"vacancies": vacancies},
    )

def review(request):
    reviews = Review.objects.all()

    return render(request, "reviews.html", {"reviews": reviews, "user": request.user, "form": ReviewForm()})


@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form_review = form.save(commit=False)
            form_review.user = request.user
            form_review.date = timezone.now()
            form_review.save()
            return redirect('reviews')
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'form': form,})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('reviews')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'edit_review.html', {'form': form, 'review': review})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        review.delete()

    return redirect('reviews')
