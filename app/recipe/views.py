"""
Views for the recipe APIs.
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import (
    viewsets,
    mixins,  # to add additional functionality in view
    status,  # to check HTTP response code
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)
from recipe import serializers  # imports recipe serializer


# add documentation changes
# extend the schema for the list endpoint (the one we add filters to)
@extend_schema_view(  # extend the auto-generated schema by drf-spectacular
    list=extend_schema(
        # parameters that passed in to the requests that are made
        # to the list api for this view
        parameters=[
            # allows to specify details of params accepted in API request
            OpenApiParameter(
                'tags',  # name of the parameter to filter
                # type is a str bcs it accepts
                # a comma separated list of IDs as a string
                OpenApiTypes.STR,
                # description for a dev who's reading a documentation
                description='Comma separated list of tag IDs to filter.',
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Comma separated list of ingr IDs to filter.',
            )
        ]
    )
)
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

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        # string: "1,2,3"
        # split them by comma, convert each to int
        return [int(str_id) for str_id in qs.split(',')]

    # override get query set method provided by model viewset
    # this ensures the recepies are filtered down to authenticated user
    def get_queryset(self):
        """Retrieve recipes for authenticated user."""

        # Get queryset object that are filtered by user
        # that is assigned to request.
        # User must be authenticated bcs of TokenAuthentication
        # and IsAuthenticated as a permission class.
        # return self.queryset.filter(user=self.request.user).order_by('-id')

        # retrieve tags/ingr as comma separated list
        # provided as a string (or None)
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        # define a quesryset to apply filters later
        # and return the resulting filtered quesryset
        queryset = self.queryset
        # if there're tags/ingrs in quesryset
        if tags:
            # convert ids to integers
            tag_ids = self._params_to_ints(tags)
            # filter related fields (tags by id)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(
            user=self.request.user
            ).order_by('-id').distinct()  # distinct: to avoid duplicates

    def get_serializer_class(self):
        """Return the serializer class for request."""

        # if calling 'list' endpoint, which is HTTP GET,
        # to the root of API, it will come up as action list
        # and return the serialization for the list view.
        if self.action == 'list':  # listing recipes
            # return a reference to a class, not an object 'RecipeSerializer()'
            return serializers.RecipeSerializer

        # upload_image: custom action added below by upload_image()
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

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

    # added a custom function specifying HTTP method POST,
    # action will to detail endpoint/portion of viewset (recipe id),
    # specify a custom url_path
    @action(methods=['POST'], detail=True, url_path='upload_image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""

        # get recipe object using primary key (pk) specified for the action
        recipe = self.get_object()
        # runs through get_serializer_class that would get an instance
        # of serializer and return the image serializer from
        # get_serializer_class code
        # data=request.data: passing in the data posted to the endpoint
        serializer = self.get_serializer(recipe, data=request.data)

        # check if serializer is valid
        if serializer.is_valid():
            # save the image to the db
            serializer.save()
            # response with data and status
            return Response(serializer.data, status=status.HTTP_200_OK)
        # return errors included with the serializer
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                # enum: enumerator that ensures that only 0 or 1 are passed in
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to recipes.',
            )
        ]
    )
)
# base of other viewset classes (RecipeAttr: tags, ingredients)
# ListModelMixin: adds listing fucntionality for listing models
# GenericViewSet: allows to add mixins to customize viewset functionality
# Note: GenericViewSet needs to be the last param bcs
# it can override some behavior
class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,  # for delete_tag to work
                            mixins.ListModelMixin,  # for update_tag to work
                            # router adds ingredient-detail url automatically
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # return only query objects for the auth user
    def get_queryset(self):
        """Filter quesryset to authentiacted user."""

        # get assigned_only value
        assigned_only = bool(  # bool to convert 1/0 to T/F
            # return assigned_only or 0 if no value is provided
            int(self.request.query_params.get('assigned_only', 0))
        )

        queryset = self.queryset

        if assigned_only:
            # filter by recipes associated with a value
            queryset = queryset.filter(recipe__isnull=False)

        # order_by('-name'): ensures that order is consistent
        # as db may store it differently
        # Note: no self.queryset bcs self will not apply filters
        return queryset.filter(
            user=self.request.user
            ).order_by('-name').distinct()


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in database."""

    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
