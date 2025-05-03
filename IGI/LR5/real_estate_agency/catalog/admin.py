from django.contrib import admin

from .models import Category, Estate, Employee, Sale, Buyer, Owner

admin.site.register(Owner)


class EstateInline(admin.TabularInline):
    model = Estate


class SaleInline(admin.TabularInline):
    model = Sale


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    inlines = [SaleInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [EstateInline]


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_filter = ["name", "email", "phone_number"]


@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):
    list_display = ["address", "cost", "category"]


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ["employee", "date_of_sale", "estate"]
