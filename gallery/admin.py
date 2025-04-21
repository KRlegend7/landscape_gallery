from django.contrib import admin
from .models import Landscape, ImportHistory

@admin.register(Landscape)
class LandscapeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ImportHistory)
class ImportHistoryAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'date_imported', 'successful_records', 'failed_records')
    list_filter = ('date_imported',)
    readonly_fields = ('date_imported',)