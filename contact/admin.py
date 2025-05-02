from django.contrib import admin
from .models import Contact, DynamicFormField


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass

class DynamicFormFieldAdmin(admin.ModelAdmin):
    list_display = ('field_name', 'field_type', 'field_value')
    search_fields = ('field_name',)
    list_filter = ('field_type',)
    ordering = ('field_name',)
    list_per_page = 20
admin.site.register(DynamicFormField, DynamicFormFieldAdmin)