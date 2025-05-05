from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import AboutCompany, FAQ, Vacancy, Contact, PromoCode, Review, News, Policy
from .forms import ReviewForm


class HomeView(ListView):
    template_name = "home.html"
    context_object_name = "last_news"

    def get_queryset(self):
        return News.objects.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_news"] = self.get_queryset()
        return context


class AboutView(ListView):
    model = AboutCompany
    template_name = "about.html"
    context_object_name = "about_info"

    def get_queryset(self):
        return AboutCompany.objects.first()


class NewsListView(ListView):
    model = News
    template_name = "news_list.html"
    paginate_by = 9


class FAQListView(ListView):
    model = FAQ
    template_name = "faq_list.html"


class ContactListView(ListView):
    model = Contact
    template_name = "contact_list.html"


class PolicyView(ListView):
    model = Policy
    template_name = "policy.html"


class VacancyListView(ListView):
    model = Vacancy
    template_name = "vacancy_list.html"


class PromoCodeView(ListView):
    model = PromoCode
    template_name = "promo-codes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_promos"] = PromoCode.objects.filter(status=True)
        context["archived_promos"] = PromoCode.objects.filter(status=False)
        return context


class ReviewListView(ListView):
    model = Review
    template_name = "review_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReviewForm()
        return context


class AddReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "review_add.html"
    success_url = reverse_lazy("reviews")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditReviewView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "review_edit.html"
    success_url = reverse_lazy("reviews")

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.updated_at = timezone.now()
        return super().form_valid(form)


class DeleteReviewView(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = reverse_lazy("reviews")

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
