import os
import datetime
from datetime import date
from flask.ext.script import Manager
from marker import app
from marker.models import Member, Cell, User
from marker.database import session as DBsession

from getpass import getpass
from werkzeug.security import generate_password_hash
from marker.models import User

from flask.ext.migrate import Migrate, MigrateCommand
from marker.database import Base


manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)


@manager.command
def adduser():
    name = raw_input("Name: ")
    email = raw_input("Email: ")
    if DBsession.query(User).filter_by(email=email).first():
        print "User with that email address already exists"
        return

    password = ""
    password_2 = ""
    while not (password and password_2) or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
    user = User(name=name, email=email,
                password=generate_password_hash(password))
    DBsession.add(user)
    DBsession.commit()   


@manager.command
def cellmember():
    member = Member(memb_name = 'Goerge',
            memb_address = "Morley Drive",
            memb_email = "smuzungu@yahoo.com",
            memb_contact = "040474449",
            cell_id = 2
            )

    DBsession.add(member)
    DBsession.commit()

  
    
class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)


    
if __name__ == '__main__':
    manager.run()




