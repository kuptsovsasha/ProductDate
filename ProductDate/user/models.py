from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Types(models.TextChoices):
        COMPANY_USER = "COMPANY_USER", "Company_user"
        SHOP_ADMIN_USER = "SHOP_ADMIN_USER", "Shop_admin_user"
        SHOP_USER = "SHOP_USER", "Shop_user"

    type = models.CharField(max_length=50, choices=Types.choices, default=Types.SHOP_USER)
    name = models.CharField(blank=True, max_length=255)


class CompanyManger(models.Manager):
    def queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.COMPANY_USER)


class ShopAdminManger(models.Manager):
    def queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.SHOP_ADMIN_USER)


class ShopManger(models.Manager):
    def queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.SHOP_USER)


class CompanyUser(User):
    objects = CompanyManger

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.COMPANY_USER
        return super().save(*args, **kwargs)


class ShopAdminUser(User):
    objects = ShopAdminManger

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.COMPANY_USER
        return super().save(*args, **kwargs)


class ShopUser(User):
    objects = ShopManger

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.COMPANY_USER
        return super().save(*args, **kwargs)
