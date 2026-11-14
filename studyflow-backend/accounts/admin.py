from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class AccountAdmin(UserAdmin):
    ordering = ('email',)
    list_display = ('email', 'full_name', 'university', 'is_active', 'is_staff')
    search_fields = ('email', 'full_name', 'university')
    readonly_fields = ('terms_accepted_at', 'last_login', 'date_joined')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Profile', {'fields': ('full_name', 'university', 'terms_accepted_at')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('email', 'full_name', 'university', 'password1', 'password2')}),)

