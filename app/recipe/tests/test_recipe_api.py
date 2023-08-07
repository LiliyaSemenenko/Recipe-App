"""
Tests for recipe APIs.
"""
from decimal import Decimal
import tempfile
import os

from PIL import Image  # Pillow Image library
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)

from recipe.serializers import (
    # recipe preview
    RecipeSerializer,
    # when user chooses a recipe, shows more fields and details for a recipe
    RecipeDetailSerializer,
)


# recipe api that can be used in tests
RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Create and return a recipe detail URL."""

    # generate a unique URL for a specific recipes detail endpoint.
    return reverse('recipe:recipe-detail', args=[recipe_id])


# helper func to generate URL to the upload-image endpoint
def image_upload_url(recipe_id):
    """Create and return a recipe detail URL."""
    return reverse('recipe:recipe-upload-image', args=[recipe_id])


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

    def test_get_recipe_detail(self):
        """Test get recipe detail."""

        # create a sample recipe, assign it to an authenticated user
        recipe = create_recipe(user=self.user)

        # create detail url using recipe id
        url = detail_url(recipe.id)
        # call the url
        res = self.client.get(url)

        # pass in the sample recipe (only 1) to the serializer
        serializer = RecipeDetailSerializer(recipe)

        # check the detail is being returned correctly
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe throught the API."""

        # Note: not using create_recipe() helper func
        # bcs goal is to test creating a recipe throught the API.
        # So we want to pass a payload to the API w/ the contents of a recipe.
        # Goal: ensure that recipe was created successfully and correctly in db

        # define fields we want to pass to API
        payload = {
            'title': 'Sample recipe',
            'time_minutes': 30,
            'price': Decimal('5.99'),
        }
        # POST recipe with payload to URL endpoint
        res = self.client.post(RECIPES_URL, payload)  # api/recipe/recipe

        # check that response is 201 since new object was created in a system
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # GET (retirieve) recipe object by its id
        recipe = Recipe.objects.get(id=res.data['id'])

        # loop through all the values in payload
        for k, v in payload.items():  # k: key, v: value
            # getattr(): gets recipe's value
            self.assertEqual(getattr(recipe, k), v)
        # check if user that is assigned to api is same as authenticated user
        self.assertEqual(recipe.user, self.user)

    def test_partial_update(self):
        """Test partial update of a recipe."""

        # Goal: to ensure that other fields in payload aren't updated
        original_link = 'htttps://example.com/recipe.pdf'
        recipe = create_recipe(
            user=self.user,
            title='Sample recipe title',
            link=original_link,
        )

        # payload update details
        payload = {'title': 'New recipe title.'}
        url = detail_url(recipe.id)
        # update url with payload (title here)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # by default, model is not refreshed, so we call it
        recipe.refresh_from_db()
        # make sure that title contents changed
        self.assertEqual(recipe.title, payload['title'])
        # make sure that link didn't change
        self.assertEqual(recipe.link, original_link)
        # make sure that user didn't change
        self.assertEqual(recipe.user, self.user)

    def test_full_update(self):
        """Test full update recipe."""

        recipe = create_recipe(
            user=self.user,
            title='Sample recipe title.',
            link='https://example.com/recipe.pdf',
        )

        payload = {
            'title': 'New recipe title.',
            'link': 'https://example.com/new-recipe.pdf',
            'description': 'New recipe description',
            'time_minutes': 10,
            'price': Decimal('2.50'),
            }

        url = detail_url(recipe.id)
        # PUT: full update of an object
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # by default, model is not refreshed, so we call it
        recipe.refresh_from_db()

        for k, v in payload.items():
            # what's assigned to the key in db should match payload value
            self.assertEqual(getattr(recipe, k), v)
        # check authenticated user did not change
        self.assertEqual(recipe.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the recipe user returns in an error."""

        new_user = create_user(email='user2@example.com', password='pass123')

        # create recipe with authenticated user
        recipe = create_recipe(user=self.user)

        # payload with new user id
        payload = {'user': new_user.id}
        url = detail_url(recipe.id)
        # PATCH (partial update) url with payload (user id here)
        self.client.patch(url, payload)

        # by default, model is not refreshed, so we call it
        recipe.refresh_from_db()

        # make sure that user didn't change
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        """Test deleting a recipe successful."""

        recipe = create_recipe(
            user=self.user,
            title='Sample recipe title.',
            link='https://example.com/recipe.pdf',
        )

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        # check that recipe with that id returns false for exists() in db
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_delete_other_users_recipe_error(self):
        """Test trying to delete another users recipe gives error."""

        other_user = create_user(email='other@example.com', password='pass123')

        recipe = create_recipe(
            user=other_user,
            title='Sample recipe title.',
            link='https://example.com/recipe.pdf',
            )

        url = detail_url(recipe.id)  # other user's url
        res = self.client.delete(url)  # del by auth user

        # Note: use HTTP_404 here instead of 403_FORBIDDEN
        # to hide the existence of a resource from an unauthorized client
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        # check that recipe with that id returns true for exists() in db
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())

    # creating tags test is here cuz created through the recipe
    def test_create_recipe_with_new_tags(self):
        """Test creating a recipe with new tags throught the API."""

        payload = {
            'title': 'Thai Prawn Curry',
            'time_minutes': 30,
            'price': Decimal('2.50'),
            # assign 2 tags to this recipe
            'tags': [{'name': 'Thai'}, {'name': 'Dinner'}]
        }
        # set format to json bcs providing nested objects
        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipes = Recipe.objects.filter(user=self.user)
        # check if 1 recipe was created
        self.assertEqual(recipes.count(), 1)

        recipe = recipes[0]  # 1st recipe
        # check if number of tags in that recipe is 2
        self.assertEqual(recipe.tags.count(), 2)

        # loop through each tag
        for tag in payload['tags']:
            exists = recipe.tags.filter(
                name=tag['name'],  # check if name is correct
                user=self.user,  # check if user/owner is correct
            ).exists()
            # check if each tag exists in db
            self.assertTrue(exists)

    def test_create_recipe_with_existing_tags(self):
        """Test creating a recipe with existing tags throught the API."""

        # Adding a recipe to a tag that a recipe is alredy assigned to

        tag_indian = Tag.objects.create(user=self.user, name='Indian')
        payload = {
            'title': 'Pongal',
            'time_minutes': 60,
            'price': Decimal('4.50'),
            'tags': [{'name': 'Indian'}, {'name': 'Breakfast'}],
        }

        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # create a new
        recipes = Recipe.objects.filter(user=self.user)
        recipe = recipes[0]

        self.assertEqual(recipes.count(), 1)
        # check if a recipe has 2 tags
        self.assertEqual(recipe.tags.count(), 2)
        # check if tag_indian was reassigned to the recipe, not created again
        self.assertIn(tag_indian, recipe.tags.all())

        for tag in payload['tags']:
            exists = recipe.tags.filter(
                name=tag['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)

    def test_create_tag_on_update(self):
        """Test creating tag when updating a recipe."""

        # check that if recipe is updated providing a nonexisting tag in db,
        # we'll automatically create it in db

        recipe = create_recipe(user=self.user)

        payload = {'tags': [{'name': 'Soup'}]}

        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Note: no refresh from db bcs many to many fields
        # is creating a new query under the hood.
        # So when you call recipe.tags.all(), it'll do a separate query
        # and retrieve all the fresh objects for the recipe.

        new_tag = Tag.objects.get(user=self.user, name='Soup')
        self.assertIn(new_tag, recipe.tags.all())

    def test_update_recipe_assign_tag(self):
        """Assigning an existing tag when creating a recipe."""

        tag_breakfast = Tag.objects.create(user=self.user, name='Breakfast')
        recipe = create_recipe(user=self.user)

        # assign a tag_breakfast to a recipe
        recipe.tags.add(tag_breakfast)

        tag_lunch = Tag.objects.create(user=self.user, name='Lunch')
        payload = {'tags': [{'name': 'Lunch'}]}

        url = detail_url(recipe.id)
        # change breakfast tag to lunch
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # recipe.tags.all() query returns all the tags associated w/ recipe
        # self.assertIn() checks if the tag_lunch is among those tags
        self.assertIn(tag_lunch, recipe.tags.all())
        self.assertNotIn(tag_breakfast, recipe.tags.all())

    def test_clear_recipe_tags(self):
        """Test clearing a recipes tags."""
        tag = Tag.objects.create(user=self.user, name='Dessert')
        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag)

        payload = {'tags': []}

        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.tags.count(), 0)

    def test_create_recipe_with_new_ingredients(self):
        """Test creating a recipe with new ingredients."""

        payload = {
            'title': 'Poke bowl.',
            'time_minutes': 15,
            'price': Decimal('10.00'),
            'ingredients': [{'name': 'White Rice'}, {'name': 'Tuna'}],
        }

        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # retrieve all the recipes assigned to self.user
        recipes = Recipe.objects.filter(user=self.user)
        # retrieve the 1st recipe
        recipe = recipes[0]

        # check that only 1 recipe is assigned to self.user
        self.assertEqual(recipes.count(), 1)
        # check that number of ingredients is 2
        self.assertEqual(recipe.ingredients.count(), 2)

        for ingredient in payload['ingredients']:
            exists = recipe.ingredients.filter(
                user=self.user,
                name=ingredient['name'],
            ).exists()
            self.assertTrue(exists)

    def test_create_recipe_with_existing_ingredient(self):
        """Test creating a recipe with existing ingredients."""

        # check if ingr_honey was reassigned to the recipe, not created again

        ingr_honey = Ingredient.objects.create(user=self.user, name='Honey')
        payload = {
            'title': 'Medovyk',
            'time_minutes': 120,
            'price': Decimal('30.00'),
            'ingredients': [{'name': 'Honey'}, {'name': 'Flour'}],
        }

        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipes = Recipe.objects.filter(user=self.user)
        recipe = recipes[0]

        self.assertEqual(recipes.count(), 1)
        self.assertEqual(recipe.ingredients.count(), 2)  # not 3
        # check if ingr_honey is in the list of ingredients in recipe
        self.assertIn(ingr_honey, recipe.ingredients.all())

        for ingredient in payload['ingredients']:  # Honey, Flour
            exists = recipe.ingredients.filter(
                user=self.user,
                name=ingredient['name'],
            ).exists()
            self.assertTrue(exists)

    def test_create_ingredient_on_update(self):
        """Test creating an ingredient when updating a recipe."""

        recipe = create_recipe(user=self.user)

        payload = {'ingredients': [{'name': 'Eggs'}]}

        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        new_ingredient = Ingredient.objects.get(user=self.user, name='Eggs')

        # check if new_ingredient was properly created and assigned to a recipe
        self.assertIn(new_ingredient, recipe.ingredients.all())

    def test_update_recipe_assign_ingredient(self):
        """Assigning an existing ingredient when creating a recipe."""

        ingredient_cream = Ingredient.objects.create(
            user=self.user, name='Cream'
            )
        recipe = create_recipe(user=self.user)
        recipe.ingredients.add(ingredient_cream)

        ingredient_jelly = Ingredient.objects.create(
            user=self.user, name='Jelly'
            )
        payload = {'ingredients': [{'name': 'Jelly'}]}

        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # check that ingredient_juice is assigned to a recipe
        self.assertIn(ingredient_jelly, recipe.ingredients.all())
        # check that ingredient_milk is removed from recipe
        self.assertNotIn(ingredient_cream, recipe.ingredients.all())

    def test_clear_recipe_ingredients(self):
        """Test clearing a recipes ingredients."""

        ingredient = Ingredient.objects.create(user=self.user, name='Avocado')
        recipe = create_recipe(user=self.user)
        recipe.ingredients.add(ingredient)

        payload = {'ingredients': []}

        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.ingredients.count(), 0)

    def test_filter_by_tags(self):
        """Test filtering recipes by tags."""
        r1 = create_recipe(user=self.user, title='Creme Brulee')
        r2 = create_recipe(user=self.user, title='Panna Cotta')
        r3 = create_recipe(user=self.user, title='Keema')

        t1 = Tag.objects.create(user=self.user, name='French')
        t2 = Tag.objects.create(user=self.user, name='Italian')

        # add tags 1,2 to recipes
        r1.tags.add(t1)
        r2.tags.add(t2)

        params = {'tags': f'{t1.id},{t2.id}'}

        # get all recipes (1,2) associated with tag IDs in params
        res = self.client.get(RECIPES_URL, params)

        # get serialized version of recipes
        s1 = RecipeSerializer(r1)
        s2 = RecipeSerializer(r2)
        s3 = RecipeSerializer(r3)

        self.assertIn(s1.data, res.data)
        self.assertIn(s2.data, res.data)
        self.assertNotIn(s3.data, res.data)

    def test_filter_by_ingredients(self):
        """Test filtering recipes by ingredients."""

        r1 = create_recipe(user=self.user, title='Posh Beans on Toast')
        r2 = create_recipe(user=self.user, title='Chicken Cacciatore')
        r3 = create_recipe(user=self.user, title='Red Lentil Daal')

        i1 = Ingredient.objects.create(user=self.user, name='Feta Cheese')
        i2 = Ingredient.objects.create(user=self.user, name='Chicken')

        # add ingredients 1,2 to recipes
        r1.ingredients.add(i1)
        r2.ingredients.add(i2)

        params = {'ingredients': f'{i1.id},{i2.id}'}

        # get all recipes (1,2) associated with ingredient IDs in params
        res = self.client.get(RECIPES_URL, params)

        # get serialized version of recipes
        s1 = RecipeSerializer(r1)
        s2 = RecipeSerializer(r2)
        s3 = RecipeSerializer(r3)

        self.assertIn(s1.data, res.data)
        self.assertIn(s2.data, res.data)
        self.assertNotIn(s3.data, res.data)


class ImageUploadTests(TestCase):
    """Tests for the image uploads API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'password',
        )
        self.client.force_authenticate(self.user)
        self.recipe = create_recipe(user=self.user)

    def tearDown(self):  # runs after every test

        # deletes image created
        # Reason: to not build up many images on the system
        self.recipe.image.delete()

    def test_upload_image(self):
        """Test uploading image to a recipe."""

        url = image_upload_url(self.recipe.id)

        # Create a named temporary file as "image_file" that user uploads
        # After with.. ends, temporary file will be deleted
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            # create img that user uploads
            img = Image.new('RGB', (10, 10))
            # save the img to image_file
            img.save(image_file, format='JPEG')
            # seek to the beginning of image_file
            image_file.seek(0)
            # generate a payload as a multipart upload format
            payload = {'image': image_file}
            # multipart: has text and binary data
            res = self.client.post(url, payload, format='multipart')

        # rfresh self.recipe created in setUp
        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # check that image is in the res.data response
        self.assertIn('image', res.data)
        # check that the path of image on the recipe exists
        # so that we know it was successfuly uploaded
        self.assertTrue(os.path.exists(self.recipe.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading invalid image."""

        url = image_upload_url(self.recipe.id)
        # posting a string of text, not an image
        payload = {'image': 'notanimage'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
