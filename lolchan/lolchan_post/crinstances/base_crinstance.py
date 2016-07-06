from django_cradmin import crinstance
from django_cradmin import crmenu

from lolchan.lolchan_post.views import postview
from lolchan.lolchan_core.models import Post, Comment


class Menu(crmenu.Menu):
    def build_menu(self):
        self.add_headeritem(label='lobby',
                            url=crinstance.reverse_cradmin_url(appname='lobby',
                                                               instanceid='lobby'))
        # self.add_headeritem(label=self.cradmin_instance.get_menu_label(),
        #                     active=self.request.cradmin_app.app_name == 'post')


class BaseCrinstance(crinstance.BaseCrAdminInstance):
    roleclass = Post
    menuclass = Menu
    rolefrontpage_appname = 'post'
    flatten_rolefrontpage_url = True
    id = 'post'
    apps = [
        ('post', postview.App)
    ]

    def has_access(self):
        return True

    @classmethod
    def matches_urlpath(cls, urlpath):
        return urlpath.startswith('/post')

    def get_rolequeryset(self):
        return Post.objects.all()

    def get_menu_label(self):
        return self.get_titletext_for_role(self.request.cradmin_role)

    def get_titletext_for_role(self, role):
        return str(role.title)