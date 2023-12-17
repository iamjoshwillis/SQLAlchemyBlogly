from unittest import TestCase

from app import app
from models import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase)
    
    def setUp(self):
        User.query.delete()

        user = User(first_name="Test", last_name="Case", image_url=" ")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):

        db.session.rollback()

    def test_show_home(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)

    def test_add_user(self):
        with app.test_client() as client:
            u = {"first_name": "Test", "last_name": "Case"}
            resp = client.post("/", data=u, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200, html)
    