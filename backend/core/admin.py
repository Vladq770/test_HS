from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('username',  'phone_number')
    search_fields = ('username', 'phone_number')
    list_filter = ('username',  'phone_number')
    readonly_fields = ('created_at',)


admin.site.register(User, UserAdmin)