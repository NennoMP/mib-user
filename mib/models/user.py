from werkzeug.security import generate_password_hash, check_password_hash

from mib import db


class User(db.Model):
    """Representation of User model."""

    # The name of the table that we explicitly set
    __tablename__ = 'User'

    # A list of fields to be serialized
    SERIALIZE_LIST = ['id', 'email', 'is_active', 'authenticated', 'is_anonymous']

    # A list of fields to be serialized
    SERIALIZE_PROFILE_LIST = ['id', 'email', 'first_name',
                              'last_name', 'location', 'is_active', 
                              'authenticated', 'is_anonymous', 'bonus',
                              'has_language_filter'
                             ]


    # All fields of user
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False, unique=True)
    first_name = db.Column(db.Unicode(128), nullable=False, unique=False)
    last_name = db.Column(db.Unicode(128), nullable=False, unique=False)
    password = db.Column(db.Unicode(128))
    date_of_birth = db.Column(db.Date())
    location = db.Column(db.Unicode(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    authenticated = db.Column(db.Boolean, default=True)
    is_anonymous = False
    has_language_filter = db.Column(db.Boolean, default=False)
    bonus = db.Column(db.Integer, default=0)

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self.authenticated = False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def set_email(self, email):
        self.email = email

    def set_first_name(self, name):
        self.first_name = name

    def set_last_name(self, name):
        self.last_name = name

    def is_authenticated(self):
        return self.authenticated

    def set_active(self, bool):
        self.is_active = bool

    def update_language_filter(self):
        self.has_language_filter = not self.has_language_filter

    def set_date_of_birth(self, date_of_birth):
        self.date_of_birth = date_of_birth

    def set_location(self, location):
        self.location = location

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self.authenticated = checked
        return self.authenticated

    def serialize(self):
        return dict([(k, self.__getattribute__(k)) for k in self.SERIALIZE_LIST])

    def serialize_profile(self):
        return dict([(k, self.__getattribute__(k)) for k in self.SERIALIZE_PROFILE_LIST])
