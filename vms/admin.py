from django.contrib import admin
from vms.models import VmTemplate, Vm
from services.models import ServiceTemplate, Service

class VmTemplateAdmin(admin.ModelAdmin):
    list_display = ('vm_template_name', 'vm_template_name')

admin.site.register(VmTemplate, VmTemplateAdmin)

class ServicesInLine(admin.TabularInline):
    model = Service
    extra = 1

class VmAdmin(admin.ModelAdmin):
    list_display = ('vm_name', 'vm_ip', 'vm_info')
    search_fields = ['vm_name']
    inlines = [ServicesInLine]

admin.site.register(Vm, VmAdmin)

admin.site.disable_action('delete_selected')
