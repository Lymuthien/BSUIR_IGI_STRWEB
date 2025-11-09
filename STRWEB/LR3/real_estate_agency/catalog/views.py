import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from django.conf import settings
from users.models import Client, Employee

from .forms import PurchaseRequestForm
from .models import ServiceCategory, Service, Estate, Sale, PurchaseRequest
from .utils import Plotter, StatisticsCalculator, MapboxClient

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
            logger.warning(
                "User not authenticated or no client, request_exists set to False"
            )

        if self.request.user.is_authenticated:
            context["map_image_url"] = MapboxClient.get_map_image_url(
                self.object.address
            )
            logger.debug(
                f"Map image URL for estate {self.object.id}: {context['map_image_url']}"
            )

        logger.info("EstateDetailView context prepared")
        return context


class EstateCreateView(PermissionRequiredMixin, CreateView):
    model = Estate
    template_name = 'estate_form.html'
    fields = ['cost', 'area', 'category', 'description', 'image', 'address']
    permission_required = 'estates.add_estate'
    success_url = reverse_lazy('estates')

    def form_valid(self, form):
        messages.success(self.request, 'Successfully created estate')
        return super().form_valid(form)


class EstateUpdateView(PermissionRequiredMixin, UpdateView):
    model = Estate
    template_name = 'estate_form.html'
    fields = ['cost', 'area', 'category', 'description', 'image', 'address']
    permission_required = 'estates.change_estate'

    def get_success_url(self):
        return reverse_lazy('estate_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Successfully updated estate')
        return super().form_valid(form)


class EstateDeleteView(PermissionRequiredMixin, DeleteView):
    model = Estate
    template_name = 'estate_confirm_delete.html'
    permission_required = 'estates.delete_estate'
    success_url = reverse_lazy('estates')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Successfully deleted estate')
        return super().delete(request, *args, **kwargs)

class CreatePurchaseRequestView(LoginRequiredMixin, CreateView):
    model = PurchaseRequest
    form_class = PurchaseRequestForm
    template_name = "estate_detail.html"

    def form_valid(self, form):
        logger.debug(
            f"User {self.request.user.username} submitting PurchaseRequest for estate_id={self.kwargs['pk']}"
        )

        if self.request.user.is_authenticated and hasattr(self.request.user, "client"):
            form.instance.client = self.request.user.client
            form.instance.estate_id = self.kwargs["pk"]

            if PurchaseRequest.objects.filter(
                client=self.request.user.client, estate_id=self.kwargs["pk"]
            ).exists():
                logger.error(
                    f"Duplicate PurchaseRequest for estate {form.instance.estate_id} and client {form.instance.client}"
                )
            else:
                PurchaseRequest.objects.create_with_assignment(
                    client=self.request.user.client,
                    estate_id=self.kwargs["pk"],
                    message=form.cleaned_data["message"],
                )
                logger.info(
                    f"PurchaseRequest created by {self.request.user.username}: estate={form.instance.estate}"
                )
        else:
            logger.error(f"User not authenticated or no client")

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

        if hasattr(self.request.user, "client"):
            context["requests"] = PurchaseRequest.objects.filter(
                client=self.request.user.client
            ).select_related("estate", "employee")

            context["sales"] = Sale.objects.filter(
                client=self.request.user.client
            ).select_related("estate", "employee")

            logger.info(
                f"ClientDashboardView context prepared for user {self.request.user.username}"
            )
        else:
            logger.warning(f"User {self.request.user.username} has no client assigned")
            messages.error(self.request, "You have not client assigned.")

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
                sale = Sale.objects.create(
                    client=purchase_request.client,
                    employee=purchase_request.employee,
                    estate=purchase_request.estate,
                )

                purchase_request.status = "completed"
                purchase_request.save()
                logger.info(
                    f"Sale created and PurchaseRequest id={request_id} marked as completed"
                )

                return redirect("payment", sale_id=sale.id)
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

