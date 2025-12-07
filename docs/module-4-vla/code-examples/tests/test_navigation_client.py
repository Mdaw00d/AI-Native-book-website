#!/usr/bin/env python3
"""Unit Tests for Navigation Client"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from navigation_client import NavigationClient, NavigationGoal, NavigationResult

@pytest.fixture
def mock_rclpy():
    with patch('navigation_client.rclpy') as mock:
        yield mock

class TestNavigationGoal:
    def test_goal_creation(self):
        goal = NavigationGoal(x=2.0, y=3.0, z=0.0)
        assert goal.x == 2.0
        assert goal.y == 3.0

class TestNavigationResult:
    def test_result_creation(self):
        result = NavigationResult(success=True, message="Done", duration=10.0)
        assert result.success is True
        assert result.duration == 10.0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
