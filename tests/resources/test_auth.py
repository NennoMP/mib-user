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
        user = self.test_user.generate_random_user()
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
        user = self.test_user.generate_random_user()
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
        assert json_response['user'] is None

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






    
    


