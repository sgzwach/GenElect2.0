#Run this to reset the database and add the admin user

from genElect.models import *

db.drop_all()
db.create_all()

user = Users(username='admin', email='jarod.keene@trojans.dsu.edu', full_name='admin', password='Password1!', role='admin')
db.session.add(user)
db.session.commit()