import re
from .view_test import ViewTest
from faker import Faker
from tests.models.test_user import TestUser



class TestAuth(ViewTest):
    """
        Simulate the user login for testing the resources
        :return: user
    """

    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestAuth, cls).setUpClass()

    
    def test_logout(self):
        # login with a correct email
        user = TestUser.generate_random_user()
        psw = user.password
        user.set_password(user.password)

        self.user_manager.create_user(user=user)
        data = {
            'email': user.email,
            'password': psw,
        }

        self.client.post('/authenticate', json=data)
        data = {
            'email': user.email
        }

        response = self.client.post('/logout', json=data)
        assert response.status_code == 200
        json_response = response.json
        assert json_response["authentication"] == 'success'
        assert json_response["message"] == 'Successfully logout'

        data = {
            'email': 'fake@email'
        }

        response = self.client.post('/logout', json=data)
        assert response.status_code == 404
        json_response = response.json
        assert json_response["authentication"] == 'failed'
        assert json_response["message"] == 'Failed logout'


    



    def test_login(self):
        # login for a customer
        user = TestUser.generate_random_user()
        
        # login with a wrong email
        data = {
            'email': user.email,
            'password': TestAuth.faker.password()
        }

        response = self.client.post('/authenticate', json=data)
        json_response = response.json

        assert response.status_code == 401
        assert json_response["authentication"] == 'failure'
        assert json_response['user'] is None

        # login with a correct email
        user = TestUser.generate_random_user()
        psw = user.password
        user.set_password(user.password)

        self.user_manager.create_user(user=user)
        data = {
            'email': user.email,
            'password': psw,
        }

        response = self.client.post('/authenticate', json=data)
        json_response = response.json

        assert response.status_code == 200
        assert json_response["authentication"] == 'success'
        assert json_response['user'] is not None

        # login banned user
        user = TestUser.generate_random_user()
        psw = user.password
        user.set_password(user.password)
        user.is_banned = True
        self.user_manager.create_user(user=user)
        data = {
            'email': user.email,
            'password': psw
        }

        response = self.client.post('/authenticate', json=data)
        json_response = response.json

        assert response.status_code == 403
        assert json_response["authentication"] == 'failure'
        assert json_response["message"] == 'Your account has been banned!'
        assert json_response['user'] is None

        # Ban an user: unauthorized
        target_user = TestUser.generate_random_user()
        self.user_manager.create_user(user=target_user)

        url = '/users/{}/update_ban_user'.format(target_user.id)
        body = {
            'user_id': user.id
        }
        response = self.client.post(url, json=body)
        json_response = response.json

        assert response.status_code == 401
        assert json_response["status"] == 'Failed'
        assert json_response["message"] == 'Unauthorized action'

        # login unregistered user
        user = TestUser.generate_random_user()
        psw = user.password
        user.set_password(user.password)
        user.is_active = False
        self.user_manager.create_user(user=user)
        data = {
            'email': user.email,
            'password': psw
        }

        response = self.client.post('/authenticate', json=data)
        json_response = response.json

        assert response.status_code == 401
        assert json_response["authentication"] == 'failure'
        assert json_response["message"] == 'Your account is no longer active!'
        assert json_response['user'] is None


    def test_admin(self):
        admin = TestUser.generate_random_user()

        # Login admin with a correct email
        admin = TestUser.generate_random_user()
        admin.set_email('admin@test.com')
        pw = 'Admin1@'
        admin.set_password(pw)
        admin.set_admin(True)
        self.user_manager.create_user(user=admin)

        data = {
            'email': admin.email,
            'password': pw
        }

        response = self.client.post('/authenticate', json=data)
        json_response = response.json

        assert response.status_code == 200
        assert json_response["authentication"] == 'success'
        assert json_response["message"] == 'Valid credentials'
        assert json_response['user'] is not None

        # Ban an user
        target_user = TestUser.generate_random_user()
        self.user_manager.create_user(user=target_user)

        url = '/users/{}/update_ban_user'.format(target_user.id)
        body = {
            'user_id': admin.id
        }
        response = self.client.post(url, json=body)
        json_response = response.json

        assert response.status_code == 202
        assert json_response["status"] == 'Success'
        assert json_response["message"] == 'Successfully banned'

        # Unban an user
        url = '/users/{}/update_ban_user'.format(target_user.id)
        body = {
            'user_id': admin.id
        }
        response = self.client.post(url, json=body)
        json_response = response.json

        assert response.status_code == 202
        assert json_response["status"] == 'Success'
        assert json_response["message"] == 'Successfully unbanned'
