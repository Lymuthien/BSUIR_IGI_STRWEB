from django.contrib import admin

from .models import (
    Category,
    Estate,
    Sale,
    ServiceCategory,
)


class EstateInline(admin.TabularInline):
    model = Estate


class SaleInline(admin.TabularInline):
    model = Sale


class CategoryInline(admin.TabularInline):
    model = Category


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    inlines = (CategoryInline, )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [EstateInline]


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
                "category",
            )
        }),
    )