class PaymentView(LoginRequiredMixin, TemplateView):
    template_name = "payment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sale_id = kwargs.get("sale_id")
        sale = get_object_or_404(Sale, id=sale_id, client=self.request.user.client)
        context["sale"] = sale
        context["cost"] = sale.cost
        return context

class EmployeeDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "employee_dashboard.html"

    def get_context_data(self, **kwargs):
        logger.debug(
            f"Preparing context for EmployeeDashboardView, user={self.request.user.username}"
        )
        context = super().get_context_data(**kwargs)

        if hasattr(self.request.user, "employee"):
            context["clients"] = Client.objects.filter(
                purchaserequest__employee=self.request.user.employee,
                purchaserequest__status__in=["new", "in_progress"],
            ).distinct()

            context["requests"] = PurchaseRequest.objects.filter(
                employee=self.request.user.employee, status__in=["new", "in_progress"]
            ).select_related("estate", "client")

            context["sales"] = Sale.objects.filter(
                employee=self.request.user.employee
            ).select_related("estate", "client")

            logger.info(
                f"EmployeeDashboardView context prepared for user {self.request.user.username}"
            )
        else:
            logger.warning(f"User {self.request.user.username} is not an employee")
            messages.error(self.request, "You must be employee.")

        return context


class StatisticsView(LoginRequiredMixin, TemplateView):
    template_name = "statistics.html"

    def get_context_data(self, **kwargs):
        logger.info(
            f"Preparing context for StatisticsView, user={self.request.user.username}"
        )
        context = super().get_context_data(**kwargs)

        cost_stats, service_stats = StatisticsCalculator.get_sale_cost_stats()
        client_stats = StatisticsCalculator.get_client_stats()
        services_by_sold_count, counts = (
            StatisticsCalculator.get_services_by_sold_count()
        )
        services_by_service_profit, service_profits = (
            StatisticsCalculator.get_services_by_service_profit()
        )
        services_by_full_costs, full_costs = (
            StatisticsCalculator.get_services_by_full_costs()
        )
        employee_service_stats, employee_service_costs = (
            StatisticsCalculator.get_employees_by_service_profit()
        )
        employee_total_stats, total_costs = (
            StatisticsCalculator.get_employees_by_full_costs()
        )

        image_paths = {
            "services_by_sold_count": f"{settings.MEDIA_URL}services_by_sold_count.jpg",
            "services_by_service_profit": f"{settings.MEDIA_URL}services_by_service_profit.jpg",
            "employee_service_stats": f"{settings.MEDIA_URL}employee_service_stats.jpg",
            "employee_total_stats": f"{settings.MEDIA_URL}employee_total_stats.jpg",
            "services_by_full_costs": f"{settings.MEDIA_URL}services_by_full_costs.jpg",
        }

        Plotter.plt_bars(
            counts,
            path=image_paths["services_by_sold_count"][1:],
            categories=(str(s)[:12] for s in services_by_sold_count),
        )
        Plotter.plt_bars(
            service_profits,
            path=image_paths["services_by_service_profit"][1:],
            categories=(str(s)[:12] for s in services_by_sold_count),
        )
        Plotter.plt_bars(
            employee_service_costs,
            path=image_paths["employee_service_stats"][1:],
            categories=(e.user.username for e in employee_service_stats),
        )
        Plotter.plt_bars(
            total_costs,
            path=image_paths["employee_total_stats"][1:],
            categories=(e.user.username for e in employee_total_stats),
        )
        Plotter.plt_bars(
            full_costs,
            path=image_paths["services_by_full_costs"][1:],
            categories=(str(s)[:12] for s in services_by_full_costs),
        )

        context.update(
            {
                "cost_stats": cost_stats,
                "service_stats": service_stats,
                "client_stats": client_stats,
                "popular_category": services_by_sold_count.first(),
                "profitable_service": services_by_service_profit.first(),
                "employee_service_stats": employee_service_stats,
                "employee_total_stats": employee_total_stats,
                "highest_cost_service": services_by_full_costs.first(),
                "chart_images": image_paths,
            }
        )

        logger.info(
            f"StatisticsViewContext prepared for user: {self.request.user.username}"
        )
        return context
