from django.contrib import admin
from django.db.models import Count

from users.models import User
from .models import Follow, Ingredient, Recipe, RecipeIngredient, Tag


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, )
    list_display = ('name', 'author')
    list_filter = ('author__username', 'name', 'tags__slug')
    empty_value_display = '-empty-'

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     return queryset.annotate(favorite_count=Count('favored_by'))
    #
    # @staticmethod
    # def get_favorite_count(obj):
    #     return obj.favorite_count


class UserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email')
    empty_value_display = '-empty-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    empty_value_display = '-empty-'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(User, UserAdmin)
admin.site.register(Follow)
admin.site.register(Recipe, RecipeAdmin)
