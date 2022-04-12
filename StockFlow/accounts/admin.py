from django.contrib import admin

# Register your models here.
from accounts.models import User

class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'ID',
        'full_name',
        'email',
        'city',
        'Mobile',
        'is_Customer',
        'is_Agent',
        'is_Admin',
        'isConfirmedAgent',
        'isPortfolio',
        'password'
        )
    list_filter = ('is_Customer','is_Agent','is_Admin')
    search_fields = ['email','full_name','ID']
    readonly_fields = ('ID','password')
    filter_horizontal = ()


admin.site.register(User,UsersAdmin)
