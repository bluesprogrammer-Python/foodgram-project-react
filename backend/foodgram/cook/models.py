from django.db import models
from users.models import User
from django.core.validators import MinValueValidator
from colorfield.fields import ColorField


class ingredients(models.Model):
    """Класс для представления списка ингридиентов.
    """
    name = models.CharField(
        max_length=200,
        db_index=True,
        blank=False,
        null=False,
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tags(models.Model):
    """Класс для представления списка тегов.
    """
    name = models.CharField(max_length=200, unique=True)
    color = ColorField(default='#FF0000')
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Recipes(models.Model):
    """Класс для представления списка рецептов.
    """
    ingredients = models.ManyToManyField(ingredients, through='ingredient_recipe')
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


class ingredient_recipe(models.Model):
    """
    Класс для представления ингридиентов в рецепте.
    """
    ingredients = models.ForeignKey(ingredients, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe} {self.ingredients}' 
