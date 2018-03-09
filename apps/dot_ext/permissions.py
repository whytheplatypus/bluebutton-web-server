import json
from oauth2_provider.contrib.rest_framework import permissions
from apps.capabilities.models import ProtectedCapability


def path_match(route, path):
    # TODO allow pattern matching
    # or something?
    return route == path


class TokenHasRouteScope(permissions.TokenHasScope):

    def get_scopes(self, request, view):
        # get route from request
        path = request.path
        method = request.method
        required_scopes = []
        # TODO build scope list by finding the scopes with this in the list
        possible_scopes = ProtectedCapability.objects.all()
        for possible_scope in possible_scopes:
            routes = json.loads(possible_scope.protected_resources)
            for route in routes:
                if route[0] == method:
                    if path_match(route[1], path):
                        required_scopes.append(possible_scope.slug)
        # call the route the scope
        return required_scopes
