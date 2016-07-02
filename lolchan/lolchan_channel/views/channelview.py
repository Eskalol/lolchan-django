from django_cradmin.viewhelpers import listbuilder
from django_cradmin import crapp
from django_cradmin.viewhelpers import listbuilderview
from lolchan.lolchan_core.models import Channel, Post


class PostItemValue(listbuilder.itemvalue.base.ItemValueRenderer):
    valuealias = 'post'
    template_name = 'lolchan_channel/listbuilder/postitemvalue.django.html'

    def __init__(self, value):
        super(PostItemValue, self).__init__(value)

    def get_extra_css_classes_list(self):
        css_classes_list = super(PostItemValue, self).get_extra_css_classes_list()
        return css_classes_list


class ChannelView(listbuilderview.View):
    model = Post
    value_renderer_class = PostItemValue

    def get_pagetitle(self):
        return 'this is a channel'

    def get_queryset_for_role(self, role):
        print(Post.objects.filter(channel=role).all())
        return Post.objects.filter(channel=role).all()


class App(crapp.App):
    appurls = [
        crapp.Url(r'^$', ChannelView.as_view(), name=crapp.INDEXVIEW_NAME)
    ]
