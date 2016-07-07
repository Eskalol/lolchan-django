from rest_framework.permissions import BasePermission


class IsAuthenticatedOrReadOnly(BasePermission):
    SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return (request.method in self.SAFE_METHODS or
                request.user and
                request.user.is_authenticated())


class PostViewPermission(IsAuthenticatedOrReadOnly):
    SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS', 'POST']


class PostViewUpdateDestroy(IsAuthenticatedOrReadOnly):
    SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS', 'PATCH']

class CommentViewPermission(IsAuthenticatedOrReadOnly):
    SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS', 'POST']