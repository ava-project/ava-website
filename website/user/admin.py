from django.contrib import admin

from .models import EmailValidationToken

class EmailValidationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'consumed')
    search_fields = ('user__username', 'token')
    readonly_fields = ('user', 'token', 'consumed',)

admin.site.register(EmailValidationToken, EmailValidationTokenAdmin)
