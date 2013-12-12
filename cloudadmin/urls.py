from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xenadmin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^vm/', include('vms.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
