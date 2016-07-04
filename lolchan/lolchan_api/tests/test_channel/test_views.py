from django import test
from model_mommy import mommy
from rest_framework.test import APIRequestFactory

from lolchan.lolchan_api.channel.views import ChannelViewSet
from lolchan.lolchan_api.tests import test_api_mixins


class TestChannelViewSet(test.TestCase, test_api_mixins.TestCaseMixin):
    viewclass = ChannelViewSet
    route = '/channel/'

    def test_get_sanity(self):
        testchannel = mommy.make('lolchan_core.Channel',
                                 name='Test',
                                 slug='test')
        response = self.mock_get_request()
        self.assertEqual(200, response.status_code)
        print(response.data)
        self.assertEqual(
            [{
                'id': testchannel.id,
                'slug': testchannel.slug,
                'name': testchannel.name,
                'description': testchannel.description,
            }],
            response.data
        )

    def test_ordering(self):
        mommy.make('lolchan_core.Channel', name='A')
        mommy.make('lolchan_core.Channel', name='B')
        mommy.make('lolchan_core.Channel', name='C')
        response = self.mock_get_request()
        names = [channeldict['name'] for channeldict in response.data]
        self.assertEqual(['A', 'B', 'C'], names)

    def test_get_retreive(self):
        channel = mommy.make('lolchan_core.Channel', pk='1')
        response = self.mock_get_request(method='retrieve', pk=channel.pk)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        channel = mommy.make('lolchan_core.Channel', pk='1')
        response = self.mock_delete_request(pk=channel.pk)
        self.assertEqual(response.status_code, 204)

    def test_update(self):
        channel = mommy.make('lolchan_core.Channel', pk='1', name='imba')
        response = self.mock_put_request(pk=channel.pk,
                                         name='lol',
                                         slug=channel.slug,
                                         description=channel.description)
        print(response.data)
        self.assertNotEqual(response.data['name'], 'imba')
        self.assertEqual(response.data['name'], 'lol')