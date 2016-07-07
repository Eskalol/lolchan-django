from django.conf.urls import patterns, url, include
from rest_framework import routers

from lolchan.lolchan_api.channel import views as channel_views
from lolchan.lolchan_api.post import views as post_views
from lolchan.lolchan_api.comment import views as comment_views
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
    url(r'^post/$', post_views.PostListFilterView.as_view(), name='post'),
    url(r'^post/update-delete/$', post_views.PostUpdateDestroyView.as_view(), name='post-update/destroy'),
    url(r'^comment/list/$', comment_views.CommentViewList.as_view(), name='comment-list'),
    url(r'^comment/$', comment_views.CommentView.as_view(), name='comment'),
)

urlpatterns += router.urls
