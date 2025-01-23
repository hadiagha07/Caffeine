from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('phone', 'first_name', 'last_name', 'is_staff')
    search_fields = ('phone', 'first_name', 'last_name')
    ordering = ('-joined',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'profile_image')}),
        ('دسترسیها', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('تاریخها', {'fields': ('last_login', 'joined')}),
    )

admin.site.register(User, CustomUserAdmin)