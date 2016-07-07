from django import test
from model_mommy import mommy
from lolchan.lolchan_api.post.views import PostListFilterView, PostUpdateDestroyView
from lolchan.lolchan_api.tests import api_test_helper
from lolchan.lolchan_core.models import Post


class TestPostListFilterVIew(api_test_helper.TestCaseMixin, test.TestCase):
    viewclass = PostListFilterView
    route = '/post/'

    def test_get_sanity(self):
        testpost = mommy.make('lolchan_core.Post')
        response = self.mock_get_request()
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            [{
                'title': testpost.title,
                'text': testpost.text,
                'votes': testpost.votes,
                'publish_date': testpost.publish_date.isoformat(),
                'channel': testpost.channel.id
            }],
            response.data
        )

    def test_get_on_id(self):
        mommy.make('lolchan_core.Post', id=2)
        testpost = mommy.make('lolchan_core.Post',
                              channel=mommy.make('lolchan_core.Channel'),
                              id=1)
        response = self.mock_get_request(queryparams='?id=1')
        self.assertEqual(200, response.status_code)
        self.assertEqual([{
                'title': testpost.title,
                'text': testpost.text,
                'votes': testpost.votes,
                'publish_date': testpost.publish_date.isoformat(),
                'channel': testpost.channel.id
            }],
            response.data)

    def test_get_id_404(self):
        mommy.make('lolchan_core.Post', id=1)
        response = self.mock_get_request(queryparams='?id=200')
        self.assertEqual(404, response.status_code)

    def test_get_text_404(self):
        mommy.make('lolchan_core.Post',
                   channel=mommy.make('lolchan_core.Channel', name='lol'),
                   title='lol', text='heia')
        response = self.mock_get_request(queryparams='?text=doge')
        self.assertEqual(404, response.status_code)

    def test_get_queryparam_text_title(self):
        mommy.make('lolchan_core.Post', title='doge')
        mommy.make('lolchan_core.Post', title='cool doge')
        mommy.make('lolchan_core.Post', title='imba')
        response = self.mock_get_request(queryparams='?text=doge')
        self.assertEqual(200, response.status_code)
        titles_response = [postdict['title'] for postdict in response.data]
        self.assertListEqual(sorted(titles_response), ['cool doge', 'doge'])

    def test_get_queryparam_text_text(self):
        mommy.make('lolchan_core.Post', text='doge')
        mommy.make('lolchan_core.Post', text='cool doge')
        mommy.make('lolchan_core.Post', text='imba')
        response = self.mock_get_request(queryparams='?text=doge')
        self.assertEqual(200, response.status_code)
        text_response = [postdict['text'] for postdict in response.data]
        self.assertListEqual(sorted(text_response), ['cool doge', 'doge'])

    def test_get_queryparam_text_channel_name(self):
        testchannel = mommy.make('lolchan_core.Channel', name='doge')
        mommy.make('lolchan_core.Post', channel=testchannel)
        mommy.make('lolchan_core.Post', channel=testchannel)
        mommy.make('lolchan_core.Post',
                   channel=mommy.make('lolchan_core.Channel', name='lol'),
                   title='lol', text='heia')
        response = self.mock_get_request(queryparams='?text=doge')
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data))

    def test_post(self):
        channel = mommy.make('lolchan_core.Channel')
        response = self.mock_post_request(
            data={
                'title': 'Doge so cool',
                'text': 'Doge is cool, Cate is not',
                'channel': channel.id
            })
        self.assertEqual(201, response.status_code)
        self.assertEqual('Doge so cool', response.data['title'])
        text_db = Post.objects.filter(title='Doge so cool').values('text')[0]['text']
        self.assertEqual(response.data['text'], text_db)

    def test_post_invalid_data(self):
        channel = mommy.make('lolchan_core.Channel')
        response = self.mock_post_request(
            data={
                'invalidfield': 'Doge so cool',
                'invalidtext': 'Doge is cool, Cate is not',
                'channel': channel.id
            })
        self.assertEqual(400, response.status_code)

    def test_post_invalid_number_of_votes(self):
        channel = mommy.make('lolchan_core.Channel')
        response = self.mock_post_request(
            data={
                'title': 'Doge so cool',
                'text': 'Doge is cool, Cate is not',
                'channel': channel.id,
                'votes': 10000
            })
        self.assertEqual(201, response.status_code)
        self.assertEqual(0, response.data['votes'])
        votes_db = Post.objects.filter(title='Doge so cool').values('votes')[0]['votes']
        self.assertEqual(response.data['votes'], votes_db)


class TestPostUpdateDestroyView(api_test_helper.TestCaseMixin, test.TestCase):
    viewclass = PostUpdateDestroyView
    route = '/post/update-delete/'

    def test_get_sanity(self):
        testpost = mommy.make('lolchan_core.Post', text='hei', title='lol')
        response = self.mock_get_request(queryparams='?id={}'.format(testpost.id))
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                'title': testpost.title,
                'text': testpost.text,
                'votes': testpost.votes,
                'publish_date': testpost.publish_date.isoformat(),
                'channel': testpost.channel.id
            },
            response.data
        )

    def test_404(self):
        response = self.mock_get_request(queryparams='?id=1337')
        self.assertEqual(404, response.status_code)

    def test_permission_anonymous_destroy(self):
        testpost = mommy.make('lolchan_core.Post')
        response = self.mock_delete_request(queryparams='?id={}'.format(testpost.id))
        self.assertEqual(403, response.status_code)

    def test_permission_admin_destroy(self):
        testpost = mommy.make('lolchan_core.Post')
        response = self.mock_delete_request(queryparams='?id={}'.format(testpost.id),
                                            requestuser=self.create_admin_user())
        self.assertEqual(204, response.status_code)
        response = self.mock_get_request(queryparams='?id={}'.format(testpost.id))
        self.assertEqual(404, response.status_code)
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(pk=testpost.id)

    def test_update_voteup_only_votes_field_changed(self):
        testpost = mommy.make('lolchan_core.Post')
        response = self.mock_patch_request(
            queryparams='?id={}'.format(testpost.id),
            data={
                'text': 'hei',
                'title': 'cool',
                'votes': 1000,
            })
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                'text': testpost.text,
                'title': testpost.title,
                'votes': testpost.votes + 1,
                'channel': testpost.channel.id,
                'publish_date': testpost.publish_date.isoformat()
            },
            response.data
        )

    def test_update_votdown_only_votes_field_changed(self):
        testpost = mommy.make('lolchan_core.Post')
        response = self.mock_patch_request(
            queryparams='?id={}'.format(testpost.id),
            data={
                'title': 'cool',
                'votes': -1000,
            })
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                'text': testpost.text,
                'title': testpost.title,
                'votes': testpost.votes - 1,
                'channel': testpost.channel.id,
                'publish_date': testpost.publish_date.isoformat()
            },
            response.data
        )

    def test_update_vote_zero_only_votes_field_changed(self):
        testpost = mommy.make('lolchan_core.Post')
        response = self.mock_patch_request(
            queryparams='?id={}'.format(testpost.id),
            data={
                'votes': 0,
            })
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                'text': testpost.text,
                'title': testpost.title,
                'votes': testpost.votes,
                'channel': testpost.channel.id,
                'publish_date': testpost.publish_date.isoformat()
            },
            response.data
        )
