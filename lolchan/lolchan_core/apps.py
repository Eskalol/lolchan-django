from django.apps import AppConfig
from django_cradmin.superuserui import superuserui_registry


class LolChanCoreConfig(AppConfig):
    name = 'lolchan.lolchan_core'
    verbose_name = "lolchan core"

    def ready(self):
        appconfig = superuserui_registry.default.add_djangoapp(
            superuserui_registry.DjangoAppConfig(app_label='lolchan_core'))
        # page_model = self.get_model('Page')
        # appconfig.add_model(superuserui_registry.ModelConfig(model_class=page_model))
        appconfig.add_all_models()
