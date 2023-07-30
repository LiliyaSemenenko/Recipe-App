"""
Serializers for recipe API.
"""
from rest_framework import serializers

from core.models import Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    # link tag serializer
    # many=True: means its a list of tags
    tags = TagSerializer(many=True, required=False)

    # set the Recipe model to this serializer
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed."""

        # request an auth user to assign tags to it
        auth_user = self.context['request'].user

        # loop through ea tag from validated_data
        for tag in tags:
            # get_or_create: gets value if exists, or creates if doesn't
            # prevents duplicates
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                # ** used to get all the values/fields that passed to 'tag'
                **tag,
            )
            recipe.tags.add(tag_obj)

    # add create method to allow creating nested values (tags here)
    # Note: overriding default behavior that makes nested values read-only
    def create(self, validated_data):
        """Create a recipe."""

        # remove tags from validated_data & assign them to 'tags' variable
        # if tags don't exist, dafault to an empty list
        tags = validated_data.pop('tags', [])

        # pass everything but tags to a new recipe
        recipe = Recipe.objects.create(**validated_data)

        self._get_or_create_tags(tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        """Update recipe."""

        # remove tags from validated_data & assign them to 'tags' variable
        # if tags don't exist, dafault to None
        tags = validated_data.pop('tags', None)

        # empty list
        if tags is not None:
            # clear existing tags assigned
            instance.tags.clear()
            # create new tags
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            # assign to instance
            setattr(instance, attr, value)

        instance.save()

        return instance


# RecipeDetailSerializer is an extention of RecipeSerializer
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    # pass all the meta values from Meta() in RecipeSerializer
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
