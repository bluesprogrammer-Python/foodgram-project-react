from django.urls import include, path
from rest_framework import routers

from api.views import RecipeViewSet, TagViewSet, IngredientViewSet

router = routers.DefaultRouter()
router.register(r'recipe', RecipeViewSet, basename='recipe')
router.register(r'tag', TagViewSet, basename='tag')
router.register(r'ingredient', IngredientViewSet, basename='ingredient')
urlpatterns = [
    path('', include(router.urls)),
]
