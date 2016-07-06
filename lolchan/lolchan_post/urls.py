from django.conf.urls import patterns, include, url
from lolchan.lolchan_post.crinstances import base_crinstance

urlpatterns = patterns(
    'lolchan.lolchan_post',
    url(r'^', include(base_crinstance.BaseCrinstance.urls())),
)