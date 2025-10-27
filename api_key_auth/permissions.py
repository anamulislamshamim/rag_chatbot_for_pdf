# permissions.py
from rest_framework.permissions import BasePermission
from rest_framework import exceptions

class HasAPIKey(BasePermission):
    """
    Allows access only if the request was authenticated using APIKeyAuthentication.
    """

    def has_permission(self, request, view):
        if not getattr(request, 'user', None):
            raise exceptions.AuthenticationFailed("API key required")
        if not hasattr(request, 'successful_authenticator'):
            raise exceptions.AuthenticationFailed("API key required")
        if request.successful_authenticator.__class__.__name__ != "APIKeyAuthentication":
            raise exceptions.AuthenticationFailed("Invalid authentication method")
        return True
