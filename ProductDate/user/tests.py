from django.contrib.auth import get_user_model
from django.test import TestCase
from django_rest_passwordreset.models import ResetPasswordToken
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


class UsersTests(TestCase):
    def test_create_shop_user(self):
        user = User.objects.create_user(
            username="test_shop_user", password="foo", email="shop@user.com"
        )
        self.assertEqual(user.email, "shop@user.com")
        self.assertEqual(user.type, User.Types.SHOP_USER)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username="superuser", password="foo", email="super@user.com"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class UserAPITests(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.super_user = User.objects.create_superuser(
            username="superuser", password="foo", email="super@user.com"
        )

    def test_create_shop_user(self):
        self.client.force_authenticate(self.super_user)
        url = "/user/user_create/"
        data = {"username": "test_shop_user", "password": "foo"}
        request = self.client.post(url, data=data)

        self.assertEqual(201, request.status_code)
        self.assertEqual(2, User.objects.all().count())
        self.assertEqual(data["username"], request.data["user"]["username"])
        self.assertEqual(self.super_user.email, request.data["user"]["email"])

    def test_update_shop_user(self):
        self.test_create_shop_user()
        shop_user = User.objects.filter(type=User.Types.SHOP_USER).last()
        self.client.force_authenticate(shop_user)
        url = "/user/user_update/"
        data = {"first_name": "Test", "last_name": "Update"}
        request = self.client.patch(url, data=data)

        self.assertEqual(200, request.status_code)
        self.assertEqual(data["first_name"], request.data["first_name"])
        self.assertEqual(data["last_name"], request.data["last_name"])

    def test_change_user_password(self):
        self.test_create_shop_user()
        shop_user = User.objects.filter(type=User.Types.SHOP_USER).last()
        self.client.force_authenticate(shop_user)
        url = "/user/change_password/"
        data = {"old_password": "foo", "new_password": "new"}
        request = self.client.patch(url, data=data)

        self.assertEqual(200, request.status_code)
        self.assertEqual("success", request.data["status"])

    def test_reset_user_password(self):
        self.test_create_shop_user()
        shop_user = User.objects.filter(type=User.Types.SHOP_USER).last()
        self.client.force_authenticate(shop_user)
        url_for_token = "/user/password_reset/"
        data_for_token = {"email": "super@user.com"}
        request_for_token = self.client.post(url_for_token, data=data_for_token)

        self.assertEqual(200, request_for_token.status_code)
        self.assertEqual("OK", request_for_token.data["status"])

        url_for_confirm_new_password = "/user/password_reset/confirm/"
        reset_token = ResetPasswordToken.objects.all().last()
        data_for_confirm_new_password = {
            "password": "new_pass",
            "token": reset_token.key,
        }
        request_for_confirm_new_password = self.client.post(
            url_for_confirm_new_password, data=data_for_confirm_new_password
        )

        self.assertEqual(200, request_for_confirm_new_password.status_code)
        self.assertEqual("OK", request_for_confirm_new_password.data["status"])
