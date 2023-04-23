from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True,
        blank=False,
        null=False
    )
    measurement_unit = models.CharField(
        max_length=200,
        blank=False,
        null=False
    )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        blank=False,
        null=False
    )
    color = ColorField(
        max_length=7,
        blank=False,
        null=False,
        unique=True
    )
    slug = models.SlugField(
        max_length=200,
        blank=False,
        null=False,
        unique=True
    )

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        blank=False,
        null=False
    )

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag)
    ingredients = models.ManyToManyField(RecipeIngredient)
    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        null=False
    )
    name = models.CharField(
        max_length=200,
        unique=True,
        blank=False,
        null=False
    )
    text = models.TextField(
        blank=False,
        null=False
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)],
        blank=False,
        null=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    def __str__(self):
        return f'{self.user}'
    
    class Meta():
        models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_favorite_recipe'
        )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
        )
    recipe = models.ForeignKey(Recipe,
        on_delete=models.CASCADE
        )

    def __str__(self):
        return f'{self.user}'

    class Meta():
        models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_favorite_recipe'
        )
