from flask import jsonify

from mib.dao.user_manager import UserManager


def authenticate(auth):
    """
    Authentication resource for generic user.

    :param auth: a dict with email and password keys.
    :return: the response 200 if credentials are correct, else 401
    """

    user = UserManager.retrieve_by_email(auth['email'])
    response = {
        'authentication': 'failure',
        'message': 'Invalid credentials',
        'user': None
    }
    response_code = 401

    if user:
        if user.authenticate(auth['password']):
            if not user.is_active:
                response = {
                    'authentication': 'failure',
                    'message': 'Your account is no longer active!',
                    'user': None
                }
                response_code = 401
            elif user.is_banned:
                response = {
                    'authentication': 'failure',
                    'message': 'Your account has been banned!',
                    'user': None
                }
                response_code = 403
            else:
                response['authentication'] = 'success'
                response['message'] = 'Valid credentials'
                response['user'] = user.serialize()
                response_code = 200

    return jsonify(response), response_code


def logout(auth):
    """
    Logout resource for generic user.

    :param auth: a dict with email key.
    :return: the response 200 if logout is correct
    """

    user = UserManager.retrieve_by_email(auth['email'])
   
    if user is not None:
        response = {
            'authentication': 'success',
            'message': 'Successfully logout'
        }
        user.set_logout()
        UserManager.save_auth()
        return jsonify(response), 200
    else:
        response = {
            'authentication': 'failed',
            'message': 'Failed logout'
            
        }
        return jsonify(response), 404


    
