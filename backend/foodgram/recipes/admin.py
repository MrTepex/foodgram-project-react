from django.contrib import admin

from .models import (FavoriteRecipe, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


if not hasattr(admin, 'display'):
    def custom_decorator_for_admin(description):
        """Это декоратор для django версий ниже 3.2,
        где отсутствует декоратор <@admin.display>
        """
        def wrapper(fn):
            fn.short_description = description
            return fn
        return wrapper
    setattr(admin, 'display', custom_decorator_for_admin)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    empty_value_display = '-empty-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'times_favorited')
    readonly_fields = ('times_favorited',)
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-empty-'

    @admin.display(description='Кол-во добавлений в избранное')
    def times_favorited(self, obj):
        return obj.favorite_recipe.count()


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


@admin.register(FavoriteRecipe)
class FavoriteRcipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
