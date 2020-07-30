import unittest
import flask
import os

from flask import g, url_for, session

import db
db.data_source_name = 'host=faraday.cse.taylor.edu dbname=dthomas008 user=dthomas008 password=roduqedi'
from gardenerexchange import app

class FlaskTestCase(unittest.TestCase):
    # This is a helper class that sets up the proper Flask execution context
    # so that the test cases that inherit it will work properly.
    def setUp(self):
        # Allow exceptions (if any) to propagate to the test client.
        app.testing = True

        # Create a test client.
        self.client = app.test_client(use_cookies=True)

        # Set session data
        with app.test_client() as client:
            with client.session_transaction() as sess:
                # Modify the session in this context block.
                sess['user'] = 'drwhite'
                sess['remember'] = 'drwhite'
                sess['email'] = 'artwhite@example.com'
                sess['location'] = 47348
                sess['address'] = '506 E Van Cleve St'

        # Create an application context for testing.
        self.app_context = app.test_request_context()
        self.app_context.push()

    def tearDown(self):
        # Clean up the application context.
        self.app_context.pop()


class ApplicationTestCase(FlaskTestCase):
    """Test the basic behavior of page routing and display"""

    def test_home_page(self):
        """Verify the home page."""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                # Modify the session in this context block.
                sess['user'] = 'drwhite'
                sess['remember'] = 'drwhite'
                sess['email'] = 'artwhite@example.com'
                sess['location'] = 47348
                sess['address'] = '506 E Van Cleve St'
        resp = self.client.get('/')
        self.assertTrue(b'Gardener' in resp.data, "Didn't find Gardener on home page")

    def test_feed(self):
        """Verify the main feed"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                # Modify the session in this context block.
                sess["last_num"] = "8"
                sess['user'] = 'drwhite'
                sess['remember'] = 'drwhite'
                sess['email'] = 'artwhite@example.com'
                sess['location'] = 47348
                sess['address'] = '506 E Van Cleve St'
        resp = self.client.get('/item_feed')
        self.assertTrue(b'Item Feed' in resp.data, "Didn't find item feed on feed")

    def test_profile(self):
        """Verify the profile page"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                # Modify the session in this context block.
                sess["last_num"] = "8"
                sess['user'] = 'drwhite'
                sess['remember'] = 'drwhite'
                sess['email'] = 'artwhite@example.com'
                sess['location'] = 47348
                sess['address'] = '506 E Van Cleve St'
        resp = self.client.get(url_for('profile', user = session['user']))
        self.assertTrue(b'Profile' in resp.data, "Didn't find profile")




class DatabaseTestCase(FlaskTestCase):
    """Test database access and update functions."""

    @staticmethod
    def execute_sql(resource_name):
        """Helper function to run a SQL script on the test database."""
        with app.open_resource(resource_name, mode='r') as f:
            g.cursor.execute(f.read())
        g.connection.commit()

    def setUp(self):
        """Open the database connection and create all the tables."""
        super(DatabaseTestCase, self).setUp()
        db.open_db_connection()
        self.execute_sql('db/create_db.sql')

    def tearDown(self):
        """Clear all tables in the database and close the connection."""
        db.close_db_connection(self)
        super(DatabaseTestCase, self).tearDown()

    def test_create_item(self):
        """Make sure we can add a new member."""
        row_count = db.create_item('test_item', '100', 'test_unit', 'test_user')
        self.assertEqual(row_count, 1)






# Do the right thing if this file is run standalone.
if __name__ == '__main__':
    unittest.main()