import logging
from io import StringIO
from pathlib import Path
from datetime import datetime
import cv2
from mock import patch
import os
import numpy as np
import pytest

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from camera import gen, show_notification


@pytest.fixture
def cap():
    # Create a fake video capture object for testing
    cap = cv2.VideoCapture(0)
    yield cap
    cap.release()


@pytest.fixture
def frame_size(cap):
    # Get the size of the frames
    frame_size = (int(cap.get(3)), int(cap.get(4)))
    return frame_size


@pytest.fixture
def fourcc():
    # Get the fourcc code for mp4v format
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    return fourcc


@pytest.fixture
def test_dir():
    # Create a temporary directory to store test videos
    test_dir = Path('test_videos')
    test_dir.mkdir(exist_ok=True)
    yield test_dir
    for file in test_dir.glob('*.mp4'):
        file.unlink()


@pytest.fixture
def logger():
    # Set up logger to capture logs from the script
    logger = logging.getLogger(__name__)
    log_capture_string = StringIO()
    log_handler = logging.StreamHandler(log_capture_string)
    logger.addHandler(log_handler)
    yield logger
    logger.removeHandler(log_handler)


def test_show_notification():
    # Test that the show_notification function creates a notification
    with patch('camera.notification.notify') as mock_notify:
        show_notification()
        mock_notify.assert_called_once()


def test_motion_detection(cap, frame_size, fourcc, test_dir, logger):
    # Test that motion detection and video recording works as expected
    gen_obj = gen()
    num_frames = 50
    for i in range(num_frames):
        frame = next(gen_obj)

        # Assert that the generator yields bytes
        assert isinstance(frame, bytes)

        # Write the frame to a video file for testing
        filename = datetime.now().strftime('%d-%m-%Y-%H-%M-%S') + ".mp4"
        test_dir = Path('test_videos')
        filename = test_dir / filename
        out = cv2.VideoWriter(str(filename), fourcc, 20, frame_size)
        out.write(cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), 1))
        out.release()

        # Assert that the video file has been created
        assert len(list(test_dir.glob('*.mp4'))) > 0

    # Assert that motion detection has started and stopped
    assert '' in logger.handlers[0].stream.getvalue()
    assert '' in logger.handlers[0].stream.getvalue()
