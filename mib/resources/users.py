import datetime

from flask import request, jsonify
from werkzeug.security import check_password_hash

from mib.dao.user_manager import UserManager
from mib.models.user import User
from ..utils import save_image, allowed_email


def create_user():
    """This method allows the creation of a new user."""

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
    date_of_birth = datetime.datetime.strptime(post_data.get('date_of_birth'),
                                          '%Y-%m-%d')
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


def update_profile(user_id: int, body):
    """This method allows the update of a user profile by its current id."""
    
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        return jsonify({
            'status': 'Not found'
        }), 404

    if not allowed_email(body['email']):
        return jsonify({
            'status': 'not success',
            'message': 'Incorrect email format'
        }), 409

    
    if user.email != body['email']:
        exist_user = UserManager.retrieve_by_email(body['email'])
        if exist_user is not None:
            return jsonify({
                'status': 'not success',
                'message': 'Email already exists'
            }), 409

    user.set_email(body['email'])
    user.set_first_name(body['firstname'])
    user.set_last_name(body['lastname'])
    user.set_location(body['location'])
    UserManager.update_user(user)

    response_object = {
        'user': user.serialize(),
        'status': 'success',
        'message': 'Successfully updated',
    }
    
    return jsonify(response_object), 200


def get_user(user_id: int):
    """
    Get a user by its current id.

    :param user_id: user id
    :return: json response
    """

    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize()), 200


def get_profile(user_id: int):
    """
    Get the user profile by its current id.

    :param user_id: user id
    :return: json response
    """

    user = UserManager.retrieve_by_id(user_id)
    print(user)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize_profile()), 200


def get_users_list():
    _users = UserManager.retrieve_users_list()
    users_list = [user.serialize_profile() for user in _users]
    response_object = {
        'users_list': users_list,
        'status': 'success'
    }
    return jsonify(response_object), 200


def report_user(user_email: str):
    """
    Report an user by its current email.

    :param user_id: id of target user
    :return: json response
    """

    _user = UserManager.retrieve_by_email(user_email)
    if _user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404
    else:
        if not _user.is_reported:
            UserManager.report_user_by_email(user_email)
        response_object = {
            'status': 'Success',
            'message': 'Successfully reported'
        }
        return jsonify(response_object), 202


def unreport_user(dest_user_email: str, body):
    """
    Unreport an user by its current email.

    :param user_email: email of target user
    :return: json response
    """

    src_user_id = body['src_user_id']

    dest_user = UserManager.retrieve_by_email(dest_user_email)
    src_user = UserManager.retrieve_by_id(src_user_id)
    if dest_user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404
    else:
        if src_user.is_admin:
            UserManager.unreport_user_by_email(dest_user_email)
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




def update_block_user(dest_user_id: int, body):
    """
    (Un)Block an user by its current id.

    :param dest_user_id: id of target user
    :return: json response
    """
    # TODO: need blocklist table and microservice
    pass


def update_ban_user(dest_user_email: str, body):
    """
    (Un)Ban an user by its current email.

    :param user_email: email of the target user
    :return: json response
    """

    src_user_id = body['src_user_id']

    dest_user = UserManager.retrieve_by_email(dest_user_email)
    src_user = UserManager.retrieve_by_id(src_user_id)
    if dest_user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404
    else:
        if src_user.is_admin:
            response_object = UserManager.update_ban_user_by_email(dest_user_email)
            return jsonify(response_object), 202
        else:
            response_object = {
            'status': 'Failed',
            'message': 'Unauthorized action'
            }
            return jsonify(response_object), 401
            


def update_profile_picture(user_id: int, body):
    """
    Update the profile picture of the user by its current id.

    :param user_id: user id
    :param body: dict that contains the file uploaded
    :return: json response
    """

    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response_object = {
            'status': 'failed',
            'message': 'Could not update the profile picture, user not found',
        }
        return jsonify(response_object), 404
    else:
        print("PIC: ", user.profile_pic)
        print("EMAIL: ", user.email)
        print("NAME: ", user.first_name)
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
    :return: json response
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


def get_user_by_email(user_email: str):
    """
    Get a user by its current email.

    :param user_email: user email
    :return: json response
    """

    user = UserManager.retrieve_by_email(user_email)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize()), 200

def unregister_user(user_id: int, body):
    """
    Unregister an user by its current id if the password macthes.

    :param user_id: user id
    :param body: dictionary that contains the password inserted in the unregister form
    :return: json response
    """

    user_id = body['id']
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


def delete_user(user_id: int):
    """
    Delete the user with id = user_id.

    :param user_id the id of user to be deleted
    :return json response
    """
    UserManager.delete_user_by_id(user_id)
    response_object = {
        'status': 'success',
        'message': 'Successfully deleted',
    }

    return jsonify(response_object), 202
