from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..company.models import Shop
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        if not validated_data.get("email"):
            validated_data["email"] = self.context["request"].user.email
        user = User.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"],
        )

        return user

    def validate(self, attrs):
        user = self.context["request"].user
        if user.is_superuser:
            return attrs
        elif user.type == User.Types.COMPANY_USER:
            company_id = attrs.get("company")
            if not company_id or company_id != user.company_id:
                raise ValidationError("Add valid company")
        else:
            shop_id = attrs.get("shop")
            if not shop_id:
                raise ValidationError("Add shop id")
            shop = Shop.objects.filter(id=shop_id).last()
            if shop.company_id != user.company_id:
                raise ValidationError("Add valid company")

        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
