from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from django_cradmin import cradmin_testhelpers
from model_mommy import mommy

from lolchan.lolchan_lobby.views import lobbyview


class TestLobbyview(TestCase, cradmin_testhelpers.TestCaseMixin):
    viewclass = lobbyview.LobbyView

    def test_channel_name(self):
        mommy.make('lolchan_core.Channel', name='Cats')
        mockresponse = self.mock_http200_getrequest_htmls()
        self.assertEqual('Cats',
                         mockresponse.selector.one(
                             '.django-cradmin-listbuilder-itemvalue-titledescription-title').alltext_normalized)

    def test_multiple_channel_names(self):
        mommy.make('lolchan_core.Channel', name='Cats')
        mommy.make('lolchan_core.Channel', name='Doge')
        mockresponse = self.mock_http200_getrequest_htmls()
        channel_names = mockresponse.selector.list(
            '.django-cradmin-listbuilder-itemvalue-titledescription-title')
        channel_names = [x.alltext_normalized for x in channel_names]
        self.assertIn('Cats', channel_names)
        self.assertIn('Doge', channel_names)

    def test_channel_count(self):
        mommy.make('lolchan_core.Channel')
        mommy.make('lolchan_core.Channel')
        mommy.make('lolchan_core.Channel')
        mockresponse = self.mock_http200_getrequest_htmls()
        channels = mockresponse.selector.list(
            '.django-cradmin-listbuilder-itemvalue-titledescription-title')
        self.assertEqual(3, len(channels))
