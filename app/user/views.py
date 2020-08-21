from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user import serializers
from core.models import User, Role
from rest_framework.generics import UpdateAPIView

class CreateUserView(generics.ListCreateAPIView):
    """Create new user in system"""
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = serializers.UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user


class PasswordChangeView(UpdateAPIView):
    serializer_class = serializers.PasswordChangeSerializer

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()

    def get_object(self, queryset=None):
        return self.request.user

class RoleView(generics.ListCreateAPIView):
    """Create new user in system"""
    serializer_class = serializers.RoleSerializer
    queryset = Role.objects.all()
