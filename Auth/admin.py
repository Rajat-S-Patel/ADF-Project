from django.contrib import admin
from .models import CustomUser
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ['username','first_name','last_name']
    ordering=('-start_date',)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

    fieldsets = (
                (None,{'fields':('username','email','password','first_name','last_name','image')}),
                ('Permissions',{'fields':('is_staff','is_superuser','is_active')}),)

admin.site.register(CustomUser, CustomUserAdmin)