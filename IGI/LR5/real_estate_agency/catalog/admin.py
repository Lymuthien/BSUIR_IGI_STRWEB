from django.contrib import admin

from .models import (
    Category,
    Estate,
    Employee,
    Sale,
    Client,
    Owner,
    ServiceCategory,
    Service,
)

admin.site.register(Owner)


class EstateInline(admin.TabularInline):
    model = Estate


class SaleInline(admin.TabularInline):
    model = Sale


class ServiceInline(admin.TabularInline):
    model = Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "cost", "category")


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    inlines = (ServiceInline,)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    inlines = [SaleInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [EstateInline]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_filter = ["name", "email", "phone_number"]


@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):
    list_display = ["address", "cost", "category"]


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ["employee", "date_of_sale", "estate", "service_cost", "cost"]
    list_filter = ["date_of_sale", "employee"]

    fieldsets = (
        (None, {
            "fields": (
                "employee",
                "client",
            )
        }),
        ("Estate", {
            "fields": (
                "estate",
                "date_of_sale",
                "date_of_contract",
                "service",
            )
        }),
    )
