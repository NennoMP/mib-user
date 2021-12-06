import datetime

from flask import request, jsonify
from werkzeug.security import check_password_hash

from mib.dao.user_manager import UserManager
from mib.models.user import User
from ..utils import save_image, allowed_email


def create_user():
    """
    This method allows the creation of a new user.
    
    :return: json response and status code
        - 201: successfully created
        - 403: chosen email already exists
    """

    post_data = request.get_json()
    email = post_data.get('email')
    password = post_data.get('password')

    searched_user = UserManager.retrieve_by_email(email)
    if searched_user is not None:
        return jsonify({
            'status': 'Already present',
            'message': 'User already exists'
        }), 403

    user = User()
    date_of_birth = datetime.datetime.strptime(
                                        post_data.get('date_of_birth'),'%Y-%m-%d'
                                    )
    user.set_email(email)
    user.set_password(password)
    user.set_first_name(post_data.get('firstname'))
    user.set_last_name(post_data.get('lastname'))
    user.set_date_of_birth(date_of_birth)
    user.set_location(post_data.get('location'))
    user.set_profile_pic('mib/static/images/default.jpg')
    UserManager.create_user(user)

    response_object = {
        'user': user.serialize(),
        'status': 'success',
        'message': 'Successfully registered',
    }

    return jsonify(response_object), 201


def get_user(user_id: int):
    """
    Get a user by its current id.

    :param user_id: user id
    :return: json response and status code
        - 200: retrieved user
        - 404: user not found
    """

    _user = UserManager.retrieve_by_id(user_id)
    if _user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(_user.serialize()), 200


def get_bonus(user_id: int):
    """
    Get bonus of user by its id.

    :param user_id: user id
    :return: json response and status code
        - 200: bonus retrieved
        - 404: user not found
    """

    _user = UserManager.retrieve_by_id(user_id)
    if _user is None:
        response = {
            'status': 'failed',
            'message': 'User not present',
            'bonus': -1
        }
        return jsonify(response), 404

    response = {
        'status': 'success',
        'message': 'Bonus retrieved',
        'bonus': _user.bonus
    }
    return jsonify(response), 200


def set_bonus(user_id: int, body):
    """
    Set bonus of user by its id.

    :param user_id: user id
    :return: json response and status code
        - 200: bonus updated
        - 404: user not found
        - 409: invalid bonus
    """

    _user = UserManager.retrieve_by_id(user_id)
    if _user is None:
        response = {
            'status': 'failed',
            'message': 'User not present',
            'bonus': -1
        }
        return jsonify(response), 404
        
    if body['bonus'] < 0:
        response = {
            'status': 'failed',
            'message': 'Negative bonus',
            'bonus': -1
        }
        return jsonify(response), 409


    _user.bonus = body['bonus']
    UserManager.update_user(_user)
    response = {
        'status': 'success',
        'message': 'Bonus updated',
        'bonus': _user.bonus
    }
    return jsonify(response), 200



def get_user_by_email(user_email: str):
    """
    Get a user by its current email.

    :param user_email: user email
    :return: json response and status code
        - 200: user found
        - 404: user not found
    """

    user = UserManager.retrieve_by_email(user_email)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize()), 200


def get_users_list():
    """
    Get the users list

    :return: json response and status code
        - 200: retrieved users list
    """

    _users = UserManager.retrieve_users_list()

    users_list = [user.serialize_profile() for user in _users if user.is_active]
    response_object = {
        'users_list': users_list,
        'status': 'success'
    }
    return jsonify(response_object), 200


def get_profile(user_id: int):
    """
    Get the user profile by its current id.

    :param user_id: user id
    :return: json response and status code
        - 200: retrieved profile information
        - 404: user not found
    """

    _user = UserManager.retrieve_by_id(user_id)
    if _user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(_user.serialize_profile()), 200


def update_profile(user_id: int, body):
    """
    This method allows the update of a user profile by its current id.
    
    :param user_id: user id
    :param body: dict with email, firstname, lastname and location keys
    :return: json response and status code
        - 200: successfully updated
        - 409: incorrect email format OR email already exists
    """
    
    _user = UserManager.retrieve_by_id(user_id)
    if _user is None:
        return jsonify({
            'status': 'Not found'
        }), 404

    if not allowed_email(body['email']):
        return jsonify({
            'status': 'not success',
            'message': 'Incorrect email format'
        }), 409
    
    if _user.email != body['email']:
        exist_user = UserManager.retrieve_by_email(body['email'])
        if exist_user is not None:
            return jsonify({
                'status': 'not success',
                'message': 'Email already exists'
            }), 409

    _user.set_email(body['email'])
    _user.set_first_name(body['firstname'])
    _user.set_last_name(body['lastname'])
    _user.set_location(body['location'])
    UserManager.update_user(_user)

    response_object = {
        'user': _user.serialize(),
        'status': 'success',
        'message': 'Successfully updated',
    }
    
    return jsonify(response_object), 200


