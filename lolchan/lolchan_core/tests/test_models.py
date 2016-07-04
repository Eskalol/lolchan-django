from django.test import TestCase
from lolchan.lolchan_core.models import *
from model_mommy import mommy
from django.db.utils import IntegrityError


class TestChannelModel(TestCase):

    def test_unique_channel_name(self):
        with self.assertRaisesMessage(IntegrityError, ''):
            mommy.make('lolchan_core.channel', name='Cats')
            mommy.make('lolchan_core.channel', name='Cats')


class TestPostModel(TestCase):

    def test_post_title_unique_to_channel(self):
        testchannel = mommy.make('lolchan_core.channel')
        with self.assertRaisesMessage(IntegrityError, ''):
            mommy.make('lolchan_core.Post', title='Funny cats', channel=testchannel)
            mommy.make('lolchan_core.Post', title='Funny cats', channel=testchannel)
