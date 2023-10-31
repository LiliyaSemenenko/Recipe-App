"""
Views for the user API.
"""
# rest_framework provides base classs that handle
# a request in default/standartalized way
# it also allows us override/modify modify the default behaviour
# from rest_framework import status
# from django.contrib.auth.hashers import make_password
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated, IsAdminUser

from user.serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions

# UserSerializer: a serializer created in serializers.py
from user.serializers import UserSerializer, UserProfileSerializer
from core.models import User, UserProfile

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# "authenticate" checks if username and password are correct
from django.contrib.auth import (
    get_user_model, authenticate, login
)
# from django.contrib.auth.views import LoginView
from user.serializers import UserSerializerWithToken
# from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# from django.contrib.auth.hashers import make_password
# from rest_framework import status
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.parsers import JSONParser,ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from . import serializers, permissions
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# HTTP POST
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer

# RetrieveUpdateAPIView: http get and http patch/put
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = [IsAuthenticated]

    # override get_object (gets object for any http request made for api)
    def get_object(self):
        """Retrieve and return the authenticated user."""

        return self.request.user


class CreateUserProfileView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer


class ManageUserProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = UserProfileSerializer

    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""

        queryset = UserProfile.objects.get(user=self.request.user)
        return queryset

    def get_object(self):
        """Retrieve and return the authenticated user."""

        # return self.request.user.profile
        return UserProfile.objects.get(user=self.request.user)



# NEW
# displays info about currently signed in users (if they successfully log in)
def index(request):
    # If no user is signed in, return to login page:
    # every request has a user associated with it.
    # so if that user object is not signed in
    if not request.user.is_authenticated:
        # user is redirected back to login page
        return HttpResponseRedirect(reverse("user:login"))
    # render this template
    return render(request, "user/profile.html")


# class LoginUserView(LoginView):

#     def login_view(request):
#         if request.method == "POST":
#             # Accessing username and password from form data
#             username = request.POST["name"]
#             password = request.POST["password"]

#             # https://docs.djangoproject.com/en/3.2/topics/auth/customizing
#             # /#writing-an-authentication-backend
#             # Check if name and pass are correct, returning User object if so
#             user = authenticate(request, username=username,
# password=password)

#             # If user object is returned, log in and route to index page:
#             if user is not None:
#                 login(request, user)
#                 # back to original route
#                 return HttpResponseRedirect(reverse("user:index"))
#             # Otherwise, return login page again with new context
#             else:
#                 # render user login page again
#                 return render(request, "user/login.html", {
#                     # display this statement
#                     "message": "Invalid Credentials"
#                 })

#         if request.GET.get('message'):
#             # Get the message from the query parameters
#             message = request.GET.get('message')
#             return render(request, 'user/login.html', {'message': message})

#         return render(request, "user/login.html")
