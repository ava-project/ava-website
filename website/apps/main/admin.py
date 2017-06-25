from django.contrib import admin

from .models import OperatingSystem, CoreInstaller


@admin.register(OperatingSystem)
class OperatingSystemAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(CoreInstaller)
class CoreInstallerAdmin(admin.ModelAdmin):
    list_display = ('version', 'os', 'created')
    list_filter = ('os', 'created')
