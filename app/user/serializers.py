"""
Serializers for the user API View.
"""
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# get_user_model(): used to retrieve the User model that
# is currently active in your Django project, regardless of
# whether it's the default User model or a custom one you have defined.
from django.contrib.auth import (
    get_user_model,
    authenticate,  # alows to auth with auth system
    )

from django.utils.translation import gettext as _

# serializers modules includes tools for defining serializers (base classes)
# serializers are the way to convert objects to and from Python objects
# ex. takes JSON input posted by api, validates it
# (secure, correct per validation rules), and then
# converts that input into Python obeject or the model in our db

# base classes: serializers.Serializer,
# serializers.ModelSerializer (validates and save to a model in db)
from rest_framework import serializers
from core.models import UserProfile
from rest_framework.serializers import raise_errors_on_nested_writes


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the user profile object."""

    # Include fields from the User model
    # name = serializers.CharField(source='user.name')
    # email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        fields =  ['picture', 'bio', 'dob', 'pronouns', 'gender']
        # extra_kwargs = {'name': {'write_only': False}, 'email': {'write_only': False}}


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    profile = UserProfileSerializer(source="userprofile", many=False)

    # tell django rest framework which model it's representing
    # does validation (if not passed, raises validation error)
    class Meta:  # turns data into dict form
        model = get_user_model()
        # fields that users can set themselves through the API
        # fields in the model that's created
        fields = ['name', 'email', 'password', 'profile']  # 'is_staff', 'is_active'
        # dict providing extra metadata to the fields
        # password: write_only: True: users can only write passwords
        # but NOT read the password.
        # 'min_length': 5: minimum 5 characters in password
        # (otherwise, fails validation)
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

    # create method: overrides the behavior of serializer when you
    # create new objects out of that serializer.
    # default behaviour: save the objects as they passed in
    # (password in clear text)
    def create(self, validated_data):
        """Create and return a user with encrypted password."""

        # use create_user method from models.py to encrypt password
        # Note: this func only gets called if the validation
        # for pw was passed in the Meta class
        return get_user_model().objects.create_user(**validated_data)

    # overriding update method on our UserSerializer
    # instance: object that's being updated (here: model)
    # validated_data: data that's already passed through
    # serializer validation (email, pw, name)
    def update(self, instance, validated_data):
        """Update and return user."""

        # pop password: retrieve and remove pw from validated data dict
        # 'password', None: let user to not update the pw,
        # so None is an default value
        password = validated_data.pop('password', None)
        # if password was specified by the user for the update
        if password:
            user.set_password(password)
            user.save()

        profile_serializer = self.fields['profile']
        profile_instance = instance.userprofile
        profile_data = validated_data.pop('userprofile', {})

        # to access the UserProfile fields in here
        # mobile = userprofile_data.get('mobile')

        # update the userprofile fields
        profile_serializer.update(profile_instance, profile_data)

        # super().update(): calls the update method on the
        # model serializer a base class.
        # Performs all of the steps for updating the object
        # (using existing update method).
        user = super().update(instance, validated_data)

        return user  # used by the view later


    # def update(self, instance, validated_data):
    #         userprofile_serializer = self.fields['profile']
    #         userprofile_instance = instance.userprofile
    #         userprofile_data = validated_data.pop('userprofile', {})

    #         # to access the UserProfile fields in here
    #         # mobile = userprofile_data.get('mobile')

    #         # update the userprofile fields
    #         userprofile_serializer.update(userprofile_instance, userprofile_data)

    #         instance = super().update(instance, validated_data)
    #         return instance

    def get_name(self, obj):
        """Retrive user's name."""
        name = obj.first_name
        return name

    def get_id(self, obj):
        """Retrive user's id."""
        return obj.id

    # def get_isAdmin(self, obj):
    #     return obj.is_staff


# basic serializer that is not likend to any specific model
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""

    # define a serializer with 2 fields
    email = serializers.EmailField()
    password = serializers.CharField(
        # with browsable API the password text will be hidden
        style={'input_type': 'password'},
        # don't trim spaces inside the password
        trim_whitespace=False,
    )

    # add a validate method that is called on the serializer
    # at a validation of an input stage (when posted to the view) by a view
    # so when the data is posted to the view, it passes data to the sterilizer
    # and then it's will call validate to check that the data is correct.
    def validate(self, attrs):  # attrs: attributes
        """Validate and authenticate the user."""

        # get email that was passed to the endpoint
        email = attrs.get('email')
        password = attrs.get('password')

        # call authentication request
        user = authenticate(
            request=self.context.get('request'),
            # email and password will be checked automatically
            # if correct: return the user
            # if incorrect: return nothing
            username=email,  # use email as username
            password=password,
        )
        # if returned nothing from authentication request
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            # Note: the view will translate this to HTTP 400 BAD REQUEST
            raise serializers.ValidationError(msg, code='authorization')

        # set user attribute to use in the view
        attrs['user'] = user

        return attrs


# UserSerializerWithToken is an extention of UserSerializer
# generates a new refresh token when user registers, updates account info
class UserSerializerWithToken(UserSerializer):
    """Serializer for user token view."""

    token = serializers.SerializerMethodField(read_only=True)

    # pass all the meta values from Meta() in UserSerializer
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['token']

    def get_token(self, obj):  # user object
        token = RefreshToken.for_user(obj)
        return str(token.access_token)  # token needs to be a str


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    # Override the default validate method
    # https://github.com/jazzband/djangorestframework-simplejwt/
    # blob/master/rest_framework_simplejwt/serializers.py
    def validate(self, attrs):
        """Serialize more info about the user."""

        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            # ex. data['username'] = self.username
            # ex. data['email'] = self.user.email
            data[k] = v

        return data

