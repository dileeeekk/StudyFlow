from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError, transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'university')


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    full_name = serializers.CharField(max_length=150)
    university = serializers.CharField(max_length=200)
    password = serializers.CharField(write_only=True, trim_whitespace=False, min_length=8, max_length=128)
    terms_accepted = serializers.BooleanField()

    def validate_email(self, value):
        value = value.strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('An account with this email already exists.')
        return value

    def validate_terms_accepted(self, value):
        if not value:
            raise serializers.ValidationError('Please accept the Terms of Service and Privacy Policy.')
        return value

    def validate(self, attrs):
        password = attrs['password']
        if not password.strip():
            raise serializers.ValidationError({'password': ['Enter a password with at least 8 characters.']})
        user = User(email=attrs['email'], full_name=attrs['full_name'], university=attrs['university'])
        try:
            validate_password(password, user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError({'password': exc.messages}) from exc
        return attrs

    def create(self, validated_data):
        validated_data.pop('terms_accepted')
        try:
            with transaction.atomic():
                return User.objects.create_user(**validated_data, terms_accepted_at=timezone.now())
        except IntegrityError as exc:
            raise serializers.ValidationError({'email': ['An account with this email already exists.']}) from exc


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs['email'] = attrs['email'].strip().lower()
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data

