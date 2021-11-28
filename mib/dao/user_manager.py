from mib.dao.manager import Manager
from mib.models.user import User


class UserManager(Manager):

    @staticmethod
    def create_user(user: User):
        Manager.create(user=user)

    @staticmethod
    def retrieve_by_id(id_: int):
        Manager.check_none(id=id_)
        return User.query.get(id_)
    
    @staticmethod
    def retrieve_users_list():
        return User.query.all()


    @staticmethod
    def retrieve_by_email(email: str):
        Manager.check_none(email=email)
        return User.query.filter(User.email == email).first()

    @staticmethod
    def update_user(user: User):
        Manager.update(user=user)

    @staticmethod
    def unregister_user(user: User):
        Manager.unregister(user=user)

    @staticmethod
    def unregister_user_by_id(id_: int):
        user = UserManager.retrieve_by_id(id_)
        UserManager.unregister_user(user)

    @staticmethod
    def report_user(user: User):
        Manager.report(user=user)

    @staticmethod
    def report_user_by_email(email: str):
        user = UserManager.retrieve_by_email(email)
        UserManager.report_user(user)

    @staticmethod
    def unreport_user(user: User):
        Manager.unreport(user=user)

    @staticmethod
    def unreport_user_by_email(email: str):
        user = UserManager.retrieve_by_email(email)
        UserManager.unreport_user(user)

    """@staticmethod
    def update_block_user(user: User):
        Manager.update_block(user=user)

    @staticmethod
    def update_block_user_by_id(id_: int):
        user = UserManager.retrieve_by_id(id_)
        UserManager.update_block_user(user)
    """

    @staticmethod
    def update_ban_user(user: User):
        Manager.update_ban(user=user)

    @staticmethod
    def update_ban_user_by_email(email: str):
        user = UserManager.retrieve_by_email(email)

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
    
    @staticmethod
    def delete_user(user: User):
        Manager.delete(user=user)

    @staticmethod
    def delete_user_by_id(id_: int):
        user = UserManager.retrieve_by_id(id_)
        UserManager.delete_user(user)
