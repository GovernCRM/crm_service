from django.contrib import admin

from .models import List


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'parent', 'user_uuid', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
