from django.utils import timezone
from django.db import models


class Channel(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False)
    description = models.TextField(blank=True, default='')
    slug = models.SlugField(max_length=255, unique=True)

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
    channel = models.ForeignKey(Channel, null=False)
    title = models.CharField(max_length=30)
    text = models.TextField(blank=False)
    votes = models.IntegerField(null=False, default=0)
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
    post = models.ForeignKey(Post, null=False)
    text = models.TextField(blank=False)
    publish_date = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return self.post.title + ' -comment'

    @property
    def get_text(self):
        return self.text

    @property
    def get_publish_date(self):
        return self.publish_date
