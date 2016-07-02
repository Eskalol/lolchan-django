from django_cradmin import crinstance
from django_cradmin import crmenu

from lolchan.lolchan_channel.views import channelview
from lolchan.lolchan_core.models import Channel, Post


class Menu(crmenu.Menu):
    def build_menu(self):
        self.add_headeritem(label='channel',
                            url=self.appindex_url('channel'),
                            active=self.request.cradmin_app.appname == 'channel')


class BaseCrinstance(crinstance.BaseCrAdminInstance):
    roleclass = Channel
    menuclass = Menu
    rolefrontpage_appname = 'channel'
    id = 'channel'
    apps = [
        ('channel', channelview.App)
    ]
    flatten_rolefrontpage_url = True

    def get_rolequeryset(self):
        return Channel.objects.all()

    def has_access(self):
        return True

    @classmethod
    def matches_urlpath(cls, urlpath):
        return urlpath.startswith('/channel')

    def get_titletext_for_role(self, role):
        return str(role)
