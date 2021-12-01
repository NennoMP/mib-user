import unittest


class ViewTest(unittest.TestCase):
    """
    This class should be implemented by
    all classes that tests resources
    """
    client = None

    @classmethod
    def setUpClass(cls):
        from mib import create_app
        app = create_app()
        cls.client = app.test_client()

        from tests.models.test_user import TestUser
        cls.test_user = TestUser

        from mib.dao.user_manager import UserManager
        cls.user_manager = UserManager  