from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from cook.models import Ingredient, Recipe, Tag

from .models import User


class UserAdmin(UserAdmin):
    list_display = ('username', 'email',
                    'first_name', 'last_name', 'role')
    list_filter = ('email', 'username')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')

    def favorites(self, obj):
        return obj.favorites.count()


admin.site.register(User, UserAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
