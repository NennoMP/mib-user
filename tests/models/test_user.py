import unittest

from faker import Faker

from .model_test import ModelTest


class TestUser(ModelTest):

    faker = Faker()

    @classmethod
    def setUpClass(cls):
        super(TestUser, cls).setUpClass()

        from mib.models import user
        cls.user = user

    @staticmethod
    def assertUserEquals(value, expected):
        t = unittest.FunctionTestCase(TestUser)
        t.assertEqual(value.email, expected.email)
        t.assertEqual(value.password, expected.password)
        t.assertEqual(value.is_active, expected.is_active)
        t.assertEqual(value.authenticated, False)
        t.assertEqual(value.is_anonymous, expected.is_anonymous)

    
    def generate_random_user():
        email = TestUser.faker.email()
        password = TestUser.faker.password()
        first_name = TestUser.faker.first_name()
        last_name = TestUser.faker.last_name()
        location = TestUser.faker.city()
      

        from mib.models import User

        user = User(
            email=email,
            password=password,
            is_active=1,
            is_admin=0,
            is_reported=0,
            is_banned=0,
            has_language_filter= 0,
            authenticated=0,
            is_anonymous=1,
            first_name=first_name,
            last_name=last_name,
            location=location
        )

        return user

    
    def test_set_password(self):
        user = TestUser.generate_random_user()
        password = self.faker.password(length=10, special_chars=False, upper_case=False)
        user.set_password(password)

        self.assertEqual(
            user.authenticate(password),
            True
        )
    
    def test_set_email(self):
        user = TestUser.generate_random_user()
        email = self.faker.email()
        user.set_email(email)
        self.assertEqual(email, user.email)

    def test_is_authenticated(self):
        user = TestUser.generate_random_user()
        self.assertFalse(user.is_authenticated())

        user = TestUser.generate_random_user()
        user.authenticated=1
        self.assertTrue(user.is_authenticated())

    def test_set_active(self):
        user = TestUser.generate_random_user()
        self.assertTrue(user.is_active)

        user.set_active(False)
        self.assertFalse(user.is_active)

    def test_set_reported(self):
        user = TestUser.generate_random_user()
        self.assertFalse(user.is_reported)

        user.set_reported(True)
        self.assertTrue(user.is_reported)