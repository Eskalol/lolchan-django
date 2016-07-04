from rest_framework import routers

from lolchan.lolchan_api.channel.views import ChannelViewSet


router = routers.DefaultRouter()
router.register(r'channel', ChannelViewSet,
                base_name='lolchan-api-channel')

urlpatterns = router.urls
