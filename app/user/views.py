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
from rest_framework import generics, permissions, status

# UserSerializer: a serializer created in serializers.py
from user.serializers import UserSerializer, UserProfileSerializer
from core.models import User, UserProfile

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# "authenticate" checks if username and password are correct
# from django.contrib.auth import (
#     get_user_model, authenticate, login
# )
# from django.contrib.auth.views import LoginView
from user.serializers import UserSerializerWithToken
# from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# from django.contrib.auth.hashers import make_password
# from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import (
    mixins,
)
from django.shortcuts import get_object_or_404


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


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
    # permission_classes = (permissions.UpdateOwnProfile,)
    queryset = UserProfile.objects.all()  # ADDED MYSELF

    # override get_object (gets object for any http request made for api)
    def get_object(self):
        """Retrieve and return the authenticated user."""

        # Note: when user is authenticated, user object is assigned
        # to the request object available in the view.
        # Use that to return the user object for the request made for this API.
        return self.request.user


##################################################################################
# # RetrieveUpdateAPIView: provides functionality for retrieving (http get)
# # and updating (http patch/put) objects in the db
# class ManageUserProfileView(generics.RetrieveUpdateAPIView,
#                             mixins.UpdateModelMixin):
#     """Manage the authenticated user."""

#     serializer_class = UserProfileSerializer

#     authentication_classes = (JWTAuthentication, )
#     # whe know who the user is and we want to know
#     # what they can do in the system
#     permission_classes = [permissions.IsAuthenticated]
#     # permission_classes = (permissions.UpdateOwnProfile,)
#     # queryset = UserProfile.objects.all()  # ADDED MYSELF

#     # def get_queryset(self):
#     #     """Retrieve recipes for authenticated user."""
#     #     name = self.request.query_params.get('name')
#     #     email = self.request.query_params.get('email')
#     #     queryset = self.queryset
#     #     if name:
#     #         tag_ids = self._params_to_ints(name)
#     #         queryset = queryset.filter(tags__id__in=tag_ids)
#     #     if ingredients:
#     #         ingredient_ids = self._params_to_ints(ingredients)
#     #         queryset = queryset.filter(ingredients__id__in=ingredient_ids)

#     #     # return queryset.filter(
#     #     #     user=self.request.user
#     #     # ).order_by('-id').distinct()

#     #     if self.request.user.is_authenticated:
#     #         # Filter by user only when authenticated
#     #         queryset = queryset.filter(user=self.request.user)

#     #     # distinct: to avoid duplicates
#     #     return queryset.order_by('-id').distinct()

#     # override get_object (gets object for any http request made for api)
#     # def get_object(self):
#     #     """Retrieve and return the authenticated user."""

#     #     # Note: when user is authenticated, user object is assigned
#     #     # to the request object available in the view.
#     #     # Use that to return the user object for the request made for this API.
#     #     user = self.request.user
#     #     try:
#     #         # Try to get the associated user profile
#     #         user_profile = UserProfile.objects.get(user=user)
#     #     except UserProfile.DoesNotExist:
#     #         # If no user profile exists, create one
#     #         user_profile = UserProfile.objects.create(user=user)

#     #     # Create a dictionary containing data from both models
#     #     user_data = {
#     #         'email': user.email,
#     #         'name': user.name,
#     #         'picture': user_profile.picture,
#     #         'bio': user_profile.bio,
#     #         'dob': user_profile.dob,
#     #         'pronouns': user_profile.pronouns,
#     #         'gender': user_profile.gender,
#     #     }
#     #     return user_data

#     def get_object(self):
#         """Retrieve and return the authenticated user's profile."""
#         user = self.request.user
#         # userprofile = user.userprofile_set.all()
#         queryset = UserProfile.objects.all()
#         if self.request.user.is_authenticated:
#             # Filter by user only when authenticated
#             queryset = queryset.filter(user=self.request.user)
#         serializer = UserProfileSerializer(queryset, many=False)
#         return Response(serializer.data)
#         # return self.request.user.profile

#     # def get_queryset(self):
#     #     qs = UserProfile.objects.all()
#     #     logged_in_user_profile = qs.filter(user=self.request.user)
#     #     return logged_in_user_profile

#     # def get_object(self):
#     #     queryset = UserProfile.objects.all()
#     #     obj = get_object_or_404(queryset, user=self.request.user)
#     #     return obj

#     # def update(self, request, *args, **kwargs):
#     #     instance = self.get_object() #------>I have the object that I would like to update
#     #     serializer = self.get_serializer(instance, data=request.data, partial=True)
#     #     serializer.is_valid(raise_exception=True) #--->Success

#     # def get(self, *args):
#     #     """
#     #     :param args: Handled by rest_framework views.dispatch

#     #     :return: JSON object containing User Personal Data
#     #     """
#     #     queryset = self.get_queryset()
#     #     serializer = UserProfileSerializer(queryset)
#     #     return Response(data=serializer.data)

#     # def put(self, request, *args, **kwargs):
#     #     return self.update(request, *args, **kwargs)

#     # def patch(self, request):
#     #     """
#     #     :param request: request object is sent by the client
#     #     :return:  Json response with the data sent of the body
#     #     """
#     #     queryset = self.get_queryset()
#     #     serializer = UserProfileSerializer(queryset, data=request.data, partial=True)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(data=serializer.data, status=status.HTTP_200_OK)
#     #     return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
########################################################################
    # def get_queryset(self):
    #     """Filter queryset to authenticated user."""
    #     assigned_only = bool(
    #         int(self.request.query_params.get('assigned_only', 0))
    #     )
    #     queryset = self.queryset
    #     if assigned_only:
    #         queryset = queryset.filter(profile__isnull=False)

    #     # return queryset.filter(
    #     #     user=self.request.user
    #     # ).order_by('-name').distinct()

    #     if self.request.user.is_authenticated:
    #         # Filter by user only when authenticated
    #         queryset = queryset.filter(user=self.request.user)

    #     return queryset.order_by('-id').distinct()

    # @api_view(['PUT', 'PATCH'])
    # def UpdateAPIView(self, request):
    #     user = request.user
    #     # user_serializer = UserSerializerWithToken(user, many=False)

    #     data = request.data

    #     profile = self.request.user.profile
    #     serializer = UserProfileSerializer(user, many=False)


    #     profile.name = data['name']
    #     profile.email = data['email']
    #     profile.picture = data['picture']
    #     profile.bio = data['bio']
    #     profile.dob = data['dob']
    #     profile.pronouns = data['pronouns']
    #     profile.gender = data['gender']


    #     user.save()
    #     profile.save()

    #     return Response(serializer.data)

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
