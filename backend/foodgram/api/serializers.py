from drf_base64.fields import Base64ImageField
from recipes.models import (FavoriteRecipe, Ingredient, Recipe,
                            RecipeIngredient,
                            ShoppingCart, Tag)
from rest_framework import serializers

from users.models import Follow, User
from users.serializers import UserGetSerializer


class RecipeSerializer(serializers.ModelSerializer):
    """GET-method: Recipes list."""
    image = Base64ImageField(read_only=True)
    name = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    """GET-method: Following authors list."""
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        return (self.context.get('request').user.is_authenticated
                and Follow.objects.filter(user=self.context['request'].user,
                                          author=obj).exists())

    @staticmethod
    def get_recipes(obj):
        recipes = obj.recipes.all()
        serializer = RecipeSerializer(recipes, many=True, read_only=True)
        return serializer.data

    @staticmethod
    def get_recipes_count(obj):
        return obj.recipes.count()


class FollowAuthorSerializer(serializers.ModelSerializer):
    """POST, DELETE-methods: Create or delete a subscription."""
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def validate(self, obj):
        if self.context['request'].user == obj:
            raise serializers.ValidationError(
                {'errors': 'Нельзя подписаться на себя.'})
        return obj

    @staticmethod
    def get_is_subscribed(obj):
        return FollowSerializer.get_is_subscribed(FollowSerializer(), obj)

    @staticmethod
    def get_recipes_count(obj):
        return obj.recipes.count()


class TagSerializer(serializers.ModelSerializer):
    """GET-method: Tags list"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """GET-method: Ingredients list"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """GET-method: Ingredients in recipe list"""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    """Ingredients foe recipe creation"""
    id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeGetSerializer(serializers.ModelSerializer):
    """GET-method: Recipes list"""
    author = UserGetSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(
        many=True,
        read_only=True,
        source='recipes'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        return (self.context.get('request').user.is_authenticated
                and FavoriteRecipe.objects.filter(
                    user=self.context.get('request').user,
                    recipe=obj).exists())

    def get_is_in_shopping_cart(self, obj):
        return (self.context.get('request').user.is_authenticated
                and ShoppingCart.objects.filter(
                    user=self.context.get('request').user,
                    recipe=obj).exists())


class RecipeCreateSerializer(serializers.ModelSerializer):
    """POST, PATCH, DELETE-methods for recipes"""
    id = serializers.ReadOnlyField()
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    author = UserGetSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = RecipeIngredientCreateSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'ingredients', 'tags', 'image', 'name',
                  'text', 'cooking_time')

    def validate(self, value):
        required_fields = ('ingredients', 'tags', 'image', 'name',
                           'text', 'cooking_time')
        for field in required_fields:
            if not value.get(field):
                raise serializers.ValidationError(
                    f'Поле {field} обязательно для заполнения.'
                )
        ingredients_ids = [obj['id'] for obj in value.get('ingredients')]
        unique_ingredients_ids = set(ingredients_ids)
        if len(unique_ingredients_ids) != len(ingredients_ids):
            raise serializers.ValidationError(
                'Ингредиенты не могут повторяться'
            )
        return value

    @staticmethod
    def tags_set(recipe, tags):
        recipe.tags.set(tags)

    @staticmethod
    def ingredients_set(recipe, ingredients):
        RecipeIngredient.objects.bulk_create(
            [RecipeIngredient(
                recipe=recipe,
                ingredient=Ingredient.objects.get(pk=ingredient['id']),
                amount=ingredient['amount']
            ) for ingredient in ingredients]
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            author=self.context.get('request').user,
            **validated_data
        )
        self.tags_set(recipe, tags)
        self.ingredients_set(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        RecipeIngredient.objects.filter(
            recipe=instance,
            ingredient__in=instance.ingredients.all()).delete()
        self.tags_set(instance, tags)
        self.ingredients_set(instance, ingredients)
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeGetSerializer(instance, context=self.context).data
