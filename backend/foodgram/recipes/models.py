from django.core.validators import MinValueValidator
from django.db import models
from django.utils.html import format_html
from users.models import User


class Tag(models.Model):
    """Tags model"""
    name = models.CharField(max_length=200,
                            verbose_name='Название')
    color = models.CharField(max_length=7,
                             verbose_name='Цвет в HEX',
                             default='#ffffff')
    slug = models.SlugField(max_length=200,
                            unique=True,
                            verbose_name='Уникальный слаг')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    # def colored_name(self):
    #     return format_html(
    #         '<span style="color: #{};">{}</span>',
    #         self.color,
    #     )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredients model"""
    name = models.CharField(max_length=200,
                            verbose_name='Ингредиент')
    measurement_unit = models.CharField(max_length=200,
                                        verbose_name='Ед. измерения')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Follow(models.Model):
    """Following model"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Подписчик'
                             )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Автор',
                               )

    class Meta:
        unique_together = ('user', 'author',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Recipe(models.Model):
    """Recipes model"""
    tags = models.ManyToManyField(Tag,
                                  related_name='recipes',
                                  verbose_name='Тэг',
                                  blank=False)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор')
    ingredients = models.ManyToManyField(Ingredient,
                                         related_name='recipes',
                                         verbose_name='Ингредиенты',
                                         blank=True)
    is_favorited = models.BooleanField(blank=False,
                                       default=False,
                                       verbose_name='Находится ли в избранном')
    is_in_shopping_cart = models.BooleanField(blank=False,
                                              default=False,
                                              verbose_name=
                                              'Находится ли в корзине')
    name = models.CharField(max_length=200,
                            unique=True,
                            blank=False,
                            verbose_name='Название рецепта')
    image = models.URLField(blank=False,
                            verbose_name='Фото рецепта')
    text = models.TextField(blank=False,
                            verbose_name='Описание рецепта')
    cooking_time = models.PositiveIntegerField(
        validators=(MinValueValidator(1, message='Значение не менее "1"'),),
        verbose_name='Время приготовления',
        blank=False
    )
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата и время публикации')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='ingredient_amount')
    amount = models.DecimalField(max_digits=6,
                                 decimal_places=2,
                                 validators=(MinValueValidator(0.01),))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_recipe_ingredient'
            )
        ]
