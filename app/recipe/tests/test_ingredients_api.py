"""
Tests for ingredients APIs.
"""
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status  # HTTP status codes
from rest_framework.test import APIClient  # testing client

from core.models import (
    Ingredient,
    Recipe)

from recipe.serializers import IngredientSerializer

# ingredients api that can be used in tests
INGREDIENTS_URL = reverse('recipe:ingredient-list')


def create_user(email='userIng@example.com', password='testpass123'):
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

    # def test_auth_required(self):
    #     """Test auth is required to call ingredients API."""

    #     res = self.client.get(INGREDIENTS_URL)

    #     self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


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

    def test_ingredients_limited_to_user(self):
        """Test list of ingredients is limited to authenticated user."""

        user2 = create_user(email='userIng2@example.com')
        Ingredient.objects.create(user=user2, name='Tomato')

        ingredient = Ingredient.objects.create(user=self.user, name='Rice')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # check that only 1 ingr is returned for auth user (self.user)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
        self.assertEqual(res.data[0]['id'], ingredient.id)

    def test_update_ingredient(self):
        """Test updating ingredient name."""

        ingredient = Ingredient.objects.create(
            user=self.user, name='Strawberry')

        payload = {'name': 'Cherry'}

        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        """Test deleting ingredients."""

        ingredient = Ingredient.objects.create(user=self.user, name='Potato')

        url = detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        # retrive list of ingredients for self.user
        ingredients = Ingredient.objects.filter(user=self.user)
        # check that no ingredients in db for self.user
        self.assertFalse(ingredients.exists())

    def test_filter_ingredients_assigned_to_recipes(self):
        """Test listing ingredients by those assigned to recipes."""

        in1 = Ingredient.objects.create(user=self.user, name='Coffee')
        in2 = Ingredient.objects.create(user=self.user, name='Cucumber')

        recipe = Recipe.objects.create(
            user=self.user,
            title='Latte',
            time_minutes=5,
            price=Decimal('2.50'),
            )
        recipe.ingredients.add(in1)

        # get a filtered request of assigned only ingredients
        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

        s1 = IngredientSerializer(in1)
        s2 = IngredientSerializer(in2)

        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filter_ingredients_unique(self):
        """Test filtered ingredinets returns a unique list."""
        ing = Ingredient.objects.create(user=self.user, name='Albacore')
        Ingredient.objects.create(user=self.user, name='Beef')

        recipe1 = Recipe.objects.create(
            user=self.user,
            title='Albacore Sushi Roll',
            time_minutes=15,
            price=Decimal('25.00'),
        )
        recipe2 = Recipe.objects.create(
            user=self.user,
            title='Spicy Poke Bowl',
            time_minutes=20,
            price=Decimal('35.00'),
        )

        recipe1.ingredients.add(ing)
        recipe2.ingredients.add(ing)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

        # check that Albacore returns only once
        self.assertEqual(len(res.data), 1)
