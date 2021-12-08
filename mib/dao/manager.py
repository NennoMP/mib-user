from mib import db


class Manager(object):
    db_session = db.session

    @staticmethod
    def check_none(**kwargs):
        """Check if given parameters are none, before setting them."""

        for name, arg in zip(kwargs.keys(), kwargs.values()):
            if arg is None:
                raise ValueError(f'You can\'t set {name} argument to None')

    @staticmethod
    def create(**kwargs):
        """Create a new entry, in the database."""

        Manager.check_none(**kwargs)
        for bean in kwargs.values():
            db.session.add(bean)
            bean.authenticated = True
            if bean.email == 'admin@example.com':
                bean.is_admin = True
        db.session.commit()

    @staticmethod
    def update(**kwargs):
        """Commit changes to the database."""

        Manager.check_none(**kwargs)
        db.session.commit()
    
    @staticmethod
    def save_auth(**kwargs):
        db.session.commit()

    @staticmethod
    def update_language_filter(**kwargs):
        """Update <has_language_filter> field of an user, in the database."""

        Manager.check_none(**kwargs)
        for bean in kwargs.values():
            bean.has_language_filter = not bean.has_language_filter
        db.session.commit()

    @staticmethod
    def unregister(**kwargs):
        """
        Logical delete of an user, set <is_active> field of an user to False, in the database.
        """

        Manager.check_none(**kwargs)
        for bean in kwargs.values():
            bean.set_active(False)
        db.session.commit()

    @staticmethod
    def report(**kwargs):
        """Set <is_reported> field of an user to True, in the database."""

        Manager.check_none(**kwargs)
        for bean in kwargs.values():
            bean.set_reported(True)
        db.session.commit()
        
    @staticmethod
    def unreport(**kwargs):
        """Set <is_reported> field of an user to False, in the database."""

        Manager.check_none(**kwargs)
        for bean in kwargs.values():
            bean.set_reported(False)
        db.session.commit()

    @staticmethod
    def update_ban(**kwargs):
        """Update <is_banned> field of an user, in the database."""

        Manager.check_none(**kwargs)
        for bean in kwargs.values():
            bean.update_banned()
            if bean.is_banned:
                bean.set_reported(False)
        db.session.commit()
