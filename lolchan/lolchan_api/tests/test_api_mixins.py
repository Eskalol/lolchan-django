from rest_framework.test import APIRequestFactory
from django.conf import settings
from model_mommy import mommy


class TestCaseMixin(object):
    route = None
    viewclass = None
    is_viewset = False

    def get_request(self, method,
                    requestuser=None, **kwargs):
        request = {
            'get': APIRequestFactory().get(self.route),
            'delete': APIRequestFactory().delete(self.route),
        }[method]
        if requestuser:
            request.user = requestuser
        return request, kwargs

    def create_admin_user(self):
        return mommy.make(settings.AUTH_USER_MODEL, is_superuser=True, is_active=True)

    def mock_delete_request(self, **kwargs):
        request, new_kwargs = self.get_request('delete', **kwargs)
        if self.is_viewset:
            view = self.viewclass.as_view({'delete': 'delete'})
        else:
            view = self.viewclass.as_view()
        response = view(request, **new_kwargs)
        return response

    def mock_get_request(self, **kwargs):
        request, new_kwargs = self.get_request('get', **kwargs)
        if self.is_viewset:
            view = self.viewclass.as_view({'get': 'get'})
        else:
            view = self.viewclass.as_view()
        response = view(request, **new_kwargs)
        return response
