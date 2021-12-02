import re
from .view_test import ViewTest
from faker import Faker
from tests.models.test_user import TestUser


TEST_PATH_FILE = 'mib/static/images/test.png'
TEST_BINARY_FILE = 'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='


class TestUsers(ViewTest):
    """
        Simulate the user login for testing the resources
        :return: user
    """

    faker = Faker('it_IT')


    @classmethod
    def create_and_login(cls):
        user = TestUser.generate_random_user()
        cls.user_manager.create_user(user=user)

        """pw = user.password
            data = {
                'email': user.email,
                'password': pw
            }
            cls.client.post('/authenticate', json=data)"""

        return user

    
    def test_create_user(self):
        user = TestUser.generate_random_user()

        body = {
            'email': user.email,
            'password': user.password,
            'firstname': user.first_name,
            'lastname': user.last_name,
            'date_of_birth': user.date_of_birth,
            'location': user.location
        }
        response = self.client.post('/user', json=body)
        json_response = response.json

        assert response.status_code == 201
        assert json_response["status"] == 'success'
        assert json_response["message"] == 'Successfully registered'


    def test_profile(self):

        fake_id = 999
        # GET profile: user not found
        url = '/profile/{}'.format(fake_id)
        response = self.client.get(url)
        json_response = response.json

        assert response.status_code == 404
        assert json_response['status'] == 'User not present'

        # Update language filter: user not found
        url = '/profile/{}/language_filter'.format(fake_id)
        response = self.client.post(url)
        json_response = response.json

        assert response.status_code == 404
        assert json_response["status"] == 'failed'
        assert json_response["message"] == 'Could not update language filter, user not found'

        user = self.create_and_login()
        user.set_profile_pic(TEST_PATH_FILE)

        """# GET profile: user found
            url = '/profile/{}'.format(user.id)
            response = self.client.get(url)
            print(response)"""

        """assert response.status_code == 200
            assert json_response["status"] == 'success'"""

        # Update language filter
        url = '/profile/{}/language_filter'.format(user.id)
        response = self.client.post(url)
        json_response = response.json

        assert response.status_code == 202
        assert json_response["status"] == 'success'
        assert json_response["message"] == 'Successfully updated language filter'
