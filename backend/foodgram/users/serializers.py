from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.core.exceptions import ValidationError
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import Follow, User


class UserGetSerializer(UserSerializer):
    """GET-method: User list."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        if (self.context.get('request')
                and not self.context['request'].user.is_anonymous):
            return Follow.objects.filter(user=self.context['request'].user,
                                         author=obj).exists()
        return False


class CustomUserCreateSerializer(UserCreateSerializer):
    """POST-method: User create."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'password')

    def validate(self, data):
        user = User(**data)
        password = data.get('password')
        username = data.get('username')
        email = data.get('email')
        errors = dict()
        if username.lower() == 'me':
            errors['username'] = 'Нельзя использовать "me" для username'
        if username.lower() == email.lower():
            errors['username'] = 'username не должен совпадать с email'
        try:
            validate_password(password=password, user=user)
        except ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(data)


class SetPasswordSerializer(serializers.Serializer):
    """POST-method: Password change."""
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, obj):
        try:
            validate_password(obj['new_password'])
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {'new_password': list(e.messages)}
            )
        return super().validate(obj)

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data['current_password']):
            raise serializers.ValidationError(
                {'current_password': 'Неправильный пароль.'}
            )
        if (validated_data['current_password']
                == validated_data['new_password']):
            raise serializers.ValidationError(
                {'new_password': 'Новый пароль должен отличаться от текущего.'}
            )
        instance.set_password(validated_data['new_password'])
        instance.save()
        return validated_data
