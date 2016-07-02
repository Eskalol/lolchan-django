from django.conf.urls import patterns, include, url
from lolchan.lolchan_channel.crinstances import base_crinstance


urlpatterns = patterns(
    'lolchan.lolchan_channel',
    url(r'^', include(base_crinstance.BaseCrinstance.urls())),
)
