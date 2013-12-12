from django.conf.urls import patterns, url

from vms.views import VmListView

urlpatterns = patterns('',
    url(r'^$', VmListView.as_view(), name='vm_list'),
)
