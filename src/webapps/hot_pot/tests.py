from django.test import TestCase
# from django.test import Client

from django.contrib.auth.models import User


# Create your tests here.
class ProfileTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="aaa",
                                password="aaa",
                                first_name="aaa",
                                last_name="aaa",
                                email="aaa@gmail.com")

    def test_create_profile(self):
        p = User.objects.get(username="aaa")
        self.assertEqual(p.username,"aaa")
        self.assertEqual(p.first_name, "aaa")
        self.assertEqual(p.last_name, "aaa")
        self.assertEqual(p.email, "aaa@gmail.com")



