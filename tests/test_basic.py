# this is an example and not yet working, build tests for everything later
import os
import unittest
 
from genElect import app, db
 
TEST_DB = 'test.db'
 
 
class BasicTests(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
        self.assertEqual(app.debug, False)
    # executed after each test
    def tearDown(self):
        pass
 

    # Unauthenticated testing
    # Making sure all pages are available

    def test_notifications(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/index', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.app.get('/about', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_contact(self):
        response = self.app.get('/contact', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.app.get('/login', follow_redirects=True) 
        self.assertEqual(response.status_code, 200)

    def test_fail(self):
        response = self.app.get('/fail', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
 
if __name__ == "__main__":
    unittest.main()