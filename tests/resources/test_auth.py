import re
from .view_test import ViewTest
from faker import Faker
#from tests.models.test_user import TestUser


TEST_PATH_FILE      = 'mib/static/images/test.png'
TEST_BINARY_FILE    = 'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='


class TestAuth(ViewTest):
    """
        Simulate the user login for testing the resources
        :return: user
    """

    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestAuth, cls).setUpClass()

    @classmethod
    def create_and_login(cls):
        user = cls.test_user.generate_random_user()
        cls.user_manager.create_user(user=user)

        pw = user.password
        data = {
            'email': user.email,
            'password': pw
        }
        cls.client.post('/authenticate', json=data)

        return user


    def create_user(self):
        user = self.test_user.generate_random_user()

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

    def test_user(self):
        user = self.test_user.generate_random_user()

        # Login with non-existent credentials
        data = {
            'email': user.email,
            'password': TestAuth.faker.password()
        }

        response = self.client.post('/authenticate', json=data)
        json_response = response.json

        assert response.status_code == 401
        assert json_response["authentication"] == 'failure'
        assert json_response["message"] == 'Invalid credentials'
        assert json_response['user'] is None

        # Login with correct credentials
        user = self.test_user.generate_random_user()
        pw = user.password
        user.set_password(pw)
        self.user_manager.create_user(user=user)

        data = {
            'email': user.email,
            'password': pw
        }

        response = self.client.post('/authenticate', json=data)
        json_response = response.json

        assert response.status_code == 200
        assert json_response["authentication"] == 'success'
        assert json_response["message"] == 'Valid credentials'
        assert json_response['user'] is not None

        # Login banned account
        user = self.test_user.generate_random_user()
        pw = user.password
        user.set_password(pw)
        self.user_manager.create_user(user=user)
        user.update_banned()

        data = {
            'email': user.email,
            'password': pw
        }

        response = self.client.post('/authenticate', json=data)
        json_response = response.json

        assert response.status_code == 403
        assert json_response["authentication"] == 'failure'
        assert json_response["message"] == 'Your account has been banned!'
        assert json_response['user'] is None

        # Ban an user: unauthorized
        target_user = self.test_user.generate_random_user()
        self.user_manager.create_user(user=target_user)

        url = '/users/{}/update_ban_user'.format(target_user.email)
        body = {
            'src_user_id': user.id
        }
        response = self.client.post(url, json=body)
        json_response = response.json

        assert response.status_code == 401
        assert json_response["status"] == 'Failed'
        assert json_response["message"] == 'Unauthorized action'

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

        # Update profile picture: user not found
        url = '/profile/{}/profile_picture'.format(fake_id)
        body = {
            'format': '.jpg',
            'file': TEST_BINARY_FILE,
        }
        response = self.client.post(url, json=body)
        json_response = response.json

        assert response.status_code == 404
        assert json_response["status"] == 'failed'
        assert json_response["message"] == 'Could not update the profile picture, user not found'


        user = self.create_and_login()
        user.set_profile_pic(TEST_PATH_FILE)

        """
        # GET profile: user found
        url = '/profile/{}'.format(user.id)
        response = self.client.get(url)
        print(response.status_code)"""

        
        # Update language filter
        url = '/profile/{}/language_filter'.format(user.id)
        response = self.client.post(url)
        json_response = response.json

        assert response.status_code == 202
        assert json_response["status"] == 'success'
        assert json_response["message"] == 'Successfully updated language filter'

        
        """# Update profile picture
        url = '/profile/{}/profile_picture'.format(user.id)
        body = {
            'format': 'png',
            'file': TEST_BINARY_FILE
        }
        print("PIC: ", user.profile_pic)
        print("EMAIL: ", user.email)
        print("NAME: ", user.first_name)
        user.set_email('ahah')
        user.set_first_name("SOP")
        print("PIC: ", user.profile_pic)
        print("EMAIL: ", user.email)
        print("NAME: ", user.first_name)
        response = self.client.post(url, json=body)
        json_response = response.json

        assert response.status_code == 202
        assert json_response["status"] == 'success'
        assert json_response["message"] == 'Profile picture updated'"""

    def test_admin(self):
        admin = self.test_user.generate_random_user()
        
        # Login admin with a correct email
        admin = self.test_user.generate_random_user()
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
        target_user = self.test_user.generate_random_user()
        self.user_manager.create_user(user=target_user)

        url = '/users/{}/update_ban_user'.format(target_user.email)
        body = {
            'src_user_id': admin.id
        }
        response = self.client.post(url, json=body)
        json_response = response.json

        assert response.status_code == 202
        assert json_response["status"] == 'Success'
        assert json_response["message"] == 'Successfully banned'

        # Unban an user
        target_user = self.test_user.generate_random_user()
        self.user_manager.create_user(user=target_user)

        url = '/users/{}/update_ban_user'.format(target_user.email)
        body = {
            'src_user_id': admin.id
        }
        response = self.client.post(url, json=body)
        json_response = response.json

        assert response.status_code == 202
        assert json_response["status"] == 'Success'
        assert json_response["message"] == 'Successfully unbanned'


    '''
    def test_delete_user(self):
        user = self.login_test_user()
        rv = self.client.delete('/user/%d' % user.id)
        assert rv.status_code == 202

    def test_get_user_by_id(self):
        # get a non-existent user
        rv = self.client.get('/user/0')
        assert rv.status_code == 404
        # get an existent user
        user = self.login_test_user()
        rv = self.client.get('/user/%d' % user.id)
        assert rv.status_code == 200

    def test_get_user_by_email(self):
        # get a non-existent user with faked email
        rv = self.client.get('/user_email/%s' % TestUsers.faker.email())
        assert rv.status_code == 404
        # get an existent user
        user = self.login_test_user()
        rv = self.client.get('/user_email/%s' % user.email)
        assert rv.status_code == 200
'''
