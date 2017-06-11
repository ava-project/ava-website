from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .models import EmailValidationToken, Profile


@admin.register(EmailValidationToken)
class EmailValidationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'consumed')
    search_fields = ('user__username', 'token')
    readonly_fields = ('user', 'token', 'consumed',)


class ProfileInline(admin.StackedInline):
    """ Details a person in line. """
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name',)
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (_('Personal info'), {'fields':
            ('username', 'first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields':
            ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('date_joined', 'last_login',)}),
    )
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
