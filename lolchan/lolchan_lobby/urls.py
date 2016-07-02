from django.conf.urls import patterns, include, url
from lolchan.lolchan_lobby.crinstances import base_crinstance


urlpatterns = patterns(
    'lolchan.lolchan_lobby',
    url(r'^', include(base_crinstance.BaseCrinstance.urls())),
)
