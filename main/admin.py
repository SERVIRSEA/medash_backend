from django.contrib import admin
from .models import APIKey, DownloadRequest

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'key_name', 'key', 'created_at', 'updated_at')
    readonly_fields = ('key',) 

@admin.register(DownloadRequest)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'institution', 'job_title', 'dataset', 'downloaded_date', 'purpose_of_download')
