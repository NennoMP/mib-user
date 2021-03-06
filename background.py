import os
import smtplib, ssl
import random

from celery import Celery
import config

os.environ['FLASK_ENV']='development'


BACKEND = BROKER = 'redis://localhost:6379/0'

celery = Celery(__name__, broker=BROKER, backend=BACKEND)

_APP = None

from mib import create_app

def lazy_init():
    '''Returns the application singleton.'''
    global _APP
    if _APP is None:
        app = create_app()
        from mib import db
        db.init_app(app)
        _APP = app
    return _APP


def send_email(email, message):
    '''Utility function to send email notification for the application.'''
    password = None
    with open('token.txt') as f:
        password = f.readline()

    smtp_server = 'smtp.gmail.com'
    port = 465
    sender_email = 'asesquad5@gmail.com'
    receiver_email = email
    message = f'''\
    Subject: MyMessageInABottle - Notification

    {message}'''

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port,context=context) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


@celery.task
def notify(user_id, message):
    '''Sends an email containing <message> to the user
       identified with <user_id>, if present and active.
    '''
    app = lazy_init()
    with app.app_context():
        from mib.dao.user_manager import UserManager
        try: user = UserManager.retrieve_by_id(user_id)
        except RuntimeError as e:
            print(str(e))
            return 
        if user is None or not user.is_active:
            return 'Email not sent'

        #send_email(user.email, message)
        print(user.email)
    return 'Email sent'


@celery.task
def lottery():
    '''Increases the bonus of a random user
        and sends a notification for that.
    '''
    app = lazy_init()
    with app.app_context():
        from mib import db
        from mib.models.user import User

        n_users = int(User.query.count())
        random_n = random.randint(0, n_users+1)
        random_user = User.query.filter_by(id=random_n).first()
        if random_user is None or not random_user.is_active:
            lottery.delay()
            return 'Redoing lottery'

        random_user.bonus += 1
        db.session.commit()
        message = 'Congratulations, you won a bonus deletion!'
        notify.delay(random_user.id, message)

    return 'Lottery done'


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    '''Registers the periodic tasks.'''
    seconds_in_a = {
        'minute': 1,
        'month': 60*60*24*30
    }
    sender.add_periodic_task(seconds_in_a['month'], lottery.s(), name='lottery')
