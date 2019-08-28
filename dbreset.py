#Run this to reset the database and add the admin user

from genElect.models import *

db.drop_all()
db.create_all()
#create username with admin:Password1! as creds
user = Users(username='admin', email='jarod.keene@trojans.dsu.edu', full_name='admin', password='ecb3548b49fefa9c984ec134fa362b3316ec8cc4c044b3a71444eed538ecc39461fe5d4dd1d71287fcd2b1c3354cc36873956b3e15229b5acbdacda276babed1', role='admin')
db.session.add(user)
db.session.commit()