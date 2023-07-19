"""
Views for the user API.
"""
# rest_framework provides base classs that handle
# a request in default/standartalized way
# it also allows us override/modify modify the default behaviour
from rest_framework import generics

# UserSerializer: a serializer created in serializers.py
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


# CreateAPIView: is part of geerics module
# it handles a HTTP POST request designed for creating objects in db
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    # define serializer, set it to this view so that
    # django rest framework knows which serializer to use
    # It also knows which model to use bcs it's defined in
    # serializers: get_user_model()
    serializer_class = UserSerializer


# ObtainAuthToken: view provided by DRF
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""

    # customise serializer
    serializer_class = AuthTokenSerializer
    # enable browsable api used for DRF
    render_classes = api_settings.DEFAULT_RENDERER_CLASSES
