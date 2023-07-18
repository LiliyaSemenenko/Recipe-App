"""
Serializers for the user API View.
"""

# get_user_model(): used to retrieve the User model that
# is currently active in your Django project, regardless of
# whether it's the default User model or a custom one you have defined.
from django.contrib.auth import get_user_model

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
