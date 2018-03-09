import json
import re
from django.core.exceptions import ImproperlyConfigured
from oauth2_provider.contrib.rest_framework import permissions
from apps.capabilities.models import ProtectedCapability


def path_match(pattern, path):
    # TODO allow pattern matching

    # or something?
    return re.match(pattern, path)


def build_required_scopes(method, path):
    required_scopes = []
    possible_scopes = ProtectedCapability.objects.all()
    for possible_scope in possible_scopes:
        routes = json.loads(possible_scope.protected_resources)
        for route in routes:
            if route[0] == method:
                if path_match(route[1], path):
                    required_scopes.append(possible_scope.slug)
    return required_scopes


class TokenHasRouteScope(permissions.TokenHasScope):

    def get_scopes(self, request, view):
        required_scopes = build_required_scopes(request.method, request.path)

        try:
            view_scopes = set(super(TokenHasRouteScope, self).get_scopes(request, view))
        except ImproperlyConfigured:
            view_scopes = []

        required_scopes.extend(view_scopes)
        # call the route the scope
        if len(required_scopes) < 1: 
            raise ImproperlyConfigured(
                "TokenHasRouteScope requires the view to define the required_scopes attribute or an existing scope has a (method, route) pair that matches the views uri."
            )
        return required_scopes
