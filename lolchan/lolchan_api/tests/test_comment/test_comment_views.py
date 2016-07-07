from django import test
from model_mommy import mommy
from lolchan.lolchan_api.comment.views import CommentView, CommentViewList
from lolchan.lolchan_api.tests import api_test_helper
from lolchan.lolchan_core.models import Comment


class TestCommentView(api_test_helper.TestCaseMixin, test.TestCase):
    viewclass = CommentView
    route = '/comment/'

    def test_sanity(self):
        testcomment = mommy.make('lolchan_core.Comment')
        response = self.mock_get_request(queryparams='?id={}'.format(testcomment.id))
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                'text': testcomment.text,
                'publish_date': testcomment.publish_date.isoformat(),
                'post': testcomment.post.id
            },
            response.data
        )

    def test_permission_anonymous_user_delete(self):
        testcomment = mommy.make('lolchan_core.Comment')
        response = self.mock_delete_request(queryparams='?id={}'.format(testcomment.id))
        self.assertEqual(403, response.status_code)

    def test_permission_admin_user_delete(self):
        testcomment = mommy.make('lolchan_core.Comment')
        response = self.mock_delete_request(queryparams='?id={}'.format(testcomment.id),
                                            requestuser=self.create_admin_user())
        self.assertEqual(204, response.status_code)
        response = self.mock_get_request(queryparams='?id={}'.format(testcomment.id))
        self.assertEqual(404, response.status_code)
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(pk=testcomment.id)

    def test_create_comment(self):
        testpost = mommy.make('lolchan_core.Post')
        response = self.mock_post_request(
            data={
                'text': 'so cool doge',
                'post': testpost.id,
            })
        self.assertEqual(201, response.status_code)
        self.assertEqual(response.data['text'], 'so cool doge')
        self.assertIsNotNone(Comment.objects.filter(text='so cool doge', post=testpost))


class TestCommentViewList(api_test_helper.TestCaseMixin, test.TestCase):
    viewclass = CommentViewList
    route = '/comment/list'

    def test_sanity(self):
        testcomment = mommy.make('lolchan_core.Comment')
        response = self.mock_get_request()
        self.assertEqual(
            [{
                'text': testcomment.text,
                'publish_date': testcomment.publish_date.isoformat(),
                'post': testcomment.post.id
            }],
            response.data
        )

    def test_404(self):
        mommy.make('lolchan_core.Comment',
                   post=mommy.make('lolchan_core.Post', title='Cate'))
        response = self.mock_get_request(queryparams='?post=Doge')
        self.assertEqual(404, response.status_code)

    def test_queryparams_channel_post_order_desc(self):
        post = mommy.make('lolchan_core.Post',
                          channel=mommy.make('lolchan_core.Channel', name='Doge'),
                          title='Doge-memes')
        mommy.make('lolchan_core.Comment', post=post, text='A')
        mommy.make('lolchan_core.Comment', post=post, text='B')
        mommy.make('lolchan_core.Comment', post=post, text='C')
        mommy.make('lolchan_core.Comment')
        mommy.make('lolchan_core.Comment')
        mommy.make('lolchan_core.Comment')
        response = self.mock_get_request(queryparams='?channel=Doge&post=Doge-memes&order=-text')
        self.assertEqual(200, response.status_code)
        texts = [commentDict['text'] for commentDict in response.data]
        self.assertListEqual(texts, ['C', 'B', 'A'])

    def test_queryparams_channel_post_order_asc(self):
        post = mommy.make('lolchan_core.Post',
                          channel=mommy.make('lolchan_core.Channel', name='Doge'),
                          title='Doge-memes')
        mommy.make('lolchan_core.Comment', post=post, text='A')
        mommy.make('lolchan_core.Comment', post=post, text='B')
        mommy.make('lolchan_core.Comment', post=post, text='C')
        mommy.make('lolchan_core.Comment')
        mommy.make('lolchan_core.Comment')
        mommy.make('lolchan_core.Comment')
        response = self.mock_get_request(queryparams='?channel=Doge&post=Doge-memes&order=text')
        self.assertEqual(200, response.status_code)
        texts = [commentDict['text'] for commentDict in response.data]
        self.assertListEqual(texts, ['A', 'B', 'C'])
