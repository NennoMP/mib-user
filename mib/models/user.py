from werkzeug.security import generate_password_hash, check_password_hash

from mib import db
from ..utils import image_to_base64


class User(db.Model):
    """Representation of User model."""

    # The name of the table that we explicitly set
    __tablename__ = 'User'

    # A list of (user) fields to be serialized
    SERIALIZE_LIST = [
                    'id', 'email', 'is_active', 'is_admin', 'is_reported', 'is_banned', 'authenticated', 'is_anonymous'
                ]

    # A list of (user) fields to be serialized for the profile
    SERIALIZE_PROFILE_LIST = [
                            'id', 'email', 'first_name',
                            'last_name', 'location', 'is_active',
                            'is_admin', 'is_reported', 'is_banned', 'authenticated', 'is_anonymous', 'bonus',
                            'has_language_filter', 'profile_pic'
                        ]

    # Data
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False, unique=True)
    first_name = db.Column(db.Unicode(128), nullable=False, unique=False)
    last_name = db.Column(db.Unicode(128), nullable=False, unique=False)
    password = db.Column(db.Unicode(128))
    date_of_birth = db.Column(db.Date())
    location = db.Column(db.Unicode(128), nullable=False)
    profile_pic = db.Column(db.String)          # profile picture path
    bonus = db.Column(db.Integer, default=0)    # lottery bonus points

    # Booleans
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_reported = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.Boolean, default=False)
    is_anonymous = False
    authenticated = db.Column(db.Boolean, default=True)
    has_language_filter = db.Column(db.Boolean, default=False)


    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self.authenticated = False

    # Set user <email>
    def set_email(self, email: str):
        self.email = email

    # Set user <first_name>
    def set_first_name(self, name: str):
        self.first_name = name

    # Set user <last_name>
    def set_last_name(self, name: str):
        self.last_name = name

    # Set user <password>
    def set_password(self, password: str):
        self.password = generate_password_hash(password)

    # Set user <date_of_birth>
    def set_date_of_birth(self, date_of_birth):
        self.date_of_birth = date_of_birth

    # Set user <location>
    def set_location(self, location: str):
        self.location = location

    # Set user <profile_pic>
    def set_profile_pic(self, profile_pic: str):
        self.profile_pic = profile_pic

    # Set user <bonus>
    def set_lottery_bonus(self, bonus):
        self.bonus += bonus

    # Set user <is_active>
    def set_active(self, bool: bool):
        self.is_active = bool

    # Set user <is_admin>
    def set_admin(self, bool: bool):
        self.is_admin = bool

    # Set user <is_reported>
    def set_reported(self, bool: bool):
        self.is_reported = bool
    
    # Set user <is_banned>
    def update_banned(self):
        self.is_banned = not self.is_banned

    # Authenticate the user
    def authenticate(self, password: str):
        checked = check_password_hash(self.password, password)
        self.authenticated = checked
        
        return self.authenticated

    # Set user <authenticated> to False
    def set_logout(self):
        self.authenticated = False

    # Update user <has_language_filter>
    def update_language_filter(self):
        self.has_language_filter = not self.has_language_filter

    # Get user <authenticated>
    def is_authenticated(self):
        return self.authenticated

    # Serialize api-gateway user model information
    def serialize(self):
        return dict([(k, self.__getattribute__(k)) for k in self.SERIALIZE_LIST])

    # Serialize profile information to display
    def serialize_profile(self):    
        dict = {}
        for k in self.SERIALIZE_PROFILE_LIST:
            dict[k] = self.__getattribute__(k)
        dict['profile_pic'] = image_to_base64(dict['profile_pic'])

        return dict
