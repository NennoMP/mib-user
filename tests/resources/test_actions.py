from .view_test import ViewTest
from faker import Faker
from tests.models.test_user import TestUser


class TestActions(ViewTest):
    """
        Simulate the user login for testing the resources
        :return: user
    """

    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestActions, cls).setUpClass()

    def test_report(self):

        # Create a user to report
        user = self.test_user.generate_random_user()
       
        self.user_manager.create_user(user=user)
        
        # Report a not existing user
        url = "/users/%s/report_user" % (self.test_user.faker.email())
        response = self.client.post(url)
        assert response.status_code == 404

        # Report an existing user
        url = "/users/%s/report_user" % (user.email)
        response = self.client.post(url)
        assert response.status_code == 202

        # Create admin to reject user
        admin = self.test_user.generate_random_user()
        admin.set_password(admin.password)
        admin.is_admin= True
        self.user_manager.create_user(user=admin)

        # Failing attempt to reject a user.
        # Only admin is authorized.
        data = {
            'src_user_id': user.id,
        }

        url = "/users/%s/unreport_user" % (user.email)
        response = self.client.post(url, json=data)
        assert response.status_code == 401
        
        # Reject an existing user
        url = "/users/%s/unreport_user" % (self.test_user.faker.email())
        response = self.client.post(url, json=data)
        assert response.status_code == 404
        
        # Successfully reject user by admin
        data = {
            'src_user_id': admin.id,
        }
    
        url = "/users/%s/unreport_user" % (user.email)
        response = self.client.post(url, json=data)
        assert response.status_code == 202
