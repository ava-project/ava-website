from django.contrib import admin

from .models import Plugin, Release


class ReleaseInline(admin.StackedInline):
    model = Release


@admin.register(Plugin)
class PluginAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    inlines = [ReleaseInline]
