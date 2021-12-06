from faker import Faker

from .view_test import ViewTest
from tests.models.test_user import TestUser


class TestAuth(ViewTest):

    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestAuth, cls).setUpClass()

    # Logout tests
    def test_logout(self):

        # Login with correct email
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

        # Logout
        response = self.client.post('/logout', json=data)
        json_response = response.json

        assert response.status_code == 200
        assert json_response["authentication"] == 'success'
        assert json_response["message"] == 'Successfully logout'

        data = {
            'email': 'fake@email'
        }

        response = self.client.post('/logout', json=data)
        json_response = response.json

        assert response.status_code == 404
        assert json_response["authentication"] == 'failed'
        assert json_response["message"] == 'Failed logout'

    # User tests
    def test_user(self):
        user = TestUser.generate_random_user()
        
        # Login with wrong email
        data = {
            'email': user.email,
            'password': TestAuth.faker.password()
        }
        response = self.client.post('/authenticate', json=data)
        json_response = response.json

        assert response.status_code == 401
        assert json_response["authentication"] == 'failure'
        assert json_response['user'] is None

        # Login with correct email
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

        # Login banned user
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

        # Login unregistered user
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

    # Admin tests
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

        # Ban unexistent user
        fake_id = 999
        url = '/users/{}/update_ban_user'.format(fake_id)
        body = {
            'user_id': admin.id
        }
        response = self.client.post(url, json=body)
        json_response = response.json

        assert response.status_code == 404
        assert json_response["status"] == 'User not present'

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
