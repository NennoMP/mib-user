from flask import jsonify

from mib.dao.user_manager import UserManager


def authenticate(auth):
    """
    Authentication resource for generic user.

    :param auth: a dict with <email> and <password> keys.
    :return: 
        - 200: credentials correct
        - 401: invalid credentials OR inactive account
        - 403: banned account
    """

    response = {
        'authentication': 'failure',
        'message': 'Invalid credentials',
        'user': None
    }
    response_code = 401

    user = UserManager.retrieve_by_email(auth['email'])
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
                UserManager.save_auth()
                response['authentication'] = 'success'
                response['message'] = 'Valid credentials'
                response['user'] = user.serialize()
                response_code = 200

    return jsonify(response), response_code


def logout(auth):
    """
    Logout resource for generic user.

    :param auth: a dict with email key.
    :return:
        - 200: successfully logout
        - 404: failed logout
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
