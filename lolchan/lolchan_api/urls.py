from django.conf.urls import patterns, url, include
from rest_framework import routers

from lolchan.lolchan_api.channel import views

router = routers.DefaultRouter()

urlpatterns = patterns(
    url(r'^', include(router.urls)),
    url(r'^channel/$', views.ChannelViewList.as_view(), name='list'),
    url(r'^channel/(?P<order>.+)/list-order-by$', views.ChannelViewListOrder.as_view(), name='list-order'),
    url(r'^channel/(?P<pk>[0-9]+)/$',
        views.ChannelViewDetail.as_view(
            {'get': 'get',
             'put': 'put',
             'delete': 'delete'}
        ),
        name='detail'),
)

urlpatterns += router.urls
