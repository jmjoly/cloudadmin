from django.contrib import admin
from services.models import ServiceTemplate, Service

class ServiceTemplateAdmin(admin.ModelAdmin):
    search_fields = ['service_template_name']

admin.site.register(ServiceTemplate, ServiceTemplateAdmin)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_template', 'service_vm')
    search_fields = ['service_template']

admin.site.register(Service, ServiceAdmin)
