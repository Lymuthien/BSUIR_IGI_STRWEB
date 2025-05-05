from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Employee, Client, Profile

admin.site.register(Employee)
admin.site.register(Client)
admin.site.register(Profile)


class EmployeeInline(admin.StackedInline):
    model = Employee

class ProfileInline(admin.StackedInline):
    model = Profile

class ClientInline(admin.StackedInline):
    model = Client


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_staff")
    list_filter = ("role", "is_staff")
    inlines = (EmployeeInline, ClientInline, ProfileInline)

    fieldsets = (
        (None, {
            "fields": (
                "username",
                "password"
            )}
         ),
        ("Personal info", {
            "fields": (
                "first_name",
                "last_name",
                "email",
                "phone_number",
                "birth_date",
            )}
         ),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
                "role",
                ),
            },
        ),
        ("Important dates", {
            "fields": (
                "last_login",
                "date_joined"
            )}
         ),
    )
