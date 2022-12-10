from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class CustomUserAdmin(UserAdmin):
    list_display_links = ('username',)
    exclude = ('first_name', 'last_name', 'last_login')
    model = CustomUser


admin.site.register(CustomUser, UserAdmin)
admin.site.site_title = 'Assortment Management'
admin.site.site_header = 'Assortment Management'
