from django.utils import timezone
from django.db import models


class Channel(models.Model):
    """
    A channel
    """

    #: name of channel
    name = models.CharField(max_length=30, unique=True, blank=False)

    #: channel description
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)

    @property
    def get_name(self):
        return self.name

    @property
    def get_description(self):
        return self.description

    @property
    def get_slug(self):
        return self.slug


class Post(models.Model):
    """
    This is a post
    """

    #: The channel this post belongs to
    channel = models.ForeignKey(Channel, null=False)

    #: Post title
    title = models.CharField(max_length=30)

    #: Post text
    text = models.TextField(blank=False)

    #: Amount of votes
    votes = models.IntegerField(null=False, default=0)

    #: The date this post was published on
    publish_date = models.DateTimeField(default=timezone.now, null=False)

    class Meta:
        unique_together = ('channel', 'title')

    def __str__(self):
        return self.title

    @property
    def get_text(self):
        return self.text

    @property
    def get_vores(self):
        return self.votes

    @property
    def get_publish_date(self):
        return self.publish_date


class Comment(models.Model):
    """
    This is a comment
    """

    #: The post this comment belongs to
    post = models.ForeignKey(Post, null=False)

    #: comment text
    text = models.TextField(blank=False)

    #: The date this comment was published on
    publish_date = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return self.post.title + ' -comment'

    @property
    def get_text(self):
        return self.text

    @property
    def get_publish_date(self):
        return self.publish_date
