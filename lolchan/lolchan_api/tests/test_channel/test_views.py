from django import test
from model_mommy import mommy


from lolchan.lolchan_api.channel.views import ChannelViewList, ChannelViewDetail, ChannelViewListOrder
from lolchan.lolchan_api.tests import test_api_mixins


class TestChannelViewList(test_api_mixins.TestCaseMixin, test.TestCase):
    viewclass = ChannelViewList
    route = '/channel/'

    def test_get_sanity(self):
        testchannel = mommy.make('lolchan_core.Channel', name='Test')
        response = self.mock_get_request()
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            [{
                'id': testchannel.id,
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
        self.assertEqual(200, response.status_code)
        names = [channeldict['name'] for channeldict in response.data]
        self.assertEqual(['A', 'B', 'C'], names)


class TestChannelViewListOrder(test_api_mixins.TestCaseMixin, test.TestCase):
    viewclass = ChannelViewListOrder
    route = r'^channel/(?P<order>.+)/list-order-by$'

    def test_get_sanity(self):
        mommy.make('lolchan_core.Channel', name='A')
        response = self.mock_get_request(order='name')
        self.assertEqual(200, response.status_code)
        self.assertEqual('A', response.data[0]['name'])

    def test_order_by_name_asc(self):
        mommy.make('lolchan_core.Channel', description='AAA')
        mommy.make('lolchan_core.Channel', description='BBB')
        mommy.make('lolchan_core.Channel', description='CCC')
        response = self.mock_get_request(order='description')
        self.assertEqual(200, response.status_code)
        descriptions = [channeldict['description'] for channeldict in response.data]
        self.assertEqual(['AAA', 'BBB', 'CCC'], descriptions)

    def test_order_by_name_desc(self):
        mommy.make('lolchan_core.Channel', id=1337)
        mommy.make('lolchan_core.Channel', id=230)
        mommy.make('lolchan_core.Channel', id=10)
        response = self.mock_get_request(order='-id')
        self.assertEqual(200, response.status_code)
        ids = [channeldict['id'] for channeldict in response.data]
        self.assertEqual([1337, 230, 10], ids)


class TestChannelViewDetail(test_api_mixins.TestCaseMixin, test.TestCase):
    viewclass = ChannelViewDetail
    route = r'^channel/(?P<pk>[0-9]+)/$'
    is_viewset = True

    def test_get_sanity(self):
        testchannel = mommy.make('lolchan_core.Channel', pk=1)
        response = self.mock_get_request(pk=1)
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                'id': testchannel.id,
                'name': testchannel.name,
                'description': testchannel.description,
            },
            response.data
        )

    def test_delete_anonymous_user(self):
        testchannel = mommy.make('lolchan_core.Channel', pk=1)
        response = self.mock_delete_request(pk=1)
        self.assertEqual(403, response.status_code)
        response = self.mock_get_request(pk=1)
        self.assertEqual(200, response.status_code)
        self.assertEqual(testchannel.name, response.data['name'])

    def test_delete_admin_user(self):
        mommy.make('lolchan_core.Channel', pk=1)
        response = self.mock_delete_request(requestuser=self.create_admin_user(), pk=1)
        self.assertEqual(204, response.status_code)
        response = self.mock_get_request(pk=1)
        self.assertEqual(404, response.status_code)
