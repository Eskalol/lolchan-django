from django_cradmin import crinstance
from django_cradmin import crmenu
from django_cradmin.decorators import has_access_to_cradmin_instance

from lolchan.lolchan_lobby.views import lobby_view


class Menu(crmenu.Menu):
    def build_menu(self):
        self.add_headeritem(label='lobby',
                            url=self.appindex_url('lobby'),
                            active=self.request.cradmin_app.appname == 'lobby')


class BaseCrinstance(crinstance.BaseCrAdminInstance):

    menuclass = Menu
    rolefrontpage_appname = 'lobby'
    flatten_rolefrontpage_url = True
    id = 'lobby'
    apps = [
        ('lobby', lobby_view.App),
    ]

    def has_access(self):
        return True

    @classmethod
    def matches_urlpath(cls, urlpath):
        return urlpath.startswith('/lobby/')

    def get_titletext_for_role(self, role):
        return str(role)