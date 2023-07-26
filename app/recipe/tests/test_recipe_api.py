"""
Tests for recipe APIs.
"""
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer


# recipe api that can be used in tests
RECIPES_URL = reverse('recipe:recipe-list')


# add a helper func for creating a recipe
def create_recipe(user, **params):  # **params: dictionary
    """Create and return a sample recipe."""

    # create new dictionary
    # default values for the case of no params passed
    defaults = {
        'title': 'Sample recipe title.',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'http://example.com/recipe.pdf',
    }
    # if params are passed, override their values with defaults
    defaults.update(params)

    # pass defaults to the recipe object
    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


# test as unauthenticated user
class PublicRecipeAPITests(TestCase):
    """Test unauthenticated API requests."""

    # create a test client for this class
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API (getting recipies)."""

        res = self.client.get(RECIPES_URL)

        # check that status code is HTTP 401
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """Test authenticated API requests."""

    # creates client and user
    # then authenticates client with that user
    def setUp(self):
        self.client = APIClient()
        # self.user = get_user_model().objects.create_user(
        #     'user@example.com',
        #     'testpass123',
        # )
        self.user = create_user(email='user@example.com', password='test123')

        self.client.force_authenticate(self.user)

    def test_retrieve_recipies(self):
        """Test retrieving a list of recipes."""

        # create 2 recipes in db
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        # assign value to a response that will make request to the API
        res = self.client.get(RECIPES_URL)

        # retrieve all the recipies (2 here)
        # sort recipes by id numbers in reverse order (last updated shows 1st)
        recipes = Recipe.objects.all().order_by('-id')

        # pass all retrieved recepies to a serializer
        # result should match whatever serializer returns
        # many=True: when passing a list of items (2 here)
        serializer = RecipeSerializer(recipes, many=True)

        # check that status is successful
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # check that data dict that was returned in the response
        # is equal to the data dict of the object passed through serializer
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated user."""

        # create a new user that has not been authenticated
        # other_user = get_user_model().objects.create_user(
        #     'other@example.com',
        #     'password123',
        # )
        other_user = create_user(email='other@example.com', password='test123')

        # create 2 recipes in db but assign to diff users
        create_recipe(user=other_user)  # unauthenticated user
        create_recipe(user=self.user)  # authenticated user

        # make request to the API
        res = self.client.get(RECIPES_URL)

        # filter recipies for authenticated user
        recipes = Recipe.objects.filter(user=self.user)
        # pass all retrieved recepies to a serializer
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
