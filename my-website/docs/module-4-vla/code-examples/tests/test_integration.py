#!/usr/bin/env python3
"""
Integration Tests for VLA Pipeline

Tests T027-T029:
- T027: Navigation scenario
- T028: Perception scenario
- T029: Full manipulation scenario
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from full_pipeline import VLAPipeline, PipelineState, PipelineResult


class TestNavigationScenario:
    """T027: Navigation-only scenario"""

    def test_navigate_to_kitchen(self):
        """Test: voice command → navigate to kitchen"""
        pipeline = VLAPipeline()
        result = pipeline.run("Navigate to the kitchen")

        assert result.success is True
        assert result.state == PipelineState.COMPLETE
        assert result.execution_time > 0


class TestPerceptionScenario:
    """T028: Perception scenario"""

    def test_find_red_cup(self):
        """Test: voice command → find red cup"""
        pipeline = VLAPipeline()
        result = pipeline.run("Find the red cup")

        assert result.success is True
        assert result.state == PipelineState.COMPLETE


class TestManipulationScenario:
    """T029: Full manipulation scenario"""

    def test_pick_and_place(self):
        """Test: voice command → pick up cup and place on table"""
        pipeline = VLAPipeline()
        result = pipeline.run("Pick up the cup and place it on the table")

        assert result.success is True
        assert result.state == PipelineState.COMPLETE
        assert result.tasks_completed > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
