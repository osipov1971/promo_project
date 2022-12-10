from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, fields
from promo_app.models import CustomUser, Role, RightForRole
from promo_app.common.serializers import LanguageSerializer
from promo_app.users.filters import FilterRightListSerializer


class UserSerializer(serializers.ModelSerializer):
    username = fields.CharField(max_length=150, required=True)
    name = fields.CharField(max_length=250, required=True)
    email = fields.EmailField(max_length=254, required=False)
    phone_number = fields.CharField(max_length=30, required=False)

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'name', 'email', 'phone_number', 'language', 'phone_number', 'role')


class RightSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = FilterRightListSerializer
        model = RightForRole
        fields = ('id', 'role', 'right', 'level')


class RoleListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=150)
    description = serializers.CharField(required=False)
    users = serializers.SerializerMethodField('get_users')
    rightforrole_set = RightSerializer(many=True)

    def get_users(self, role):
        users = CustomUser.objects.filter(role=role, is_active=True).exclude(is_superuser=True)
        serializer = UserSerializer(users, many=True)
        return serializer.data

    class Meta:
        model = Role
        fields = ('id', 'name', 'description', 'users', 'rightforrole_set')


class RoleWithRightsSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()
    rightforrole_set = RightSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ('id', 'name', 'description', 'rightforrole_set')


class RoleShortInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField(required=False)

    class Meta:
        model = Role
        fields = ('id', 'name', 'description')


class UserDetailSerializer(serializers.ModelSerializer):
    username = fields.CharField(max_length=150, required=True)
    name = fields.CharField(max_length=250, required=True)
    email = fields.EmailField(max_length=254, required=False)
    phone_number = fields.CharField(max_length=30, required=False)
    language = LanguageSerializer(read_only=True)
    role = RoleShortInfoSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'name', 'email', 'phone_number', 'language', 'phone_number', 'role')


class CurrentUserSerializer(serializers.ModelSerializer):
    username = fields.CharField(max_length=150, required=True)
    name = fields.CharField(max_length=250, required=True)
    email = fields.EmailField(max_length=254, required=False)
    phone_number = fields.CharField(max_length=30, required=False)
    language = LanguageSerializer(required=False)
    role = RoleWithRightsSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'name', 'email', 'phone_number', 'language', 'phone_number', 'role')


class PasswordSerialiser(serializers.Serializer):
    old_password = fields.CharField(max_length=150)
    new_password = fields.CharField(max_length=150)

    def validated_new_password(self, value):
        validate_password(value)
        return value
