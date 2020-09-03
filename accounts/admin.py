from django.contrib import admin
from .models import User, OTPModel
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
class UserAdmin(BaseUserAdmin):
	model = User
	list_display = ('phone', 'name', 'is_admin',)
	list_filter = ('is_admin',)
	fieldsets = (
        (None, {'fields': ('phone','password', 'name')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_staff')}),
    )
	add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'name','password', 'is_admin', 'is_active','is_staff'),
        }),
    )
	search_fields = ('phone',)
	ordering = ('phone',)
	filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(OTPModel)
