from rest_framework.test import APIRequestFactory


class TestCaseMixin(object):
    route = None
    viewclass = None

    def __get_method(self, method):
        return {
            'list': ({'get': 'list'}, APIRequestFactory().get(self.route)),
            'retrieve': ({'get': 'retrieve'}, APIRequestFactory().get(self.route)),
            'update': ({'put': 'update'}, APIRequestFactory().put(self.route)),
            'partial_update': ({'patch': 'partial_update'}, APIRequestFactory().patch(self.route)),
            'destroy': ({'delete': 'destroy'}, APIRequestFactory().delete(self.route)),
        }.get(method, ({'get': 'list'}, APIRequestFactory().get(self.route)))

    def __mock_request(self, method, **kwargs):
        method, request = self.__get_method(method)
        view = self.viewclass.as_view(method)
        return view(request, **kwargs)

    def mock_get_request(self, method='list', **kwargs):
        return self.__mock_request(method, **kwargs)

    def mock_delete_request(self, **kwargs):
        return self.__mock_request('destroy', **kwargs)

    def mock_put_request(self, **kwargs):
        return self.__mock_request('update', **kwargs)
