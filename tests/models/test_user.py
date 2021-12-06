import unittest

from faker import Faker

from .model_test import ModelTest


class TestUser(ModelTest):
    """Tests for User table methods."""

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

    # Generate a random user to use in the tests
    def generate_random_user():
        email = TestUser.faker.email()
        password = TestUser.faker.password()
        first_name = TestUser.faker.first_name()
        last_name = TestUser.faker.last_name()
        location = TestUser.faker.city()
        date_of_birth = TestUser.faker.date_of_birth()
        profile_pic = 'mib/static/images/test.png'

        is_active = True
        is_admin = False
        authenticated = False
        is_reported = False
        is_banned = False
        language_filter = False
    
        from mib.models import User

        user = User(
            email=email,
            password=password,
            is_active=is_active,
            is_admin=is_admin,
            is_reported=is_reported,
            is_banned=is_banned,
            has_language_filter= language_filter,
            authenticated=authenticated,
            first_name=first_name,
            last_name=last_name,
            location=location,
            date_of_birth=date_of_birth,
            profile_pic=profile_pic
        )

        return user
    
    # Set <email>
    def test_set_email(self):
        user = TestUser.generate_random_user()
        email = self.faker.email()
        user.set_email(email)
        self.assertEqual(email, user.email)

    # Set <first_name>
    def test_firstname(self):
        user = TestUser.generate_random_user()
        first_name = self.faker.first_name()
        user.set_first_name(first_name)
        self.assertEqual(first_name, user.first_name)

    # Set <last_name>
    def test_set_lastname(self):
        user = TestUser.generate_random_user()
        last_name = self.faker.last_name()
        user.set_last_name(last_name)
        self.assertEqual(last_name, user.last_name)

    # Set <password>
    def test_set_password(self):
        user = TestUser.generate_random_user()
        password = self.faker.password(length=10, special_chars=False, upper_case=False)
        user.set_password(password)

        self.assertEqual(
            user.authenticate(password),
            True
        )

    # Set <date_of_birth>
    def test_set_dateofbirth(self):
        user = TestUser.generate_random_user()
        date_of_birth = self.faker.date_of_birth()
        user.set_date_of_birth(date_of_birth)
        self.assertEqual(date_of_birth, user.date_of_birth)

    # Set <location>
    def test_set_location(self):
        user = TestUser.generate_random_user()
        location = self.faker.city()
        user.set_location(location)
        self.assertEqual(location, user.location)

    # Set <profile_pic>
    def test_set_profile_pic(self):
        user = TestUser.generate_random_user()
        profile_pic = 'mib/static/images/test.png'
        user.set_profile_pic(profile_pic)
        self.assertEqual(profile_pic, user.profile_pic)

    # Set <is_banned>
    def test_update_banned(self):
        user = TestUser.generate_random_user()
        is_banned = user.is_banned
        user.update_banned()
        self.assertEqual(not is_banned, user.is_banned)

    # Set <has_language_filter>
    def test_update_language_filter(self):
        user = TestUser.generate_random_user()
        has_language_filter = user.has_language_filter
        user.update_language_filter()
        self.assertEqual(not has_language_filter, user.has_language_filter)

    # Get <is_authenticated>
    def test_is_authenticated(self):
        user = TestUser.generate_random_user()
        user.authenticated=1
        self.assertTrue(user.is_authenticated())

    # Set <is_active>
    def test_set_active(self):
        user = TestUser.generate_random_user()
        self.assertTrue(user.is_active)

        user.set_active(False)
        self.assertFalse(user.is_active)

    # Set <is_reported>
    def test_set_reported(self):
        user = TestUser.generate_random_user()
        self.assertFalse(user.is_reported)

        user.set_reported(True)
        self.assertTrue(user.is_reported)
