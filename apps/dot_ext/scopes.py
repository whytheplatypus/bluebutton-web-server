from __future__ import absolute_import
from __future__ import unicode_literals

from oauth2_provider.scopes import BaseScopes
from oauth2_provider.contrib.rest_framework import permissions

from apps.capabilities.models import ProtectedCapability


class CapabilitiesScopes(BaseScopes):
    """
    A scope backend that uses ProtectedCapability model.
    """
    def get_all_scopes(self):
        """
        Returns a dict-like object that contains all the scopes
        in the ProtectedCapability model.
        """
        return dict(ProtectedCapability.objects.values_list('slug', 'title'))

    def get_available_scopes(self, application=None, request=None, *args, **kwargs):
        """
        Returns a list that contains all the capabilities related
        to the current application.
        """
        return list(ProtectedCapability.objects.values_list('slug', flat=True))

    def get_default_scopes(self, application=None, request=None, *args, **kwargs):
        """
        Returns a list that contains all the capabilities related
        to the current application.
        """
        # at the moment we assume that the default scopes are all those availables
        return self.get_available_scopes(application, request, *args, **kwargs)


class TokenHasRouteScope(permissions.TokenHasScope):

    def get_scopes(self, request, view):
        # get route from request
        route = request.path
        # call the route the scope 
        return [route]
