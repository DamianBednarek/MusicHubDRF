from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email",)}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_admin", "is_verified")},
        ),
        # ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Custom Info", {"fields": ("profile_avatar", "followers")}),
    )
    filter_horizontal = ()
    ordering = (
        "created_at",
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("email", "is_active", "is_staff")


admin.site.register(get_user_model(), UserAdmin)
