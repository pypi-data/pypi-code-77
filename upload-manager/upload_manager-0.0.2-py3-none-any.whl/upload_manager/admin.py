from django.contrib import admin
from django.utils.html import format_html

from .models import UploadManager


@admin.register(UploadManager)
class UploadManagerAdmin(admin.ModelAdmin):
    list_display = ('id', 'upload_name', 'user', 'get_s3_upload_path_link',
                    'get_s3_download_path_link', 'status', 'meta_info', 'created_on', 'updated_on')
    list_filter = ('status', 'upload_name')
    search_fields = ('upload_name',)
    ordering = ('-created_on',)
    list_per_page = 100

    def get_s3_upload_path_link(self, obj):
        if not obj.s3_upload_path:
            return None
        return format_html(f'<a href="{obj.s3_upload_path}" target="_blank">Download Request File</a>')
    get_s3_upload_path_link.short_description = "Request File"

    def get_s3_download_path_link(self, obj):
        if not obj.s3_download_path:
            return None
        return format_html(f'<a href="{obj.s3_download_path}" target="_blank">Download Response File</a>')
    get_s3_download_path_link.short_description = "Response File"

    def has_delete_permission(self, request):
        return False

    def has_add_permission(self, request):
        return False

