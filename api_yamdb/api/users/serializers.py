from rest_framework import serializers

from users.models import User
from users.validators import validate_username
from .mixins import UsernameValidationMixin


class SignUpSerializer(UsernameValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class GetTokenSerializer(UsernameValidationMixin, serializers.Serializer):
    username = serializers.SlugField(
        required=True,
        validators=[validate_username]
    )
    confirmation_code = serializers.SlugField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(UsernameValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class MeSerializer(UsernameValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('username', 'email')
