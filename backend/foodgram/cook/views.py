from django.shortcuts import render

from rest_framework import viewsets
from .serializers import ingredientsSerializer, RecipesSerializer, TagsSerializer
from .models import ingredients, Tags, Recipes, ingredient_recipe


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class ingredientsViewSet(viewsets.ModelViewSet):
    queryset = ingredients.objects.all()
    serializer_class = ingredientsSerializer
