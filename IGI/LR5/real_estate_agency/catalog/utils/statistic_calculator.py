import logging
from datetime import timedelta

import pandas as pd
from django.db.models import Count, Sum, F
from django.utils import timezone
from users.models import Client, Employee

from ..models import Sale, Service

logger = logging.getLogger(__name__)


class StatisticsCalculator(object):
    @staticmethod
    def get_sale_cost_stats():
        logger.info("StatisticCalculator.get_sale_cost_stats()")
        sales = Sale.objects.all()

        estate_df = pd.Series([float(s.cost) for s in sales])
        full_cost_stats = {
            "mean_cost": estate_df.mean() or 0,
            "median_cost": estate_df.median() or 0,
            "mode_cost": estate_df.mode().get(0) or 0,
        }
        logger.debug(f"full_cost_stats: {full_cost_stats}")

        service_df = pd.Series([float(s.estate.category.cost) for s in sales])
        service_cost_stats = {
            "mean_cost": service_df.mean() or 0,
            "median_cost": service_df.median() or 0,
            "mode_cost": service_df.mode().get(0) or 0,
        }
        logger.debug(f"service_cost_stats: {service_cost_stats}")

        return full_cost_stats, service_cost_stats

    @staticmethod
    def get_client_stats():
        logger.info("StatisticCalculator.get_client_ages()")

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
        logger.debug(f"ages: {ages}")

        ages_df = pd.Series(ages)
        client_stats = {"mean_age": ages_df.mean(), "median_age": ages_df.median()}
        logger.debug(f"client_stats: {client_stats}")

        return client_stats

    @staticmethod
    def get_services_by_sold_count():
        logger.info("StatisticCalculator.get_services_sold_estate_count()")

        services = (
            Service.objects.filter(estate__sale__isnull=False)
            .annotate(count=Count("estate"))
            .order_by("-count")
        )
        counts = services.values_list("count", flat=True)
        logger.debug(f"services: {services}")

        return services, counts

    @staticmethod
    def get_services_by_service_profit():
        logger.info("StatisticCalculator.get_services_by_service_profit()")

        services_by_service_profit = (
            Service.objects.filter(
                estate__sale__isnull=False,
            )
            .annotate(total_service_cost=Sum("estate__category__cost"))
            .order_by("-total_service_cost")
        )
        service_profits = services_by_service_profit.values_list(
            "total_service_cost", flat=True
        )

        logger.debug(f"services_by_service_profit: {services_by_service_profit}")

        return services_by_service_profit, service_profits

    @staticmethod
    def get_services_by_full_costs():
        logger.info("StatisticCalculator.get_services_by_full_costs()")

        services_by_full_costs = (
            Service.objects.filter(estate__sale__isnull=False)
            .annotate(total_value=Sum("estate__cost") + Sum("cost"))
            .order_by("-total_value")
        )
        profits = services_by_full_costs.values_list("total_value", flat=True)
        logger.debug(f"services_by_full_costs: {services_by_full_costs}")

        return services_by_full_costs, profits

    @staticmethod
    def get_employees_by_service_profit(days_ago=30):
        logger.info("StatisticCalculator.get_employees_by_service_profit()")

        time_ago = timezone.now() - timedelta(days=days_ago)
        employee_service_stats = (
            Employee.objects.filter(sale__date_of_sale__gte=time_ago)
            .annotate(total_service_cost=Sum("sale__estate__category__cost"))
            .order_by("-total_service_cost")
        )
        costs = employee_service_stats.values_list("total_service_cost", flat=True)
        logger.debug(f"employee_service_stats: {employee_service_stats}")

        return employee_service_stats, costs

    @staticmethod
    def get_employees_by_full_costs(days_ago=30):
        logger.info("StatisticCalculator.get_employees_by_full_costs()")

        time_ago = timezone.now() - timedelta(days=days_ago)
        employee_total_stats = (
            Employee.objects.filter(sale__date_of_sale__gte=time_ago)
            .annotate(
                total_cost=Sum("sale__cost"))
            .order_by("-total_cost")
        )
        costs = employee_total_stats.values_list("total_cost", flat=True)
        logger.debug(f"employee_total_stats: {employee_total_stats}")

        return employee_total_stats, costs
