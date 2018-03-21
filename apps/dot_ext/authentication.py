from django.contrib.auth.models import User
from oauth2_provider.oauth2_validators import OAuth2Validator
from rest_framework import authentication
from rest_framework import exceptions
from apps.fhir.authentication import extract_username


class SLSAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        id = request.META.get('HTTP_X_AUTHENTICATION')
        if not id:
            return None

        username = extract_username(id)

        # raises User.DoesNotExist should result in 404
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.NotFound()

        # these are for compatability with OAuth2Validator
        # TODO remove if it becomes possible
        if not hasattr(request, 'headers'):
            request.headers = request.META

        if not hasattr(request, 'client'):
            request.client = None

        # populates request.client with Application if successful
        validator = OAuth2Validator()
        authenticated = validator.authenticate_client(request)
        if not authenticated:
            raise exceptions.AuthenticationFailed('No such application')

        return (user, request.client)
