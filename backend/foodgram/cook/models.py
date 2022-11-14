from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredients(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True,
        blank=False,
        null=False,
    )
    measurement_unit = models.CharField(
        max_length=200,
    )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tags(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = ColorField(default='#FF0000')
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Recipes(models.Model):
    tags = models.ManyToManyField(Tags)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    name = models.CharField(max_length=200, unique=True)
    text = models.TextField()
    cooking_time = models.IntegerField(
        blank=False, validators=[MinValueValidator(1)])
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredients = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.recipe} {self.ingredients}'


class Favorite(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='recipes_favorites',)
    recipe = models.ForeignKey(Recipes,
                               on_delete=models.CASCADE,
                               related_name='favorites',)

    def __str__(self):
        return f'{self.user}'
    
    class Meta():
        models.UniqueConstraint(
            fields=['user', 'recipe'], name='unique_recording')


class ShoppingCart(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='shopping_carts',)
    recipe = models.ForeignKey(Recipes,
                               on_delete=models.CASCADE,
                               related_name='shopping_carts',)

    def __str__(self):
        return f'{self.user}'

    class Meta():
        models.UniqueConstraint(
            fields=['user', 'recipe'], name='unique_recording')
