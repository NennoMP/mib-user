from mib.dao.manager import Manager
from mib.models.user import User


class UserManager(Manager):

    @staticmethod
    def create_user(user: User):
        """Create a new user."""
        Manager.create(user=user)

    @staticmethod
    def retrieve_by_id(id_: int):
        """Retrieve a user by its id."""
        Manager.check_none(id=id_)
        return User.query.get(id_)
    
    @staticmethod
    def retrieve_users_list():
        """Retrieve the current users list."""
        return User.query.all()


    @staticmethod
    def retrieve_by_email(email: str):
        """Retrieve a user by its email"""
        Manager.check_none(email=email)
        return User.query.filter(User.email == email).first()

    @staticmethod
    def update_user(user: User):
        """Update fields of a specific user."""
        Manager.update(user=user)

    @staticmethod
    def unregister_user(user: User):
        """Unregister a specific user."""
        Manager.unregister(user=user)
        user.set_logout()
        Manager.save_auth()

    @staticmethod
    def unregister_user_by_id(id_: int):
        """Unregister a user by its id."""
        user = UserManager.retrieve_by_id(id_)
        UserManager.unregister_user(user)

    @staticmethod
    def update_language_filter(user: User):
        """Update language filter of a specific user."""
        Manager.update_language_filter(user=user)

    @staticmethod
    def update_language_filter_by_id(id_: int):
        """Update language filter of a user by its id."""
        user = UserManager.retrieve_by_id(id_)
        UserManager.update_language_filter(user)

    @staticmethod
    def report_user(user: User):
        """Report a specific user."""
        Manager.report(user=user)

    @staticmethod
    def report_user_by_id(id: int):
        """Report a user by its id."""
        user = UserManager.retrieve_by_id(id)
        UserManager.report_user(user)

    @staticmethod
    def unreport_user(user: User):
        """Unreport a specific user."""
        Manager.unreport(user=user)

    @staticmethod
    def unreport_user_by_id(id: int):
        """Unreport a user by its id."""
        user = UserManager.retrieve_by_id(id)
        UserManager.unreport_user(user)

    @staticmethod
    def update_ban_user(user: User):
        """(Un)Ban of a specific user."""
        Manager.update_ban(user=user)

    @staticmethod
    def update_ban_user_by_id(id: int):
        """(Un)Ban of a user by its id."""

        user = UserManager.retrieve_by_id(id)
        if user.is_banned:
            response_object = {
            'status': 'Success',
            'message': 'Successfully unbanned',
            }
        else:
            response_object = {
            'status': 'Success',
            'message': 'Successfully banned',
            }

        UserManager.update_ban_user(user)
        return response_object