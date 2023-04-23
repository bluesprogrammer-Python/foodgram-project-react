from django.core.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.serializers import UserSerializer

from cook.models import (Favorite, Recipe, ShoppingCart, Tag, RecipeIngredient,
                     Ingredient)

COUNT = 'amount'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'ingredient', 'recipe', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    ingredient = IngredientRecipeSerializer(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'ingredient', 'tag', 'image',
                  'name', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj.id).exists()

    def validate(self, data):
        ingredients = self.initial_data.get('ingredient')
        ingredients_list = {}
        if ingredients:
            for ingredient in ingredients:
                if ingredient.get('id') in ingredients_list:
                    raise ValidationError(
                        ('Ингридиенты должны быть уникальными'))
                ingredients_list[ingredient.get('id')] = (
                    ingredients_list.get('amount')
                )
            return data
        else:
            raise ValidationError(('Необходимо добавить ингридиенты'))

    def ingredient_recipe_create(self, ingredients_set, recipe):
        for ingredient_get in ingredients_set:
            ingredient = Ingredient.objects.get(
                id=ingredient_get.get('id')
            )
            RecipeIngredient.objects.create(ingredient=ingredient,
                                             recipe=recipe,
                                             amount=ingredient_get.get(COUNT)
                                             )

    def create(self, validated_data):
        image = validated_data.pop('image')
        recipe = Recipe.objects.create(image=image,
                                        author=self.context['request'].user,
                                        **validated_data
                                        )
        tag = self.initial_data.get('tag')
        recipe.tags.set(tag)
        ingredients_set = self.initial_data.get('ingredient')
        self.ingredient_recipe_create(ingredients_set, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        instance.tag.clear()
        tags = self.initial_data.get('tag')
        instance.tag.set(tags)
        instance.save()
        RecipeIngredient.objects.filter(recipe=instance).delete()
        ingredients_set = self.initial_data.get('ingredient')
        self.ingredient_recipe_create(ingredients_set, instance)
        return instance


class ShoppingCardSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.ImageField(source='recipe.image')
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = ShoppingCart
        fields = ('id', 'user', 'recipe')


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.ImageField(source='recipe.image')
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = Favorite
        fields = ('id', 'user', 'recipe')