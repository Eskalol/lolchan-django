from django.conf import settings
from django.conf.urls import patterns, url

from lolchan.project.default.default_urls import default_urls


urlpatterns = patterns('', *default_urls)

urlpatterns += [
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT})
]
