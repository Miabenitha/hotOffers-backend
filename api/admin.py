from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.forms import UserCreationForm, UserChangeForm
from users.models import User, UserLocation, UserAvatar


admin.site.site_header = 'Hot Offers Administration'
admin.site.register(UserLocation)
admin.site.register(UserAvatar)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = (
        "email",
        "first_name",
        "last_name",
        "user_type",
        "is_verfied",
        "is_active",
    )
    list_filter = (
        "email",
        "user_type",
        "is_staff",
        "is_verfied",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email_token")}),
        ("Permissions", {"fields": ("user_type", "is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "user_type",
                    "is_staff",
                    "is_active",
                    "is_verfied",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, UserAdmin)
