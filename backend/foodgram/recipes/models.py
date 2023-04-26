from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField

User = get_user_model()

class Ingredient(models.Model):
    GRAM = 'г'
    KILOGRAM = 'кг'
    MILLILITER = 'мл'
    LITER = 'л'
    TEASPOON = 'ч.л.'
    TABLESPOON = 'ст.л.'
    ITEM = 'шт'

    MEASUREMENT_UNITS = (
        (GRAM, 'г'),
        (KILOGRAM, 'кг'),
        (MILLILITER, 'мл'),
        (LITER, 'л'),
        (TEASPOON, 'ч.л.'),
        (TABLESPOON, 'ст.л.'),
        (ITEM, 'шт'),
    )

    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200, choices=MEASUREMENT_UNITS)

    class Meta:
        unique_together = ('name', 'measurement_unit')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True, null=True)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipes/')
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField('Tag', related_name='recipes')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(
            1, message='Время приготовления должно быть не менее 1 минуты!'
        )]
    )
    def __str__(self):
        return self.name

class IngredientAmount(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.ingredient.name} - {self.amount} {self.ingredient.measurement_unit}'

class Favorite(models.Model):
    """ Модель избранного. """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorites',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        unique_together = ['user', 'recipe']
    
    def __str__(self):
        return f'{self.recipe.name} - {self.user.username}'


class RecipeTag(models.Model):
    """ Модель связи тега и рецепта. """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег'
    )

    class Meta:
        unique_together = ('recipe', 'tag',)

class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзина покупок'
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Корзину покупок'