from faker import Faker

from .dao_test import DaoTest


class TestUserManager(DaoTest):
    faker = Faker()

    @classmethod
    def setUpClass(cls):
        super(TestUserManager, cls).setUpClass()
        from tests.models.test_user import TestUser
        cls.test_user = TestUser
        from mib.dao import user_manager
        cls.user_manager = user_manager.UserManager

    def test_crud(self):
        for _ in range(0, 10):
            user = self.test_user.generate_random_user()
            self.user_manager.create_user(user=user)
            user1 = self.user_manager.retrieve_by_id(user.id)
            self.test_user.assertUserEquals(user1, user)

            user.set_password(self.faker.password())
            user.email = self.faker.email()
            self.user_manager.update_user(user=user)
            user1 = self.user_manager.retrieve_by_id(user.id)
            self.test_user.assertUserEquals(user1, user)
            self.user_manager.delete_user(user=user)

    def test_retrieved_by_email(self):
        for _ in range(0, 10):
            base_user = self.test_user.generate_random_user()
            self.user_manager.create_user(user=base_user)
            retrieved_user = self.user_manager.retrieve_by_email(email=base_user.email)
            self.test_user.assertUserEquals(base_user, retrieved_user)
            self.user_manager.delete_user(user=base_user)

    def test_update_language_filter(self):
        for _ in range(0, 10):
            base_user = self.test_user.generate_random_user()
            self.user_manager.create_user(user=base_user)

            # update language filter bool -> not bool = bool1
            has_language_filter = base_user.has_language_filter
            self.user_manager.update_language_filter_by_id(base_user.id)
            self.assertEqual(has_language_filter, not base_user.has_language_filter)
            
            # update language filter bool1 -> not bool1 = bool
            has_language_filter = base_user.has_language_filter
            self.user_manager.update_language_filter_by_id(base_user.id)
            self.assertEqual(has_language_filter, not base_user.has_language_filter)

            self.user_manager.delete_user(user=base_user)

    def test_update_ban_user(self):
        for _ in range(0, 10):
            base_user = self.test_user.generate_random_user()
            self.user_manager.create_user(user=base_user)

            # update ban bool -> not bool = bool1
            is_banned = base_user.is_banned
            self.user_manager.update_ban_user_by_id(id=base_user.id)
            self.assertEqual(is_banned, not base_user.is_banned)
            
            # update ban bool1 -> not bool1 = bool
            is_banned = base_user.is_banned
            self.user_manager.update_ban_user_by_id(id=base_user.id)
            self.assertEqual(is_banned, not base_user.is_banned)

            self.user_manager.delete_user(user=base_user)
            

    def test_actions(self):
        user = self.test_user.generate_random_user()
        self.user_manager.create_user(user=user)
        self.user_manager.unregister_user_by_id(user.id)
        user1 = self.user_manager.retrieve_by_id(user.id)
        self.assertEquals(user1.is_active, 0)


        user = self.test_user.generate_random_user()
        self.user_manager.create_user(user=user)
        self.user_manager.report_user_by_id(user.id)
        user1 = self.user_manager.retrieve_by_id(user.id)
        self.assertEquals(user1.is_reported, 1)

        self.user_manager.unreport_user_by_id(user.id)
        user2 = self.user_manager.retrieve_by_id(user.id)
        self.assertEqual(user2.is_reported, 0)
