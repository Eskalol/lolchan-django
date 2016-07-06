from django import test
from model_mommy import mommy


from lolchan.lolchan_api.channel.views import ChannelViewList, ChannelViewDetail, ChannelViewListOrder
from lolchan.lolchan_api.tests import test_api_mixins
from lolchan.lolchan_core.models import Channel


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

    def test_post_permission_anonymous_user(self):
        response = self.mock_post_request(
            data={
                'name': 'imba',
                'description': 'wohoo',
            }
        )
        self.assertEqual(403, response.status_code)

    def test_post_permission_admin_user(self):
        response = self.mock_post_request(
            requestuser=self.create_admin_user(),
            data={
                'name': 'imba',
                'description': 'wohoo',
            }
        )
        self.assertEqual(201, response.status_code)
        self.assertEqual(
            {
                'name': 'imba',
                'description': 'wohoo'
            },
            {
                'name': response.data['name'],
                'description': response.data['description']
            }
        )

    def test_post_admin_response_db(self):
        response = self.mock_post_request(
            requestuser=self.create_admin_user(),
            data={
                'name': 'lol',
                'description': 'hei',
            }
        )
        self.assertEqual(201, response.status_code)
        channel = Channel.objects.get(pk=response.data['id'])
        self.assertEqual(response.data,
                         {
                             'id': channel.id,
                             'name': channel.name,
                             'description': channel.description
                         })

    def test_post_invalid_data(self):
        response = self.mock_post_request(
            requestuser=self.create_admin_user(),
            data={
                'description': 'hei',
            }
        )
        self.assertEqual(400, response.status_code)

    def test_post_invalid_field(self):
        response = self.mock_post_request(
            requestuser=self.create_admin_user(),
            data={
                'somefield': 'hei',
            }
        )
        self.assertEqual(400, response.status_code)


class TestChannelViewListOrder(test_api_mixins.TestCaseMixin, test.TestCase):
    viewclass = ChannelViewListOrder
    route = r'^channel/(?P<order>.+)/list-order-by$'

    def test_get_sanity(self):
        mommy.make('lolchan_core.Channel', name='A')
        response = self.mock_get_request(order='name')
        self.assertEqual(200, response.status_code)
        self.assertEqual('A', response.data[0]['name'])

    def test_order_by_description_asc(self):
        mommy.make('lolchan_core.Channel', description='AAA')
        mommy.make('lolchan_core.Channel', description='BBB')
        mommy.make('lolchan_core.Channel', description='CCC')
        response = self.mock_get_request(order='description')
        self.assertEqual(200, response.status_code)
        descriptions = [channeldict['description'] for channeldict in response.data]
        self.assertEqual(['AAA', 'BBB', 'CCC'], descriptions)

    def test_order_by_id_desc(self):
        mommy.make('lolchan_core.Channel', id=1337)
        mommy.make('lolchan_core.Channel', id=230)
        mommy.make('lolchan_core.Channel', id=10)
        response = self.mock_get_request(order='-id')
        self.assertEqual(200, response.status_code)
        ids = [channeldict['id'] for channeldict in response.data]
        self.assertEqual([1337, 230, 10], ids)

    def test_invalid_field(self):
        mommy.make('lolchan_core.Channel')
        mommy.make('lolchan_core.Channel')
        mommy.make('lolchan_core.Channel')
        response = self.mock_get_request(order='somefield')
        self.assertEqual(400, response.status_code)


class TestChannelViewDetail(test_api_mixins.TestCaseMixin, test.TestCase):
    viewclass = ChannelViewDetail
    route = r'^channel/(?P<pk>[0-9]+)/$'
    is_viewset = True

    def test_get_sanity(self):
        testchannel = mommy.make('lolchan_core.Channel', pk=1)
        response = self.mock_get_request(method='retrieve', pk=1)
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                'id': testchannel.id,
                'name': testchannel.name,
                'description': testchannel.description,
            },
            response.data
        )

    def test_destroy_permission_anonymous_user(self):
        testchannel = mommy.make('lolchan_core.Channel', pk=1)
        response = self.mock_delete_request(method='destroy', pk=1)
        self.assertEqual(403, response.status_code)
        response = self.mock_get_request(method='retrieve', pk=1)
        self.assertEqual(200, response.status_code)
        self.assertEqual(testchannel.name, response.data['name'])

    def test_destroy_permission_admin_user(self):
        mommy.make('lolchan_core.Channel', pk=1)
        response = self.mock_delete_request(method='destroy', requestuser=self.create_admin_user(), pk=1)
        self.assertEqual(204, response.status_code)
        response = self.mock_get_request(method='retrieve', pk=1)
        self.assertEqual(404, response.status_code)

    def test_update_permission_anonymous_user(self):
        mommy.make('lolchan_core.Channel', pk=1, description='heia')
        response = self.mock_put_request(method='update', pk=1, data={'description': 'imbalol'})
        self.assertEqual(403, response.status_code)
        self.assertEqual(Channel.objects.get(id=1).description, 'heia')

    def test_update_admin_user_response_data(self):
        mommy.make('lolchan_core.Channel', pk=1, description='heia')
        response = self.mock_put_request(method='update',
                                         requestuser=self.create_admin_user(),
                                         pk=1, data={'description': 'imbalol'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data['description'], 'imbalol')

    def test_update_admin_user_db_data(self):
        mommy.make('lolchan_core.Channel', pk=1, description='heia')
        response = self.mock_put_request(method='update',
                                         requestuser=self.create_admin_user(),
                                         pk=1, data={'description': 'imbalol'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(Channel.objects.get(id=1).description, 'imbalol')

    def test_get_invalid_pk(self):
        mommy.make('lolchan_core.Channel', pk=1)
        response = self.mock_get_request(method='retrieve', pk=200)
        self.assertEqual(404, response.status_code)

    def test_update_invalid_pk(self):
        mommy.make('lolchan_core.Channel', pk=1)
        response = self.mock_put_request(method='update',
                                         requestuser=self.create_admin_user(),
                                         pk=200, data={'description': 'imbalol'})
        self.assertEqual(404, response.status_code)

    def test_destroy_invalid_pk(self):
        mommy.make('lolchan_core.Channel', pk=1)
        response = self.mock_delete_request(method='destroy',
                                            requestuser=self.create_admin_user(),
                                            pk=200)
        self.assertEqual(404, response.status_code)

    """
        TODO: one testcase missing, test_update with invalid field, need to fix serializer
    """
