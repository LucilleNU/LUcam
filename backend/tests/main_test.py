import unittest
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app, db, User

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register(self):
        response = self.app.post('/register', json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.data)

        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.password.startswith('$2'))

        response = self.app.post('/register', json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Registration failed', response.data)

    def test_login(self):
        user = User(username='testuser', email='testuser@example.com', password='$2a$12$t5ix5e5oQd.Uw/fGcv0pj.C/KZm1tZgezA7IpefD9XO70G09k/bJW')
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        response = self.app.post('/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'User not found', response.data)

        response = self.app.post('/login', json={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid password', response.data)

        response = self.app.post('/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)

    def test_recordings(self):
        with app.app_context():
            user = User(username='testuser', email='testuser@example.com', password='$2a$12$t5ix5e5oQd.Uw/fGcv0pj.C/KZm1tZgezA7IpefD9XO70G09k/bJW')
            db.session.add(user)
            db.session.commit()
            db.session.close()

            conn = sqlite3.connect(':memory:')
            cur = conn.cursor()
            cur.execute('INSERT INTO current_user (username) VALUES (?)', ('testuser',))
            conn.commit()
            cur.execute('INSERT INTO videos (url, username) VALUES (?, ?)', ('video1.mp4', 'testuser'))
            conn.commit()
            cur.execute('SELECT url FROM videos WHERE username = ?', ('testuser',))
            result = cur.fetchall()
            conn.close()

        response = self.app.get('/recordings')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'video1.mp4', response.data)

    def test_dashboard(self):
        response = self.app
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'Location:', response.data)
        self.assertIn(b'/login', response.data)

        with app.app_context():
            user = User(username='testuser', email='testuser@example.com', password='$2a$12$t5ix5e5oQd.Uw/fGcv0pj.C/KZm1tZgezA7IpefD9XO70G09k/bJW')
            db.session.add(user)
            db.session.commit()

            with self.app as client:
                with client.session_transaction() as session:
                    session['user_id'] = user.id

                response = self.app.get('/dashboard')
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'Dashboard', response.data)

    def test_logout(self):
        with app.app_context():
            user = User(username='testuser', email='testuser@example.com', password='$2a$12$t5ix5e5oQd.Uw/fGcv0pj.C/KZm1tZgezA7IpefD9XO70G09k/bJW')
            db.session.add(user)
            db.session.commit()

            with self.app as client:
                with client.session_transaction() as session:
                    session['user_id'] = user.id

                response = self.app.get('/logout')
                self.assertEqual(response.status_code, 302)
                self.assertIn(b'Location:', response.data)
                self.assertIn(b'/login', response.data)

                with client.session_transaction() as session:
                    self.assertNotIn('user_id', session)

    def test_start_recording(self):
        response = self.app.post('/start-recording')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recording started', response.data)

    def test_stop_recording(self):
        response = self.app.post('/stop-recording')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Stopped Recording and Saved Video', response.data)

    def test_toggle_notification(self):
        response = self.app.post('/toggle_notification', data={
            'status': 'on',
            'permission': 'granted'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
            'message': 'Notification settings updated',
            'status': 'on',
            'permission': 'granted'
        })

if __name__ == '__main__':
    unittest.main()