##################################################################################
# class UserProfileSerializer(serializers.ModelSerializer):
#     """Serializer for the user profile object."""

#     # Include fields from the User model
#     name = serializers.CharField(source='user.name')
#     email = serializers.EmailField(source='user.email')

#     class Meta:
#         model = UserProfile
#         fields =  ['name', 'email', 'picture', 'bio', 'dob', 'pronouns', 'gender']
#         # extra_kwargs = {'name': {'write_only': False}, 'email': {'write_only': False}}

#     def get_token(self, obj):
#         token = RefreshToken.for_user(obj)
#         return str(token.access_token)

#     def create(self, validated_data):
#         """Create a profile."""

#         user = self.context['request'].user
#         # user = request.user
#         # user = self.context['request'].user
#         profile, created = UserProfile.objects.update_or_create(user=user, **validated_data)

#         return profile

#     def update(self, instance, validated_data):
#         """Update recipe."""
#         # picture = validated_data.pop('picture', None)
#         bio = validated_data.pop('bio', None)
#         # dob = validated_data.pop('dob', None)
#         # pronouns = validated_data.pop('pronouns', None)
#         # gender = validated_data.pop('gender', None)
#         user = super().update(instance, validated_data)

#         profile = super().update(instance, validated_data)
#         profile.save()
#         password = validated_data.pop('password', None)

#         # # if password was specified by the user for the update
#         if password:
#             user.set_password(password)
#             user.save()

#         return profile  # used by the view later


#     # Custom .update() method for serializer to handle UserProfile data update
#     # def update(self, instance, validated_data):
#     #     auth_user = self.context['request'].user

#     #     userprofile_serializer = self.fields['bio']
#     #     userprofile_instance = instance.profile
#     #     userprofile_data = validated_data.pop('bio', {})

#     #     # to access the UserProfile fields in here
#     #     # mobile = userprofile_data.get('mobile')

#     #     # update the userprofile fields
#     #     userprofile_serializer.update(userprofile_instance, userprofile_data)

#     #     instance = super().update(instance, validated_data)
#     #     return instance


#     # def update(self, instance, validated_data):
#     #     raise_errors_on_nested_writes('update', self, validated_data)
#     #     info = UserProfile._meta.get_field_info(instance)
#     #     profile = instance.userprofile
#     #     p_info = UserProfile._meta.get_field_info(profile)

#     #     for attr, value in validated_data.items():
#     #         if attr == 'userprofile':
#     #             for attr2, value2 in value.items():
#     #                 setattr(profile, attr2, value2)

#     #         elif attr in info.relations and info.relations[attr].to_many:
#     #             # field = getattr(instance, attr)
#     #             # field.set(value)
#     #             continue
#     #         if attr == 'user':  # Skip updating the 'user' field
#     #             continue
#     #         else:
#     #             setattr(instance, attr, value)
#     #     instance.save()
#     #     profile.save()

#     #     return instance



#     def get_id(self, obj):
#         """Retrive user's id."""
#         return obj.user.id

#     def get_name(self, obj):
#         """Get the name from the related User model."""
#         return obj.user.name

#     def get_email(self, obj):
#         """Get the email from the related User model."""
#         return obj.user.email

#     def get_bio(self, obj):
#         """Get the email from the related User model."""
#         return obj.bio
########################################################################



    # def put(self, request):
    #     try:
    #         user_profile = UserProfile.objects.get(user=request.user)
    #         serializer = UserProfileSerializer(user_profile, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except UserProfile.DoesNotExist:
    #         return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    # @api_view(['PUT'])
    # @permission_classes([IsAuthenticated])
    # def updateUserProfile(request):
    #     user = request.user
    #     serializer = UserSerializerWithToken(user, many=False)

    #     data = request.data
    #     user.first_name = data['name']
    #     user.username = data['email']
    #     user.email = data['email']

    #     if data['password'] != '':
    #         user.password = make_password(data['password'])

    #     user.save()

    #     return Response(serializer.data)





    # def get_token(self, obj):
    #     token = RefreshToken.for_user(obj)
    #     return str(token.access_token)

    # # create method: overrides the behavior of serializer when you
    # # create new objects out of that serializer.
    # # default behaviour: save the objects as they passed in
    # # (password in clear text)
    # def create(self, validated_data):
    #     """Create and return a user with encrypted password."""

    #     # use create_user method from models.py to encrypt password
    #     # Note: this func only gets called if the validation
    #     # for pw was passed in the Meta class
    #     return get_user_model().objects.create_user(**validated_data)

    # # overriding update method on our UserSerializer
    # # instance: object that's being updated (here: model)
    # # validated_data: data that's already passed through
    # # serializer validation (email, pw, name)
    # def update(self, instance, validated_data):
    #     """Update and return user."""

    #     # pop password: retrieve and remove pw from validated data dict
    #     # 'password', None: let user to not update the pw,
    #     # so None is an default value
    #     password = validated_data.pop('password', None)
    #     # super().update(): calls the update method on the
    #     # model serializer a base class.
    #     # Performs all of the steps for updating the object
    #     # (using existing update method).
    #     user = super().update(instance, validated_data)

    #     # if password was specified by the user for the update
    #     if password:
    #         user.set_password(password)
    #         user.save()

    #     return user  # used by the view later

    # def get_name(self, obj):
    #     """Retrive user's name."""
    #     name = obj.first_name
    #     return name

    # def get_id(self, obj):
    #     """Retrive user's id."""
    #     return obj.id

    # # def get_isAdmin(self, obj):
    # #     return obj.is_staff