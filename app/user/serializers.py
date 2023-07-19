"""
Serializers for the user API View.
"""

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


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    # tell django rest framework which model it's representing
    # does validation (if not passed, raises validation error)
    class Meta:
        model = get_user_model()
        # fields that users can set themselves through the API
        # fields in the model that's created
        fields = ['email', 'password', 'name']
        # dict providing extra metadata to the fields
        # password: write_only: True: users can only write passwords
        # but NOT read the password.
        # 'min_length': 5: minimum 5 characters in password
        # (otherwise, fails validation)
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

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
    # so when the data is posted to the view,
    # it's will pass it to the sterilizer
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
