#!/usr/bin/env python3
"""
Unit Tests for LLM Planner Module

Tests cover:
- LLM initialization and configuration
- Task plan generation
- JSON schema validation
- Retry logic and error handling
- Feasibility assessment
- Safety constraint checking

Run with: pytest test_llm_planner.py -v --cov=scripts.llm_planner
"""

import pytest
import json
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
from dataclasses import asdict

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from llm_planner import (
    LLMPlanner,
    Task,
    TaskPlan,
    FeasibilityAssessment,
    PlanMetadata
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing without API calls"""
    with patch('llm_planner.openai.OpenAI') as mock_openai:
        mock_client = MagicMock()

        # Mock response structure
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps({
            "tasks": [
                {
                    "task_id": 1,
                    "task_type": "navigate",
                    "parameters": {"target": "kitchen", "position": [2.0, 3.0, 0.0]},
                    "preconditions": [],
                    "expected_duration": 10.0
                }
            ],
            "feasibility": {
                "is_feasible": True,
                "confidence": 0.95,
                "warnings": []
            }
        })
        mock_response.usage.prompt_tokens = 150
        mock_response.usage.completion_tokens = 80

        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        yield mock_client


@pytest.fixture
def sample_task():
    """Sample task for testing"""
    return Task(
        task_id=1,
        task_type="navigate",
        parameters={"target": "kitchen", "position": [2.0, 3.0, 0.0]},
        preconditions=[],
        expected_duration=10.0
    )


@pytest.fixture
def sample_feasibility():
    """Sample feasibility assessment"""
    return FeasibilityAssessment(
        is_feasible=True,
        confidence=0.95,
        warnings=[]
    )


@pytest.fixture
def sample_metadata():
    """Sample plan metadata"""
    return PlanMetadata(
        llm_model="gpt-4",
        prompt_tokens=150,
        completion_tokens=80,
        generation_time=1.5,
        schema_version="1.0.0"
    )


@pytest.fixture
def sample_task_plan(sample_task, sample_feasibility, sample_metadata):
    """Sample complete task plan"""
    return TaskPlan(
        tasks=[sample_task],
        feasibility=sample_feasibility,
        metadata=sample_metadata
    )


@pytest.fixture
def planner_with_mock(mock_openai_client):
    """LLM planner with mocked OpenAI client"""
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
        planner = LLMPlanner(api_key='test-key', model='gpt-4')
        return planner


# ============================================================================
# Initialization Tests
# ============================================================================

class TestLLMPlannerInit:
    """Test LLMPlanner initialization"""

    def test_init_with_api_key(self, mock_openai_client):
        """Test initialization with explicit API key"""
        planner = LLMPlanner(api_key='test-key', model='gpt-4')

        assert planner.api_key == 'test-key'
        assert planner.model == 'gpt-4'
        assert planner.temperature == 0.0

    def test_init_with_env_var(self, mock_openai_client):
        """Test initialization using environment variable"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'env-key'}):
            planner = LLMPlanner(model='gpt-3.5-turbo')

            assert planner.api_key == 'env-key'
            assert planner.model == 'gpt-3.5-turbo'

    def test_init_no_api_key(self, mock_openai_client):
        """Test initialization fails without API key"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="OpenAI API key required"):
                LLMPlanner()

    def test_init_custom_temperature(self, mock_openai_client):
        """Test initialization with custom temperature"""
        planner = LLMPlanner(api_key='test-key', temperature=0.7)

        assert planner.temperature == 0.7

    def test_schema_loading(self, mock_openai_client):
        """Test JSON schema loading"""
        planner = LLMPlanner(api_key='test-key')

        # Should have schema (either from file or inline)
        assert planner.schema is not None
        assert 'properties' in planner.schema
        assert 'tasks' in planner.schema['properties']


# ============================================================================
# Data Classes Tests
# ============================================================================

class TestDataClasses:
    """Test data class definitions"""

    def test_task_creation(self):
        """Test Task dataclass creation"""
        task = Task(
            task_id=1,
            task_type="navigate",
            parameters={"target": "kitchen"},
            preconditions=[],
            expected_duration=5.0
        )

        assert task.task_id == 1
        assert task.task_type == "navigate"
        assert task.parameters["target"] == "kitchen"
        assert len(task.preconditions) == 0
        assert task.expected_duration == 5.0

    def test_feasibility_creation(self):
        """Test FeasibilityAssessment creation"""
        feasibility = FeasibilityAssessment(
            is_feasible=True,
            confidence=0.9,
            warnings=["Low confidence"]
        )

        assert feasibility.is_feasible is True
        assert feasibility.confidence == 0.9
        assert len(feasibility.warnings) == 1

    def test_task_plan_creation(self, sample_task, sample_feasibility, sample_metadata):
        """Test TaskPlan creation"""
        plan = TaskPlan(
            tasks=[sample_task],
            feasibility=sample_feasibility,
            metadata=sample_metadata
        )

        assert len(plan.tasks) == 1
        assert plan.feasibility.is_feasible is True
        assert plan.metadata.llm_model == "gpt-4"


# ============================================================================
# Plan Generation Tests
# ============================================================================

class TestPlanGeneration:
    """Test plan generation functionality"""

    def test_generate_simple_plan(self, planner_with_mock):
        """Test generating a simple navigation plan"""
        command = "Navigate to the kitchen"

        plan = planner_with_mock.generate_plan(command)

        assert isinstance(plan, TaskPlan)
        assert len(plan.tasks) > 0
        assert plan.tasks[0].task_type == "navigate"
        assert plan.feasibility.is_feasible is True

    def test_generate_with_context(self, planner_with_mock):
        """Test plan generation with environment context"""
        command = "Pick up the cup"
        context = {
            "known_objects": ["cup", "table"],
            "known_locations": ["kitchen"]
        }

        plan = planner_with_mock.generate_plan(command, environment_context=context)

        assert isinstance(plan, TaskPlan)
        assert plan.metadata.prompt_tokens > 0

    def test_generate_plan_metadata(self, planner_with_mock):
        """Test that plan includes correct metadata"""
        plan = planner_with_mock.generate_plan("Navigate to kitchen")

        assert plan.metadata.llm_model == planner_with_mock.model
        assert plan.metadata.prompt_tokens > 0
        assert plan.metadata.completion_tokens > 0
        assert plan.metadata.generation_time > 0
        assert plan.metadata.schema_version == "1.0.0"

    def test_multiple_tasks_plan(self, planner_with_mock, mock_openai_client):
        """Test generating plan with multiple tasks"""
        # Update mock to return multi-task plan
        multi_task_response = {
            "tasks": [
                {
                    "task_id": 1,
                    "task_type": "navigate",
                    "parameters": {"target": "kitchen"},
                    "preconditions": [],
                    "expected_duration": 10.0
                },
                {
                    "task_id": 2,
                    "task_type": "detect",
                    "parameters": {"object": "cup"},
                    "preconditions": [1],
                    "expected_duration": 3.0
                },
                {
                    "task_id": 3,
                    "task_type": "manipulate",
                    "parameters": {"action": "pick", "object": "cup"},
                    "preconditions": [1, 2],
                    "expected_duration": 5.0
                }
            ],
            "feasibility": {
                "is_feasible": True,
                "confidence": 0.9,
                "warnings": []
            }
        }

        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = json.dumps(multi_task_response)

        plan = planner_with_mock.generate_plan("Pick up the cup")

        assert len(plan.tasks) == 3
        assert plan.tasks[0].task_type == "navigate"
        assert plan.tasks[1].task_type == "detect"
        assert plan.tasks[2].task_type == "manipulate"
        assert 1 in plan.tasks[2].preconditions


# ============================================================================
# Validation Tests
# ============================================================================

class TestPlanValidation:
    """Test plan validation logic"""

    def test_validate_valid_plan(self, planner_with_mock):
        """Test validation passes for valid plan"""
        valid_plan = {
            "tasks": [{"task_id": 1, "task_type": "navigate", "parameters": {}}],
            "feasibility": {"is_feasible": True, "confidence": 0.9}
        }

        # Should not raise
        planner_with_mock._validate_plan(valid_plan)

    def test_validate_missing_tasks(self, planner_with_mock):
        """Test validation fails when tasks missing"""
        invalid_plan = {
            "feasibility": {"is_feasible": True, "confidence": 0.9}
        }

        with pytest.raises(ValueError, match="Missing required key: tasks"):
            planner_with_mock._validate_plan(invalid_plan)

    def test_validate_missing_feasibility(self, planner_with_mock):
        """Test validation fails when feasibility missing"""
        invalid_plan = {
            "tasks": [{"task_id": 1, "task_type": "navigate", "parameters": {}}]
        }

        with pytest.raises(ValueError, match="Missing required key: feasibility"):
            planner_with_mock._validate_plan(invalid_plan)

    def test_validate_tasks_not_list(self, planner_with_mock):
        """Test validation fails when tasks not a list"""
        invalid_plan = {
            "tasks": "not a list",
            "feasibility": {"is_feasible": True, "confidence": 0.9}
        }

        with pytest.raises(ValueError, match="Tasks must be a list"):
            planner_with_mock._validate_plan(invalid_plan)

    def test_validate_empty_tasks(self, planner_with_mock):
        """Test validation fails with empty task list"""
        invalid_plan = {
            "tasks": [],
            "feasibility": {"is_feasible": True, "confidence": 0.9}
        }

        with pytest.raises(ValueError, match="at least one task"):
            planner_with_mock._validate_plan(invalid_plan)


# ============================================================================
# Retry Logic Tests
# ============================================================================

class TestRetryLogic:
    """Test retry mechanism"""

    def test_retry_on_json_decode_error(self, planner_with_mock, mock_openai_client):
        """Test retry on invalid JSON response"""
        # First attempt: invalid JSON
        # Second attempt: valid JSON
        responses = [
            MagicMock(choices=[MagicMock(message=MagicMock(content="invalid json"))]),
            MagicMock(choices=[MagicMock(message=MagicMock(content=json.dumps({
                "tasks": [{"task_id": 1, "task_type": "navigate", "parameters": {}, "preconditions": [], "expected_duration": 5.0}],
                "feasibility": {"is_feasible": True, "confidence": 0.9, "warnings": []}
            })))]),
        ]

        for resp in responses:
            resp.usage = MagicMock(prompt_tokens=100, completion_tokens=50)

        mock_openai_client.chat.completions.create.side_effect = responses

        # Should succeed on second attempt
        plan = planner_with_mock.generate_plan("Test command", max_retries=3)

        assert isinstance(plan, TaskPlan)
        assert mock_openai_client.chat.completions.create.call_count == 2

    def test_max_retries_exceeded(self, planner_with_mock, mock_openai_client):
        """Test failure after max retries"""
        # All attempts return invalid JSON
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "invalid json"

        with pytest.raises(ValueError, match="Failed to generate valid JSON"):
            planner_with_mock.generate_plan("Test command", max_retries=2)

    def test_retry_with_exception(self, planner_with_mock, mock_openai_client):
        """Test retry on API exception"""
        # First: exception, Second: success
        valid_response = MagicMock()
        valid_response.choices = [MagicMock(message=MagicMock(content=json.dumps({
            "tasks": [{"task_id": 1, "task_type": "navigate", "parameters": {}, "preconditions": [], "expected_duration": 5.0}],
            "feasibility": {"is_feasible": True, "confidence": 0.9, "warnings": []}
        })))]
        valid_response.usage = MagicMock(prompt_tokens=100, completion_tokens=50)

        mock_openai_client.chat.completions.create.side_effect = [
            Exception("API Error"),
            valid_response
        ]

        plan = planner_with_mock.generate_plan("Test", max_retries=3)
        assert isinstance(plan, TaskPlan)


# ============================================================================
# Schema Tests
# ============================================================================

class TestSchemaHandling:
    """Test JSON schema handling"""

    def test_inline_schema_structure(self, planner_with_mock):
        """Test inline schema has correct structure"""
        schema = planner_with_mock._get_inline_schema()

        assert schema['type'] == 'object'
        assert 'tasks' in schema['properties']
        assert 'feasibility' in schema['properties']

        # Check task schema
        task_schema = schema['properties']['tasks']['items']
        assert 'task_id' in task_schema['properties']
        assert 'task_type' in task_schema['properties']

        # Check task types enum
        assert set(task_schema['properties']['task_type']['enum']) == {
            'navigate', 'detect', 'manipulate', 'inspect'
        }


# ============================================================================
# System Prompt Tests
# ============================================================================

class TestSystemPrompt:
    """Test system prompt generation"""

    def test_system_prompt_includes_task_types(self, planner_with_mock):
        """Test system prompt includes all task types"""
        prompt = planner_with_mock._create_system_prompt()

        assert 'navigate' in prompt
        assert 'detect' in prompt
        assert 'manipulate' in prompt
        assert 'inspect' in prompt

    def test_system_prompt_includes_constraints(self, planner_with_mock):
        """Test system prompt includes safety constraints"""
        prompt = planner_with_mock._create_system_prompt()

        assert 'SAFETY CONSTRAINTS' in prompt
        assert 'workspace' in prompt.lower() or 'bounds' in prompt.lower()

    def test_system_prompt_specifies_json(self, planner_with_mock):
        """Test system prompt requires JSON output"""
        prompt = planner_with_mock._create_system_prompt()

        assert 'JSON' in prompt


# ============================================================================
# Conversion Tests
# ============================================================================

class TestDataConversion:
    """Test data conversion utilities"""

    def test_dict_to_task_plan(self, planner_with_mock):
        """Test converting dictionary to TaskPlan"""
        plan_dict = {
            "tasks": [
                {
                    "task_id": 1,
                    "task_type": "navigate",
                    "parameters": {"target": "kitchen"},
                    "preconditions": [],
                    "expected_duration": 10.0
                }
            ],
            "feasibility": {
                "is_feasible": True,
                "confidence": 0.95,
                "warnings": []
            },
            "metadata": {
                "llm_model": "gpt-4",
                "prompt_tokens": 100,
                "completion_tokens": 50,
                "generation_time": 1.5,
                "schema_version": "1.0.0"
            }
        }

        plan = planner_with_mock._dict_to_task_plan(plan_dict)

        assert isinstance(plan, TaskPlan)
        assert len(plan.tasks) == 1
        assert plan.tasks[0].task_id == 1
        assert plan.feasibility.is_feasible is True

    def test_plan_to_json(self, planner_with_mock, sample_task_plan):
        """Test converting TaskPlan to JSON string"""
        json_str = planner_with_mock.plan_to_json(sample_task_plan)

        # Should be valid JSON
        parsed = json.loads(json_str)

        assert 'tasks' in parsed
        assert 'feasibility' in parsed
        assert 'metadata' in parsed


# ============================================================================
# Feasibility Tests
# ============================================================================

class TestFeasibilityAssessment:
    """Test feasibility assessment"""

    def test_infeasible_plan_warning(self, planner_with_mock, mock_openai_client):
        """Test plan marked as infeasible triggers warning"""
        infeasible_response = {
            "tasks": [{"task_id": 1, "task_type": "navigate", "parameters": {}, "preconditions": [], "expected_duration": 5.0}],
            "feasibility": {
                "is_feasible": False,
                "confidence": 0.3,
                "warnings": ["Command is physically impossible"]
            }
        }

        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = json.dumps(infeasible_response)

        plan = planner_with_mock.generate_plan("Fly to the moon")

        assert plan.feasibility.is_feasible is False
        assert plan.feasibility.confidence == 0.3
        assert len(plan.feasibility.warnings) > 0


# ============================================================================
# Integration Tests
# ============================================================================

class TestLLMPlannerIntegration:
    """Integration tests for complete workflows"""

    def test_end_to_end_planning(self, planner_with_mock):
        """Test complete planning workflow"""
        command = "Navigate to the kitchen and pick up the red cup"

        plan = planner_with_mock.generate_plan(command)

        # Verify plan structure
        assert isinstance(plan, TaskPlan)
        assert len(plan.tasks) > 0
        assert plan.feasibility is not None
        assert plan.metadata is not None

        # Verify can convert to JSON
        json_str = planner_with_mock.plan_to_json(plan)
        assert isinstance(json_str, str)

        # Verify JSON is valid
        parsed = json.loads(json_str)
        assert 'tasks' in parsed

    def test_plan_with_preconditions(self, planner_with_mock, mock_openai_client):
        """Test plan with task dependencies"""
        complex_response = {
            "tasks": [
                {"task_id": 1, "task_type": "navigate", "parameters": {"target": "kitchen"}, "preconditions": [], "expected_duration": 10.0},
                {"task_id": 2, "task_type": "detect", "parameters": {"object": "cup"}, "preconditions": [1], "expected_duration": 3.0}
            ],
            "feasibility": {"is_feasible": True, "confidence": 0.9, "warnings": []}
        }

        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = json.dumps(complex_response)

        plan = planner_with_mock.generate_plan("Find the cup in the kitchen")

        assert len(plan.tasks) == 2
        assert 1 in plan.tasks[1].preconditions


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=llm_planner", "--cov-report=term-missing"])
