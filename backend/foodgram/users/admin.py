from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
@admin.display(boolean=True)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'last_name', 'first_name', 'username', 'is_subscribed']


