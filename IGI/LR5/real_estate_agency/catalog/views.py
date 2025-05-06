import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from users.models import Client

from .forms import PurchaseRequestForm
from .models import ServiceCategory, Service, Estate, Sale, PurchaseRequest

logger = logging.getLogger(__name__)


class ServiceListView(ListView):
    model = Service
    template_name = "service_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        service_category = self.request.GET.get("service_category")
        if service_category:
            queryset = queryset.filter(category_id=service_category)

        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")

        if min_price:
            queryset = queryset.filter(cost__gte=min_price)
        if max_price:
            queryset = queryset.filter(cost__lte=max_price)

        return queryset.select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["service_categories"] = ServiceCategory.objects.all()
        return context


class AvailableEstateListView(ListView):
    model = Estate
    template_name = "estate_list.html"
    paginate_by = 9
    ordering = "-cost"

    def get_queryset(self):
        sold_estates_ids = Sale.objects.all().values_list("estate_id", flat=True)
        queryset = Estate.objects.exclude(id__in=sold_estates_ids).select_related(
            "category"
        )

        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(address__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(category__name__icontains=search_query)
            )

        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        service_category_id = self.request.GET.get("service_category")
        if service_category_id:
            queryset = queryset.filter(category__category_id=service_category_id)

        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        if min_price:
            queryset = queryset.filter(cost__gte=min_price)
        if max_price:
            queryset = queryset.filter(cost__lte=max_price)

        sort = self.request.GET.get("sort")
        if sort:
            if sort == "price_asc":
                queryset = queryset.order_by("cost")
            elif sort == "price_desc":
                queryset = queryset.order_by("-cost")
            elif sort == "area_asc":
                queryset = queryset.order_by("area")
            elif sort == "area_desc":
                queryset = queryset.order_by("-area")
        else:
            queryset = queryset.order_by(self.ordering)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Service.objects.all()
        context["service_categories"] = ServiceCategory.objects.all()
        context["search_query"] = self.request.GET.get("search", "")
        context["current_sort"] = self.request.GET.get("sort")
        return context


class EstateDetailView(LoginRequiredMixin, DetailView):
    model = Estate
    template_name = "estate_detail.html"
    context_object_name = "estate"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PurchaseRequestForm(initial={"estate": self.object.id})
        if self.request.user.is_authenticated and hasattr(self.request.user, "client"):
            context["request_exists"] = PurchaseRequest.objects.filter(
                client=self.request.user.client, estate=self.object
            ).exists()
        else:
            context["request_exists"] = False
        return context


class CreatePurchaseRequestView(LoginRequiredMixin, CreateView):
    model = PurchaseRequest
    form_class = PurchaseRequestForm
    template_name = "estate_detail.html"

    def form_valid(self, form):
        form.instance.client = Client.objects.filter(user=self.request.user)[0]
        form.instance.estate_id = self.kwargs["pk"]

        if PurchaseRequest.objects.filter(
            client=self.request.user.client, estate_id=self.kwargs["pk"]
        ).exists():
            messages.error(self.request, "You have already purchased this request.")
        else:
            PurchaseRequest.objects.create_with_assignment(
                client=self.request.user.client,
                estate_id=self.kwargs["pk"],
                message=form.cleaned_data["message"],
            )

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("estate_detail", kwargs={"pk": self.kwargs["pk"]})
