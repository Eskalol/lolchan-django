from django_cradmin.viewhelpers import listbuilder
from django_cradmin import crapp
from django_cradmin.viewhelpers import listbuilderview
from lolchan.lolchan_core.models import Channel, Post

from crispy_forms import layout


class PostItemFrame(listbuilder.itemframe.DefaultSpacingItemFrame):
    pass


class PostItemValue(listbuilder.itemvalue.FocusBox):
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
    frame_renderer_class = PostItemFrame

    def get_pagetitle(self):
        return self.request.cradmin_role.name

    def get_queryset_for_role(self, role):
        return Post.objects.filter(channel=role).all()


class App(crapp.App):
    appurls = [
        crapp.Url(r'^$', ChannelView.as_view(), name=crapp.INDEXVIEW_NAME)
    ]
