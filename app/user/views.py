"""
Views for the user API.
"""
# rest_framework provides base classs that handle
# a request in default/standartalized way
# it also allows us override/modify modify the default behaviour
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from user.serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions

# UserSerializer: a serializer created in serializers.py
from user.serializers import UserSerializer
from core.models import User

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# "authenticate" checks if username and password are correct
from django.contrib.auth import (
    get_user_model, authenticate, login
)
from django.contrib.auth.views import LoginView
from user.serializers import UserSerializerWithToken
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


# CreateAPIView: is part of geerics module
# it handles a HTTP POST request designed for creating objects in db
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    # define serializer, set it to this view so that
    # django rest framework knows which serializer to use
    # It also knows which model to use bcs it's defined in
    # serializers: get_user_model()
    serializer_class = UserSerializer


# RetrieveUpdateAPIView: provides functionality for retrieving (http get)
# and updating (http patch/put) objects in the db
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    # set UserSerializer (from app/user/serializers.py)
    serializer_class = UserSerializer

    authentication_classes = (JWTAuthentication, )
    # authentication_classes = [authentication.TokenAuthentication]
    # whe know who the user is and we want to know
    # what they can do in the system
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()  # ADDED MYSELF

    # override get_object (gets object for any http request made for api)
    def get_object(self):
        """Retrieve and return the authenticated user."""

        # Note: when user is authenticated, user object is assigned
        # to the request object available in the view.
        # Use that to return the user object for the request made for this API.
        return self.request.user


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
#             user = authenticate(request, username=username, password=password)

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


class MyTokenObtainPairView(TokenObtainPairView):
    serializer = MyTokenObtainPairSerializer


# @api_view(['POST'])
# def registerUser(request):
#     data = request.data
#     try:
#         user = get_user_model().objects.create(
#             name=data['name'],
#             email=data['email'],
#             password=make_password(data['password'])
#         )
#         serializer = UserSerializerWithToken(user, many=False)
#         return Response(serializer.data)
#     except Exception:
#         message = {'detail': "User with this email already exists."}
#         return Response(message, status=status.HTTP_400_BAD_REQUEST)


# # get token before getting a user
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getUserProfile(request):
#     user = request.user  # get logged in user
#     serializer = UserSerializer(user, many=False)
#     return Response(serializer.data)


# @api_view(['GET'])
# # admin has to be authenticated so no IsAuthenticated
# @permission_classes([IsAdminUser])
# def getUsersList(request):
#     # get all the users
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)
