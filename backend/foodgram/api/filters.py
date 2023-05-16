from django_filters.rest_framework import FilterSet, filters

from cook.models import Recipe, Tag


class RecipeFieldsFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(field_name='tags__slug', to_field_name='slug', queryset=Tag.objects.all())
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_in_shopping_cart', 'is_favorited')

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(carts__user=self.request.user)
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

