"""
Tests for ingredients APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status  # HTTP status codes
from rest_framework.test import APIClient  # testing client

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

# ingredients api that can be used in tests
INGREDIENTS_URL = reverse('recipe:ingredient-list')


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email=email, password=password)


def detail_url(ingredient_id):
    """Create and return a ingredient detail URL."""

    # generate a unique URL for a specific recipes detail endpoint.
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


class PublicIngredientsAPITesst(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call ingredients API."""

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """Test retrieving a list of ingredients."""

        Ingredient.objects.create(user=self.user, name='Milk')
        Ingredient.objects.create(user=self.user, name='Sugar')

        res = self.client.get(INGREDIENTS_URL)

        # retrieve all the ingredients (2 here)
        # sort ingredients by names in reverse order (last updated shows 1st)
        ingredients = Ingredient.objects.all().order_by('-name')

        # pass all retrieved tags to a serializer
        # result should match whatever serializer returns
        # many=True: when passing a list of items (2 here)
        serializer = IngredientSerializer(ingredients, many=True)

        # self.assertEqual(actual_value, expected_value)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # check if db data is same as serializer data
        self.assertEqual(res.data, serializer.data)
