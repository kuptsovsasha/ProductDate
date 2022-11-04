from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created

from ProductDate.company.models import Company, Shop


class User(AbstractUser):
    class Types(models.TextChoices):
        COMPANY_USER = "COMPANY_USER", "Company_user"
        SHOP_ADMIN_USER = "SHOP_ADMIN_USER", "Shop_admin_user"
        SHOP_USER = "SHOP_USER", "Shop_user"

    type = models.CharField(
        max_length=50, choices=Types.choices, default=Types.SHOP_USER
    )
    name = models.CharField(blank=True, max_length=255)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, blank=True, null=True
    )
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)


class CompanyManger(models.Manager):
    def queryset(self, *args, **kwargs):
        return (
            super().get_queryset(*args, **kwargs).filter(type=User.Types.COMPANY_USER)
        )


class ShopAdminManger(models.Manager):
    def queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(type=User.Types.SHOP_ADMIN_USER)
        )


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


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):

    email_plaintext_message = "{}?token={}".format(
        reverse("password_reset:reset-password-request"), reset_password_token.key
    )

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email],
    )
