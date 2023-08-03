"""
Views for the recipe APIs.
"""
from rest_framework import (
    viewsets,
    mixins,  # to add additional functionality in view
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)
from recipe import serializers  # imports recipe serializer

# Note: everything needs to be spelled correctly here!!!


# ModelViewSet: works directly with a model
# (good for using existing logic from existing
# serializer to peform CRUD operations)
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""

    # configure viewset
    serializer_class = serializers.RecipeDetailSerializer
    # represents objects available for this viewset through the Recipe model
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    # you need to be authenticated to make a request to API
    permission_classes = [IsAuthenticated]

    # override get query set method provided by model viewset
    # this ensures the recepies are filtered down to authenticated user
    def get_queryset(self):
        """Retrieve recipes for authenticated user."""

        # Get queryset object that are filtered by user
        # that is assigned to request.
        # User must be authenticated bcs of TokenAuthentication
        # and IsAuthenticated as a permission class.
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""

        # if calling 'list' endpoint, which is HTTP GET,
        # to the root of API, it will come up as action list
        # and return the serialization for the list view.
        if self.action == 'list':  # listing recipes
            # return a reference to a class, not an object 'RecipeSerializer()'
            return serializers.RecipeSerializer
        # if anything besides listing ia called
        return self.serializer_class  # configured serializer class

    # When a new recipe is created through CREATE feature of this
    # model viewset, perform_create() is called as part of that object creation
    def perform_create(self, serializer):
        # serializer data is validated already through this viewset

        """Create a new recipe."""

        # override how DRF saves a model in a viewset.
        # set user value to the current authecticated user when object is saved
        serializer.save(user=self.request.user)


# ListModelMixin: adds listing fucntionality for listing models
# GenericViewSet: allows to add mixins to customize viewset functionality
# Note: GenericViewSet needs to be the last param
# bcs it can override some behavior
class TagViewSet(mixins.DestroyModelMixin,  # for test_delete_tag to work
                 mixins.UpdateModelMixin,  # for test_update_tag to work
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """Manage tags in the database."""

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # return only query objects for the auth user
    def get_queryset(self):
        """Filter quesryset to authentiacted user."""
        # order_by('-name'): ensures that order is consistent
        # as db may store it differently
        return self.queryset.filter(
            user=self.request.user
            ).order_by('-name').distinct()


class IngredientViewSet(
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                # router adds ingredient-detail url automatically
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    """Manage ingredients in database."""

    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    # use token to auth
    authentication_classes = [TokenAuthentication]
    # all users must be auth to use this endpoint
    permission_classes = [IsAuthenticated]

    # return only query objects for the auth user
    def get_queryset(self):
        """Filter quesryset to authentiacted user."""
        # order_by('-name'): ensures that order is consistent
        # as db may store it differently
        return self.queryset.filter(
            user=self.request.user
            ).order_by('-name').distinct()
