from django.contrib import admin

#from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
@admin.display(boolean=True)
class UserAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'username', 'email', 'is_subscribed']


