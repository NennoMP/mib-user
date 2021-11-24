from flask import request, jsonify
from sqlalchemy.orm import joinedload
from mib.dao.user_manager import UserManager
from mib.models.user import User
import datetime

from werkzeug.security import check_password_hash



def create_user():
    """This method allows the creation of a new user.
    """
    post_data = request.get_json()
    email = post_data.get('email')
    password = post_data.get('password')

    searched_user = UserManager.retrieve_by_email(email)
    if searched_user is not None:
        return jsonify({
            'status': 'Already present'
        }), 200

    user = User()
    date_of_birth = datetime.datetime.strptime(post_data.get('date_of_birth'),
                                          '%Y-%m-%d')
    user.set_email(email)
    user.set_password(password)
    user.set_first_name(post_data.get('firstname'))
    user.set_last_name(post_data.get('lastname'))
    user.set_date_of_birth(date_of_birth)
    user.set_location(post_data.get('location'))
    UserManager.create_user(user)

    response_object = {
        'user': user.serialize(),
        'status': 'success',
        'message': 'Successfully registered',
    }

    return jsonify(response_object), 201


def get_user(user_id):
    """
    Get a user by its current id.

    :param user_id: user it
    :return: json response
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize()), 200


def get_profile(user_id):
    """
    Get the user profile by its current id.

    :param user_id: user id
    :return: json response
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize_profile()), 200

def update_language_filter(user_id):
    """
    Update the language filter of the user by its user_id

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
        UserManager.update_language_filter(user)
        response_object = {
            'status': 'success',
            'message': 'Successfully updated language filter',
        }
        return jsonify(response_object), 202

def get_user_by_email(user_email):
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

def unregister_user(user_id, body):
    """
    Unregister an user by its id if the password macthes

    :param user_id: user id
    :param password: password inserted in the unregister form
    :return: json response
    """

    user_id = body['id']
    _user = UserManager.retrieve_by_id(user_id)

    if _user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

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


def delete_user(user_id):
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
