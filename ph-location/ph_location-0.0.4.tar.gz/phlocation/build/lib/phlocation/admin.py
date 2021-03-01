from django.contrib import admin

from phlocation.models import PSGC


@admin.register(PSGC)
class PSGCAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'geographic_level')
    fields = ('code', 'name', 'geographic_level')

    list_filter = ('geographic_level',)

    ordering = ('code',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
