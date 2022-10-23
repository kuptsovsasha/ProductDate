from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersTests(TestCase):

    def test_create_shop_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='test_shop_user', password='foo', email='shop@user.com')
        self.assertEqual(user.email, 'shop@user.com')
        self.assertEqual(user.type, User.Types.SHOP_USER)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(username='superuser', password='foo', email='super@user.com')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
