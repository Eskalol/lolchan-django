from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from django_cradmin import cradmin_testhelpers
from model_mommy import mommy

from lolchan.lolchan_lobby.views import lobbyview


class TestLobbyview(TestCase, cradmin_testhelpers.TestCaseMixin):
    viewclass = lobbyview.LobbyView

    def test_channel_name(self):
        mommy.make('lolchan_core.channel', name='Cats')
        mockresponse = self.mock_http200_getrequest_htmls()
        self.assertEqual('Cats', mockresponse.selector.one(
            '.django-cradmin-listbuilder-itemvalue-titledescription-title').alltext_normalized)

    def test_multiple_channel_names(self):
        mommy.make('lolchan_core.channel', name='Cats')
        mommy.make('lolchan_core.channel', name='Doge')
        mockresponse = self.mock_http200_getrequest_htmls()
        channel_names = mockresponse.selector.list(
            '.django-cradmin-listbuilder-itemvalue-titledescription-title')
        channel_names = [x.alltext_normalized for x in channel_names]
        self.assertIn('Cats', channel_names)
        self.assertIn('Doge', channel_names)

    def test_channel_count(self):
        mommy.make('lolchan_core.channel')
        mommy.make('lolchan_core.channel')
        mommy.make('lolchan_core.channel')
        mockresponse = self.mock_http200_getrequest_htmls()
        channels = mockresponse.selector.list(
            '.django-cradmin-listbuilder-itemvalue-titledescription-title')
        self.assertEqual(3, len(channels))

    def test_filter_name_order_descending(self):
        mommy.make('lolchan_core.channel', name='Cats')
        mommy.make('lolchan_core.channel', name='Doge')
        mockresponse = self.mock_http200_getrequest_htmls(viewkwargs={'filters_string': 'orderby-name_descending'})
        result_list = mockresponse.selector.list('.django-cradmin-listbuilder-itemvalue-titledescription-title')
        self.assertEqual('Doge', result_list[0].alltext_normalized)
        self.assertEqual('Cats', result_list[1].alltext_normalized)

    def test_filter_search(self):
        mommy.make('lolchan_core.channel', name='Doge')
        mommy.make('lolchan_core.channel', name='Cats')
        mommy.make('lolchan_core.channel', name='Imba')
        mockresponse = self.mock_http200_getrequest_htmls(viewkwargs={'filters_string': 'Search-c'})
        self.assertEqual('Cats', mockresponse.selector.one(
            '.django-cradmin-listbuilder-itemvalue-titledescription-title').alltext_normalized)

    def test_filter_order_and_search(self):
        mommy.make('lolchan_core.channel', name='Doge')
        mommy.make('lolchan_core.channel', name='Cats')
        mommy.make('lolchan_core.channel', name='Imba')
        mommy.make('lolchan_core.channel', name='Cool')
        mommy.make('lolchan_core.channel', name='Cola')
        mockresponse = self.mock_http200_getrequest_htmls(viewkwargs={'filters_string': 'Search-c/orderby-name_descending'})
        result_list = mockresponse.selector.list('.django-cradmin-listbuilder-itemvalue-titledescription-title')
        self.assertEqual('Cool', result_list[0].alltext_normalized)
        self.assertEqual('Cola', result_list[1].alltext_normalized)
        self.assertEqual('Cats', result_list[2].alltext_normalized)