from rest_framework.test import APIRequestFactory


class TestCaseMixin(object):
    route = None
    viewclass = None

    def mock_get_request(self, **kwargs):
        factory = APIRequestFactory()
        request = factory.get(self.route, **kwargs)
        response = self.viewclass.as_view({'get': 'list'})(request)
        return response