def update_profile_picture(user_id: int, body):
    """
    Update the profile picture of the user by its current id.

    :param user_id: user id
    :param body: dict with <format> and <file> keys, the format and the binary of the file
    :return: json response and status code
        - 202: successfully updated
        - 404: user not gound
    """

    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response_object = {
            'status': 'failed',
            'message': 'Could not update the profile picture, user not found',
        }
        return jsonify(response_object), 404
    else:
        user.set_profile_pic(save_image(user_id, body['file']))
        UserManager.update_user(user)
        response_object = {
            'status': 'success',
            'message': 'Profile picture updated',
        }
        return jsonify(response_object), 202


def update_language_filter(user_id: int):
    """
    Update the language filter of the user by its current id.

    :param user_id: user id
    :return: json response and status code
        - 202: successfully updated
        - 404: user not gound
    """

    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response_object = {
            'status': 'failed',
            'message': 'Could not update language filter, user not found',
        }
        return jsonify(response_object), 404
    else:
        UserManager.update_language_filter_by_id(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully updated language filter',
        }
        return jsonify(response_object), 202


def report_user(target_id: int):
    """
    Report an user by its current email.

    :param user_id: id of target user
    :return: json response and status code
        - 202: successfully reported
        - 404: user not found
    """

    _user = UserManager.retrieve_by_id(target_id)
    if _user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404
    else:
        if not _user.is_reported:
            UserManager.report_user_by_id(target_id)
        response_object = {
            'status': 'Success',
            'message': 'Successfully reported'
        }
        return jsonify(response_object), 202

def unreport_user(target_id: int, body):
    """
    Unreport an user by its current email.

    :param user_email: email of target user
    :param body: dict with <user_id> key, id of the user reporting
    :return: json response and statys code
        - 202: successfully unreported
        - 401: unauthorized
        - 404: user not found
    """

    user_id = body['user_id']

    _user = UserManager.retrieve_by_id(user_id)
    target_user = UserManager.retrieve_by_id(target_id)
    if target_user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404
    else:
        if _user.is_admin:
            UserManager.unreport_user_by_id(target_id)
            response_object = {
                'status': 'Success',
                'message': 'Successfully unreported'
            }
            return jsonify(response_object), 202
        else:
            response_object = {
                'status': 'Failed',
                'message': 'Unauthorized action'
            }
            return jsonify(response_object), 401


def update_ban_user(target_id: int, body):
    """
    (Un)Ban an user by its current email.

    :param user_email: email of the target user
    :param body: dict with <user_email>, the email of the admin banning
    :return: json response and status code
        - 202: successfully updated ban status
        - 401: unauthorized
        - 404: user not found
    """

    user_id = body['user_id']

    _user = UserManager.retrieve_by_id(user_id)
    target_user = UserManager.retrieve_by_id(target_id)
    if target_user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404
    else:
        if _user.is_admin:
            response_object = UserManager.update_ban_user_by_id(target_id)
            return jsonify(response_object), 202
        else:
            response_object = {
            'status': 'Failed',
            'message': 'Unauthorized action'
            }
            return jsonify(response_object), 401


def unregister_user(user_id: int, body):
    """
    Unregister an user by its current id if the inserted password matches.

    :param user_id: user id
    :param body: dict with the <password> key
    :return: json response and statys code
        - 202: successfully unregistered
        - 401: incorrect password
        - 404: user not found
    """

    _user = UserManager.retrieve_by_id(user_id)
    if _user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404
    else:
        if check_password_hash(_user.password, body['password']):
            UserManager.unregister_user_by_id(user_id)
            response_object = {
                'status': 'success',
                'message': 'Successfully unregistered',
            }
            return jsonify(response_object), 202
        else:
            response_object = {
                'status': 'failed',
                'message': 'Could not unregister, inserted password does not match',
            }
            return jsonify(response_object), 401
