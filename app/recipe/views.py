"""
Views for the recipe APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers  # imports recipe serializer


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
