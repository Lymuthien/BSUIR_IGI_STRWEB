import logging
from datetime import timedelta

import pandas as pd
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count, Sum
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from users.models import Client, Employee

from .forms import PurchaseRequestForm
from .models import ServiceCategory, Service, Estate, Sale, PurchaseRequest

logger = logging.getLogger(__name__)


class ServiceListView(ListView):
    model = Service
    template_name = "service_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        logger.debug(f"Getting queryset of service list")

        service_category = self.request.GET.get("service_category")
        if service_category:
            logger.debug(f"Filtering by service_category: {service_category}")
            queryset = queryset.filter(category_id=service_category)

        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")

        if min_price:
            logger.debug(f"Filtering by min_price: {min_price}")
            queryset = queryset.filter(cost__gte=float(min_price))

        if max_price:
            logger.debug(f"Filtering by max_price: {max_price}")
            queryset = queryset.filter(cost__lte=float(max_price))

        logger.info("ServiceListView queryset prepared")
        return queryset.select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["service_categories"] = ServiceCategory.objects.all()
        return context


class AvailableEstateListView(LoginRequiredMixin, ListView):
    model = Estate
    template_name = "estate_list.html"
    paginate_by = 9
    ordering = "-cost"

    def get_queryset(self):
        logger.debug("Fetching queryset for AvailableEstateListView")
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
            logger.debug(f"Filtering by category_id: {category_id}")
            queryset = queryset.filter(category_id=category_id)

        service_category_id = self.request.GET.get("service_category")
        if service_category_id:
            logger.debug(f"Filtering by service_category_id: {service_category_id}")
            queryset = queryset.filter(category__category_id=service_category_id)

        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        if min_price:
            logger.debug(f"Filtering by min_price: {min_price}")
            queryset = queryset.filter(cost__gte=min_price)
        if max_price:
            logger.debug(f"Filtering by max_price: {max_price}")
            queryset = queryset.filter(cost__lte=max_price)

        sort = self.request.GET.get("sort")
        if sort:
            logger.debug(f"Sorting by: {sort}")
            sort_options = {
                "price_asc": "cost",
                "price_desc": "-cost",
                "area_asc": "area",
                "area_desc": "-area",
            }
            if sort in sort_options:
                queryset = queryset.order_by(sort_options[sort])
            else:
                logger.warning(f"Invalid sort option: {sort}")
                queryset = queryset.order_by(self.ordering)
        else:
            queryset = queryset.order_by(self.ordering)

        logger.info("AvailableEstateListView queryset prepared")
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
        logger.debug(
            f"Preparing context for EstateDetailView, estate_id={self.kwargs.get('pk')}"
        )
        context = super().get_context_data(**kwargs)
        context["form"] = PurchaseRequestForm(initial={"estate": self.object.id})
        if self.request.user.is_authenticated and hasattr(self.request.user, "client"):
            context["request_exists"] = PurchaseRequest.objects.filter(
                client=self.request.user.client, estate=self.object
            ).exists()
            logger.debug(
                f"Checked request_exists for user {self.request.user.username}: {context['request_exists']}"
            )
        else:
            context["request_exists"] = False
            logger.debug(
                "User not authenticated or no client, request_exists set to False"
            )

        logger.info("EstateDetailView context prepared")
        return context


class CreatePurchaseRequestView(LoginRequiredMixin, CreateView):
    model = PurchaseRequest
    form_class = PurchaseRequestForm
    template_name = "estate_detail.html"

    def form_valid(self, form):
        logger.debug(
            f"User {self.request.user.username} submitting PurchaseRequest for estate_id={self.kwargs['pk']}"
        )

        form.instance.client = Client.objects.filter(user=self.request.user)[0]
        form.instance.estate_id = self.kwargs["pk"]

        if PurchaseRequest.objects.filter(
            client=self.request.user.client, estate_id=self.kwargs["pk"]
        ).exists():
            logger.error(
                f"Duplicate PurchaseRequest for estate {form.instance.estate} and client {form.instance.client}"
            )
        else:
            PurchaseRequest.objects.create_with_assignment(
                client=self.request.user.client,
                estate_id=self.kwargs["pk"],
                message=form.cleaned_data["message"],
            )
            logger.info(
                f"PurchaseRequest created by {self.request.user.username}: estate={form.instance.estate}, client={form.instance.client}"
            )

        return redirect(self.get_success_url())

    def get_success_url(self):
        logger.debug(f"Redirecting to estate_detail for estate_id={self.kwargs['pk']}")
        return reverse_lazy("estate_detail", kwargs={"pk": self.kwargs["pk"]})


class ClientDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "client_dashboard.html"

    def get_context_data(self, **kwargs):
        logger.debug(
            f"Preparing context for ClientDashboardView, user={self.request.user.username}"
        )
        context = super().get_context_data(**kwargs)
        if not hasattr(self.request.user, "client"):
            logger.warning(f"User {self.request.user.username} has no client assigned")
            messages.error(self.request, "You have not client assigned.")
            return context

        context["requests"] = PurchaseRequest.objects.filter(
            client=self.request.user.client
        ).select_related("estate", "employee")

        context["sales"] = Sale.objects.filter(
            client=self.request.user.client
        ).select_related("estate", "employee", "category")

        logger.info(
            f"ClientDashboardView context prepared for user {self.request.user.username}"
        )
        return context

    def post(self, request, *args, **kwargs):
        logger.debug(
            f"Processing POST request for ClientDashboardView, user={request.user.username}"
        )
        action = request.POST.get("action")
        request_id = request.POST.get("request_id")

        if not request_id:
            logger.error("No request_id provided in POST request")
            messages.error(request, "Incorrect request.")
            return redirect("client_dashboard")

        purchase_request = get_object_or_404(
            PurchaseRequest, pk=request_id, client=self.request.user.client
        )

        if action == "buy":
            if purchase_request.status in ["new", "in_progress"]:
                logger.debug(f"Creating Sale for PurchaseRequest id={request_id}")
                Sale.objects.create(
                    client=purchase_request.client,
                    employee=purchase_request.employee,
                    date_of_contract=timezone.now().date(),
                    date_of_sale=timezone.now().date(),
                    estate=purchase_request.estate,
                    category=purchase_request.estate.category,
                    service_cost=(
                        purchase_request.estate.category.cost
                        if purchase_request.estate.category
                        else 0
                    ),
                    cost=purchase_request.estate.cost,
                )

                purchase_request.status = "completed"
                purchase_request.save()
                logger.info(
                    f"Sale created and PurchaseRequest id={request_id} marked as completed"
                )
            else:
                logger.warning(f"PurchaseRequest id={request_id} already completed")
                messages.error(request, "This purchase is already completed.")

        elif action == "cancel":
            if purchase_request.status in ["new", "in_progress"]:
                logger.debug(f"Cancelling PurchaseRequest id={request_id}")
                purchase_request.status = "completed"
                purchase_request.save()
            else:
                logger.warning(f"PurchaseRequest id={request_id} already completed")
                messages.error(request, "This purchase is already completed.")

        return redirect("client_dashboard")


class EmployeeDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "employee_dashboard.html"

    def get_context_data(self, **kwargs):
        logger.debug(
            f"Preparing context for EmployeeDashboardView, user={self.request.user.username}"
        )
        context = super().get_context_data(**kwargs)
        if not hasattr(self.request.user, "employee"):
            logger.warning(f"User {self.request.user.username} is not an employee")
            messages.error(self.request, "You must be employee.")
            return context

        context["clients"] = Client.objects.filter(
            purchaserequest__employee=self.request.user.employee,
            purchaserequest__status__in=["new", "in_progress"],
        ).distinct()

        context["requests"] = PurchaseRequest.objects.filter(
            employee=self.request.user.employee, status__in=["new", "in_progress"]
        ).select_related("estate", "client")

        context["sales"] = Sale.objects.filter(
            employee=self.request.user.employee
        ).select_related("estate", "client", "category")

        logger.info(
            f"EmployeeDashboardView context prepared for user {self.request.user.username}"
        )
        return context


class StatisticsView(LoginRequiredMixin, TemplateView):
    template_name = "statistics.html"

    def get_context_data(self, **kwargs):
        logger.info(
            f"Preparing context for StatisticsView, user={self.request.user.username}"
        )
        context = super().get_context_data(**kwargs)

        sales = Sale.objects.all()

        estate_df = pd.Series([float(s.cost) for s in sales])
        cost_stats = {
            "mean_cost": estate_df.mean() or 0,
            "median_cost": estate_df.median() or 0,
            "mode_cost": estate_df.mode().get(0) or 0,
        }
        logger.debug(f"cost_stats: {cost_stats}")
        context["cost_stats"] = cost_stats

        service_df = pd.Series([float(s.service_cost) for s in sales if s.service_cost])
        service_stats = {
            "mean_cost": service_df.mean() or 0,
            "median_cost": service_df.median() or 0,
            "mode_cost": service_df.mode().get(0) or 0,
        }
        logger.debug(f"service_stats: {service_stats}")
        context["service_stats"] = service_stats

        clients = Client.objects.filter(user__birth_date__isnull=False)
        today = timezone.now().date()
        ages = [
            today.year
            - client.user.birth_date.year
            - (
                (today.month, today.day)
                < (client.user.birth_date.month, client.user.birth_date.day)
            )
            for client in clients
        ]

        ages_df = pd.Series(ages)
        client_stats = {"mean_age": ages_df.mean(), "median_age": ages_df.median()}
        logger.debug(f"client_stats: {client_stats}")
        context["client_stats"] = client_stats

        popular_category = (
            Service.objects.filter(estate__sale__isnull=False)
            .annotate(count=Count("estate"))
            .order_by("-count")
            .first()
        )
        logger.debug(f"popular_category: {popular_category}")
        context["popular_category"] = popular_category

        profitable_service_category = (
            Service.objects.filter(
                estate__sale__isnull=False,
            )
            .annotate(total_service_cost=Sum("estate__category__cost"))
            .order_by("-total_service_cost")
            .first()
        )
        logger.debug(f"profitable_service_category: {profitable_service_category}")
        context["profitable_service_category"] = profitable_service_category

        one_month_ago = timezone.now() - timedelta(days=30)
        employee_service_stats = (
            Employee.objects.filter(sale__date_of_sale__gte=one_month_ago)
            .annotate(total_service_cost=Sum("sale__service_cost"))
            .order_by("-total_service_cost")
        )
        logger.debug(f"employee_service_stats: {employee_service_stats}")
        context["employee_service_stats"] = employee_service_stats

        employee_total_stats = (
            Employee.objects.filter(sale__date_of_sale__gte=one_month_ago)
            .annotate(total_cost=Sum("sale__cost"))
            .order_by("-total_cost")
        )
        logger.debug(f"employee_total_stats: {employee_total_stats}")
        context["employee_total_stats"] = employee_total_stats

        highest_value_category = (
            Service.objects.filter(
                estate__sale__isnull=False
            )
            .annotate(total_value=Sum("estate__cost") + Sum("cost"))
            .order_by("-total_value")
            .first()
        )

        logger.debug(f"highest_value_category: {highest_value_category}")
        context["highest_value_category"] = highest_value_category

        logger.info(
            f"StatisticsViewContext prepared for user: {self.request.user.username}"
        )
        return context
