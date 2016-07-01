from django.conf.urls import include, url
from django.contrib import admin

#from lolchan.lolchan_admin.cradmin import CrAdminInstance


admin.autodiscover()


default_urls = [
    url(r'^superuser/', include(admin.site.urls)),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name='lolchan-logout'),
    #url(r'^admin/', include(CrAdminInstance.urls())),
]
