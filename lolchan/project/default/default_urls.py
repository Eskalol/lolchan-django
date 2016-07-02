from django.conf.urls import include, url
from django.contrib import admin

#from lolchan.lolchan_admin.cradmin import CrAdminInstance
from django_cradmin.superuserui import superuserui_registry

admin.autodiscover()


default_urls = [
    url(r'^superuser/', include(admin.site.urls)),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name='lolchan-logout'),
    url('^cradmin/', include(superuserui_registry.default.make_cradmin_instance_class().urls())),
    #url(r'^admin/', include(CrAdminInstance.urls())),
]
