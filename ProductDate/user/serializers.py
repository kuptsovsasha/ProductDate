from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..company.models import Shop
from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "password",
            "username",
            "first_name",
            "last_name",
            "email",
            "company",
            "shop",
        ]

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
