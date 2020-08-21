from django.contrib.auth import get_user_model, authenticate, password_validation
from django.utils.translation import ugettext_lazy as _
from core.models import Role

from rest_framework import serializers


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for roles"""
    class Meta:
        model = Role
        fields = ('id', 'name')
        read_only_fields = ('id',)

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'name', 'surname', 'role', 'dateCreated', 'phone')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs



class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=200, write_only=True, required=True)
    new_password = serializers.CharField(max_length=200, write_only=True, required=True)
    confirm_password = serializers.CharField(max_length=200, write_only=True, required=True)

    def validate(self, data):
        if not self.context['request'].user.check_password(data.get('old_password')):
            raise serializers.ValidationError({'old_password': 'Wrong old password'})

        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Not same.'})
        password_validation.validate_password(data['new_password'], self.context['request'].user)
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user
