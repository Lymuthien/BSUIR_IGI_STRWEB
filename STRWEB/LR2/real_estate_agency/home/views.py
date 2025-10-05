import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView, DetailView,
)

from .forms import ReviewForm
from .models import AboutCompany, FAQ, Vacancy, Contact, PromoCode, Review, News, Policy, Partner
from catalog.models import ServiceCategory

logger = logging.getLogger(__name__)


class HomeView(ListView):
    template_name = "home.html"
    context_object_name = "last_news"

    def get_queryset(self):
        logger.debug("Fetching latest news")
        news = News.objects.first()
        partner_companies = Partner.objects.all()
        categories = ServiceCategory.objects.all()
        if not news:
            logger.warning("No news found")
        return news, partner_companies, categories

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news, partner_companies, categories = self.get_queryset()
        context["last_news"] = news
        context["partner_companies"] = partner_companies
        context["categories"] = categories
        logger.debug("Prepared context for HomeView")
        return context


class AboutView(ListView):
    model = AboutCompany
    template_name = "about.html"
    context_object_name = "about_info"

    def get_queryset(self):
        logger.debug("Fetching AboutCompany info")
        about = AboutCompany.objects.first()
        if not about:
            logger.warning("No AboutCompany info found")
        return about


class NewsListView(ListView):
    model = News
    template_name = "news_list.html"
    paginate_by = 9

    def get_queryset(self):
        return super().get_queryset().order_by("-created")

class NewsView(DetailView):
    model = News
    template_name = "news_detail.html"
    context_object_name = "news"

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
        logger.debug(f"Prepared promo codes: {context['active_promos'].count()} active, {context['archived_promos'].count()} archived")
        return context


class ReviewListView(ListView):
    model = Review
    template_name = "review_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReviewForm()
        logger.debug(f"Prepared Review list, page: {self.request.GET.get('page', 1)}")
        return context


class AddReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "review_add.html"
    success_url = reverse_lazy("reviews")

    def form_valid(self, form):
        logger.debug(f"User {self.request.user.username} adding review")
        try:
            form.instance.user = self.request.user
            response = super().form_valid(form)
            logger.info(f"User {self.request.user.username} added review ID: {form.instance.id}")
            return response
        except Exception:
            logger.exception(f"Error adding review by {self.request.user.username}")
            raise


class UpdateReviewView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "review_edit.html"
    success_url = reverse_lazy("reviews")

    def get_queryset(self):
        logger.debug(f"User {self.request.user.username} fetching review for edit")
        return Review.objects.filter(user=self.request.user)

    def form_valid(self, form):
        logger.debug(f"User {self.request.user.username} editing review ID: {self.object.id}")
        try:
            form.instance.updated_at = timezone.now()
            response = super().form_valid(form)
            logger.info(f"User {self.request.user.username} updated review ID: {self.object.id}")
            return response
        except Exception:
            logger.exception(f"Error updating review ID: {self.object.id} by {self.request.user.username}")
            raise


class DeleteReviewView(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = reverse_lazy("reviews")

    def get_queryset(self):
        logger.debug(f"User {self.request.user.username} fetching review for delete")
        return Review.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        logger.debug(f"User {request.user.username} deleting review ID: {self.object.id}")
        try:
            response = super().delete(request, *args, **kwargs)
            logger.info(f"User {request.user.username} deleted review ID: {self.object.id}")
            return response
        except Exception:
            logger.exception(f"Error deleting review ID: {self.object.id} by {request.user.username}")
            raise

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
