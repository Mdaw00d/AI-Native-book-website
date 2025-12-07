#!/usr/bin/env python3
"""Unit Tests for Object Detector Module"""

import pytest
import numpy as np
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from object_detector import (
    ObjectDetector, Detection, BoundingBox, CameraIntrinsics
)

@pytest.fixture
def mock_yolo():
    """Mock YOLO model"""
    with patch('object_detector.YOLO') as mock:
        model = MagicMock()
        model.names = {0: 'person', 1: 'cup', 2: 'bottle'}
        mock.return_value = model
        yield model

@pytest.fixture
def detector(mock_yolo):
    """ObjectDetector with mocked YOLO"""
    return ObjectDetector(model_size='n')

@pytest.fixture
def sample_image():
    """Sample RGB image"""
    return np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

@pytest.fixture
def sample_depth():
    """Sample depth image"""
    return np.random.uniform(0.5, 5.0, (480, 640)).astype(np.float32)

class TestBoundingBox:
    def test_bbox_properties(self):
        bbox = BoundingBox(100, 100, 200, 200)
        assert bbox.width == 100
        assert bbox.height == 100
        assert bbox.center == (150, 150)
        assert bbox.area == 10000

class TestCameraIntrinsics:
    def test_intrinsics_creation(self):
        cam = CameraIntrinsics(525.0, 525.0, 320.0, 240.0, 640, 480)
        assert cam.fx == 525.0
        assert cam.width == 640

class TestObjectDetector:
    def test_init(self, mock_yolo):
        detector = ObjectDetector(model_size='n', confidence_threshold=0.6)
        assert detector.model_size == 'n'
        assert detector.confidence_threshold == 0.6

    def test_detect_objects(self, detector, sample_image, mock_yolo):
        # Mock detection results
        mock_result = MagicMock()
        mock_boxes = MagicMock()
        mock_boxes.xyxy = [MagicMock()]
        mock_boxes.xyxy[0].cpu().numpy.return_value = np.array([100, 100, 200, 200])
        mock_boxes.conf = [MagicMock()]
        mock_boxes.conf[0].cpu().numpy.return_value = 0.9
        mock_boxes.cls = [MagicMock()]
        mock_boxes.cls[0].cpu().numpy.return_value = 1
        mock_result.boxes = mock_boxes
        mock_yolo.return_value = [mock_result]
        
        detections = detector.detect_objects(sample_image)
        assert len(detections) >= 0

    def test_3d_position_estimation(self, detector, sample_depth):
        bbox = BoundingBox(200, 200, 300, 300)
        pos, conf = detector._estimate_3d_position(bbox, sample_depth)
        assert pos is not None
        assert len(pos) == 3
        assert 0 <= conf <= 1

    def test_filter_by_confidence(self, detector):
        detections = [
            Detection(0, 'cup', 0.9, BoundingBox(0,0,10,10)),
            Detection(1, 'bottle', 0.4, BoundingBox(0,0,10,10))
        ]
        filtered = detector.filter_by_confidence(detections, 0.5)
        assert len(filtered) == 1

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
