from .models import ingredients, Tags, Recipes, ingredient_recipe
from rest_framework import serializers


class RecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ('id', 'ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time')


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug')


class ingredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ingredients
        fields = ('id', 'name', 'measurement_unit')
