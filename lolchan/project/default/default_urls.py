from django.conf.urls import include, url
from django.contrib import admin

#from lolchan.lolchan_admin.cradmin import CrAdminInstancef
from django_cradmin.superuserui import superuserui_registry

admin.autodiscover()


default_urls = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name='lolchan-logout'),
    url(r'^superuser/', include(superuserui_registry.default.make_cradmin_instance_class().urls())),
    url(r'^lobby/', include('lolchan.lolchan_lobby.urls')),
    url(r'^channel/', include('lolchan.lolchan_channel.urls')),
    url(r'^post/', include('lolchan.lolchan_post.urls')),
    url(r'^api/', include('lolchan.lolchan_api.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    #url(r'^admin/', include(CrAdminInstance.urls())),
]
