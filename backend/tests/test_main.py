import pytest
from flask.testing import FlaskClient
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app


@pytest.fixture
def client() -> FlaskClient:
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def detection():
    return False


def test_dashboard(client: FlaskClient):
    response = client.get('/')
    assert response.status_code == 200


def test_video_feed(client: FlaskClient):
    response = client.get('/video_feed')
    assert response.status_code == 200
    assert response.content_type == 'multipart/x-mixed-replace; boundary=frame'


# def test_start_recording(client: FlaskClient, detection):
#     response = client.post('/start-recording')
#     assert response.status_code == 200
#     assert b'Recording started' in response.data


# def test_stop_recording(client: FlaskClient, detection):
#     response = client.post('/stop-recording')
#     assert response.status_code == 302


def test_toggle_notification(client: FlaskClient):
    response = client.post(
        '/toggle_notification',
        data={
            'status': 'yes',
            'permission': 'granted'
        }
    )
    assert response.status_code == 200
    assert response.data == b'OK'
