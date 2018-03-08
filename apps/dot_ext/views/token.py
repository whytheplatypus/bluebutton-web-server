# TODO: Lock down endpoint via a scope
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.models import AccessToken
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from ..models import Application
from ..scopes import TokenHasRouteScope


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'name', 'logo_uri', 'tos_uri', 'policy_uri', 'contacts')


class AccessTokenSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer(read_only=True)

    class Meta:
        model = AccessToken
        fields = ('id', 'user', 'application', 'expires', 'scope')


# TODO limit with mixins
class AuthorizedTokens(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin):

    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated, TokenHasRouteScope]
    serializer_class = AccessTokenSerializer

    def get_queryset(self):
        return AccessToken.objects.select_related("application").filter(user=self.request.user)

