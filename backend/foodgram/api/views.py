import io

from django.db.models import Sum
from django.http import FileResponse
from django.utils.translation import gettext as _
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.permission import AuthorOrReadOnly

from cook.models import (Favorite, Recipe, ShoppingCart, Tag, RecipeIngredient,
                     Ingredient)
from .serializers import (FavoriteSerializer, RecipeSerializer,
                          ShoppingCardSerializer, TagSerializer,
                          IngredientSerializer)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrReadOnly,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend, )

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.add_obj(model=Favorite,
                                pk=pk,
                                serializers=FavoriteSerializer,
                                user=request.user)
        elif request.method == 'DELETE':
            return self.del_obj(model=Favorite, pk=pk, user=request.user)
        return None

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.add_obj(model=ShoppingCart,
                                pk=pk,
                                serializers=ShoppingCardSerializer,
                                user=request.user)
        if request.method == 'DELETE':
            return self.del_obj(model=ShoppingCart, pk=pk, user=request.user)
        return Response(_('Разрешены только POST и DELETE запросы'),
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_carts__user=user).values(
                'ingredient__name',
                'ingredient__measurement_unit').annotate(amount=Sum('amount'))
        buffer = io.BytesIO()
        canvas = Canvas(buffer)
        pdfmetrics.registerFont(
            TTFont('FreeSans', 'FreeSans.ttf'))
        canvas.setFont('FreeSans', size=16)
        for ingredient in ingredients:
            canvas.drawString(f"{ingredient['ingredient__name']}")
            canvas.drawString(f"{ingredient['amount']}")
            canvas.drawString(f"{ingredient['ingredient__measurement_unit']}")
        canvas.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True,
                            filename='ShoppingCart.pdf')
