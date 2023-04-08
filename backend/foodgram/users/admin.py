from django.contrib import admin
from .models import CustomUser, Subscribe

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):

    list_display = ['email', 'last_name', 'first_name', 'username', 'show_users']

    def show_users(self, obj):
        users_list = []
        queryset_users = obj.subscribed.all()
        for _ in queryset_users:
           users_list.append(f'{_.user}')
        return ', '.join(users_list)
    show_users.short_description = 'Подписки'

##   def show_issubscribed(self, obj):
 #       return Subscribe.objects.filter(user=obj).exists()
#    show_issubscribed.short_description = 'Подписка'
@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['subscribed', 'user']


