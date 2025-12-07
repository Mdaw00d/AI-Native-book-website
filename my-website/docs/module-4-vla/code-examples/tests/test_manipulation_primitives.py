#!/usr/bin/env python3
"""Unit Tests for Manipulation Primitives"""

import pytest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from manipulation_primitives import ManipulationPrimitives, GraspPose, ManipulationResult

class TestGraspPose:
    def test_grasp_creation(self):
        grasp = GraspPose(position=(0.5, 0.0, 0.2))
        assert grasp.position == (0.5, 0.0, 0.2)

class TestManipulationResult:
    def test_result_creation(self):
        result = ManipulationResult(success=True, message="Done")
        assert result.success is True

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
