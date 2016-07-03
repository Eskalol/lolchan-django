from django_cradmin.viewhelpers import listbuilder
from django_cradmin import crapp
from django_cradmin.viewhelpers import listbuilderview, listfilter
from django_cradmin.crinstance import reverse_cradmin_url
from lolchan.lolchan_core.models import Channel


class ChannelItemFrame(listbuilder.itemframe.Link):
    valuealias = 'channel'

    def get_url(self):
        return reverse_cradmin_url(instanceid='channel',
                                   appname='channel',
                                   roleid=self.channel.id,
                                   viewname=crapp.INDEXVIEW_NAME)


class ChannelItemValue(listbuilder.itemvalue.TitleDescription):
    valuealias = 'channel'

    def __init__(self, value):
        super(ChannelItemValue, self).__init__(value)

    def get_extra_css_classes_list(self):
        css_classes_list = super(ChannelItemValue, self).get_extra_css_classes_list()
        return css_classes_list

    def get_title(self):
        return self.channel.name

    def get_description(self):
        return self.channel.description


class DefaultChannelOrder(listfilter.django.single.select.AbstractOrderBy):
    pass
    def get_ordering_options(self):
        return [
            ('', {
                'label': 'Name',
                'order_by': ['name'],
            }),
            ('name_descending', {
                'label': 'Name (descending)',
                'order_by': ['-name'],
            }),
        ]


class LobbyView(listbuilderview.FilterListMixin, listbuilderview.View):
    model = Channel
    value_renderer_class = ChannelItemValue
    frame_renderer_class = ChannelItemFrame

    def get_pagetitle(self):
        return 'Lobby'

    def add_filterlist_items(self, filterlist):
        filterlist.append(listfilter.django.single.textinput.Search(
            slug='Search',
            label='Search',
            label_is_screenreader_only=True,
            modelfields=['name']))
        filterlist.append(DefaultChannelOrder(
            slug='orderby',
            label='Order by'))

    def get_filterlist_url(self, filters_string):
        return self.request.cradmin_app.reverse_appurl(
            'filter', kwargs={'filters_string': filters_string})

    def get_unfiltered_queryset_for_role(self, role):
        return Channel.objects.all()


class App(crapp.App):
    appurls = [
        crapp.Url(r'^$', LobbyView.as_view(), name=crapp.INDEXVIEW_NAME),
        crapp.Url(r'^filter/(?P<filters_string>.+)?$',
                  LobbyView.as_view(),
                  name='filter'),

    ]