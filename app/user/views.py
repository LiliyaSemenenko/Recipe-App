"""
Views for the user API.
"""
# rest_framework provides base classs that handle
# a request in default/standartalized way
# it also allows us override/modify modify the default behaviour
from rest_framework import generics, authentication, permissions

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


# RetrieveUpdateAPIView: provides functionality for retrieving (http get)
# and updating (http patch/put) objects in the db
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    # set UserSerializer (from app/user/serializers.py)
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    # whe know who the user is and we want to know
    # what they can do in the system
    permission_classes = [permissions.IsAuthenticated]

    # override get_object (gets object for any http request made for api)
    def get_object(self):
        """Retrieve and return the authenticated user."""

        # Note: when user is authenticated, user object is assigned
        # to the request object available in the view.
        # Use that to return the user object for the request made for this API.
        return self.request.user
