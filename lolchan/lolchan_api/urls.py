from django.conf.urls import patterns, url, include
from rest_framework import routers

from lolchan.lolchan_api.channel import views as channel_views
from lolchan.lolchan_api.post import views as post_views
router = routers.DefaultRouter()

urlpatterns = patterns(
    url(r'^', include(router.urls)),
    url(r'^channel/$', channel_views.ChannelViewList.as_view(), name='list'),
    url(r'^channel/(?P<order>.+)/list-order-by$', channel_views.ChannelViewListOrder.as_view(), name='list-order'),
    url(r'^channel/(?P<pk>[0-9]+)/$',
        channel_views.ChannelViewDetail.as_view(
            {'get': 'retrieve',
             'put': 'update',
             'delete': 'destroy'}
        ),
        name='detail'),
    url(r'^post/(?P<pk>[0-9]+)/vote$', post_views.PostViewVote.as_view(), name='post-vote'),
)

urlpatterns += router.urls
