from django.urls import include, path
from rest_framework import routers

from .views import RecipesViewSet, TagsViewSet, ingredientsViewSet

router = routers.DefaultRouter()
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'ingredients', ingredientsViewSet, basename='ingredients')
urlpatterns = [
    path('', include(router.urls)),
    #path('recipes/download_shopping_cart/'),
    #path('recipes/id/shopping_cart/'),
    #path('recipes/id/favorite/'),
]
