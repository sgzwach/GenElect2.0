from genElect.models import Users
from genElect import db
from getpass import getpass
import bcrypt

def main():
    username = input('Username: ')
    password = getpass('Password: ')
    new_user = Users(username=username, full_name=username, role="admin", email=f'{username}@localhost', password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()))
    db.session.add(new_user)
    db.session.commit()

if __name__ == '__main__':
    main()
