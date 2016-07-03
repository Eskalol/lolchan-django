from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from django_cradmin import cradmin_testhelpers
from model_mommy import mommy

from lolchan.lolchan_channel.views import channelview


class TestChannelview(TestCase, cradmin_testhelpers.TestCaseMixin):
    viewclass = channelview.ChannelView

    def test_post_name(self):
        channel = mommy.make('lolchan_core.Channel')
        mommy.make('lolchan_core.Post', channel=channel, title='Doge is life')
        mockresponse = self.mock_http200_getrequest_htmls(cradmin_role=channel)
        self.assertEqual('Doge is life',
                         mockresponse.selector.one('.lolchan-channel-post-title').alltext_normalized)

    def test_post_description(self):
        channel = mommy.make('lolchan_core.Channel')
        mommy.make('lolchan_core.Post', channel=channel, text='So scare')
        mockresponse = self.mock_http200_getrequest_htmls(cradmin_role=channel)
        self.assertEqual('So scare',
                         mockresponse.selector.one('.lolchan-channel-post-description').alltext_normalized)

    def test_post_count(self):
        channel = mommy.make('lolchan_core.Channel')
        mommy.make('lolchan_core.Post', channel=channel)
        mommy.make('lolchan_core.Post', channel=channel)
        mommy.make('lolchan_core.Post', channel=channel)
        mommy.make('lolchan_core.Post', channel=mommy.make('lolchan_core.Channel'))
        mockresponse = self.mock_http200_getrequest_htmls(cradmin_role=channel)
        self.assertEqual(3, len(mockresponse.selector.list('.lolchan-channel-post')))

    def test_post_positive_votes(self):
        channel = mommy.make('lolchan_core.Channel')
        mommy.make('lolchan_core.Post', channel=channel, votes=30)
        mockresponse = self.mock_http200_getrequest_htmls(cradmin_role=channel)
        self.assertEqual('30', mockresponse.selector.one('.lolchan-channel-post-votes').alltext_normalized)

    def test_post_negative_votes(self):
        channel = mommy.make('lolchan_core.Channel')
        mommy.make('lolchan_core.Post', channel=channel, votes=-150)
        mockresponse = self.mock_http200_getrequest_htmls(cradmin_role=channel)
        self.assertEqual('-150', mockresponse.selector.one('.lolchan-channel-post-votes').alltext_normalized)
