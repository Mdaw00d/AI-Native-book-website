#!/usr/bin/env python3
"""
LLM Cognitive Planner for VLA Integration
Converts natural language commands to structured ROS 2 task plans
"""

import json
import os
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class Task:
    """Individual task in the plan"""
    task_id: int
    task_type: str  # "navigate", "detect", "manipulate", "inspect"
    parameters: Dict[str, Any]
    preconditions: List[int]
    expected_duration: float


@dataclass
class FeasibilityAssessment:
    """Plan feasibility evaluation"""
    is_feasible: bool
    confidence: float
    warnings: List[str]


@dataclass
class PlanMetadata:
    """Generation metadata"""
    llm_model: str
    prompt_tokens: int
    completion_tokens: int
    generation_time: float
    schema_version: str = "1.0.0"


@dataclass
class TaskPlan:
    """Complete task plan with metadata"""
    tasks: List[Task]
    feasibility: FeasibilityAssessment
    metadata: PlanMetadata


class LLMPlanner:
    """LLM-based cognitive planner for robot task generation"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        temperature: float = 0.0
    ):
        """
        Initialize LLM planner

        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY env var)
            model: Model to use (default "gpt-4")
            temperature: Sampling temperature (0.0 for deterministic)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required (set OPENAI_API_KEY)")

        self.model = model
        self.temperature = temperature
        self.client = openai.OpenAI(api_key=self.api_key)

        # Load JSON schema for validation
        schema_path = os.path.join(
            os.path.dirname(__file__),
            "../../contracts/task-plan-schema.json"
        )
        try:
            with open(schema_path, 'r') as f:
                self.schema = json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Schema not found at {schema_path}, using inline schema")
            self.schema = self._get_inline_schema()

    def _get_inline_schema(self) -> Dict:
        """Fallback inline schema if file not found"""
        return {
            "type": "object",
            "required": ["tasks", "feasibility", "metadata"],
            "properties": {
                "tasks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["task_id", "task_type", "parameters", "preconditions", "expected_duration"],
                        "properties": {
                            "task_id": {"type": "integer", "minimum": 1},
                            "task_type": {"type": "string", "enum": ["navigate", "detect", "manipulate", "inspect"]},
                            "parameters": {"type": "object"},
                            "preconditions": {"type": "array", "items": {"type": "integer"}},
                            "expected_duration": {"type": "number", "minimum": 0.1}
                        }
                    }
                },
                "feasibility": {
                    "type": "object",
                    "required": ["is_feasible", "confidence"],
                    "properties": {
                        "is_feasible": {"type": "boolean"},
                        "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                        "warnings": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "metadata": {
                    "type": "object",
                    "required": ["llm_model", "generation_time", "schema_version"]
                }
            }
        }

    def _create_system_prompt(self) -> str:
        """Create system prompt for task planning"""
        return """You are a robotic task planner. Convert natural language commands into structured JSON task plans for a humanoid robot.

AVAILABLE TASK TYPES:
- navigate: Move to a location
- detect: Perceive objects using vision
- manipulate: Pick/place objects
- inspect: Visual inspection

TASK PLAN FORMAT (strict JSON):
{
  "tasks": [
    {
      "task_id": 1,
      "task_type": "navigate",
      "parameters": {"target": "location_name", "position": [x, y, z]},
      "preconditions": [],
      "expected_duration": 10.0
    }
  ],
  "feasibility": {
    "is_feasible": true,
    "confidence": 0.95,
    "warnings": []
  },
  "metadata": {
    "llm_model": "gpt-4",
    "generation_time": 1.2,
    "schema_version": "1.0.0"
  }
}

SAFETY CONSTRAINTS:
- Ensure navigation before manipulation
- Validate object detection before grasping
- Check workspace limits (x: -5 to 5, y: -5 to 5, z: 0 to 3 meters)
- Avoid collision paths

Return ONLY valid JSON matching the schema. No explanations."""

    def generate_plan(
        self,
        command: str,
        environment_context: Optional[Dict] = None,
        max_retries: int = 3
    ) -> TaskPlan:
        """
        Generate task plan from natural language command

        Args:
            command: Natural language command (e.g., "Navigate to the kitchen")
            environment_context: Optional context (known objects, locations)
            max_retries: Maximum retry attempts on failure

        Returns:
            TaskPlan with structured tasks

        Raises:
            ValueError: If plan generation fails after retries
        """
        print(f"🧠 Planning: \"{command}\"")

        # Build user message
        user_message = f"Command: {command}"
        if environment_context:
            user_message += f"\n\nEnvironment Context:\n{json.dumps(environment_context, indent=2)}"

        for attempt in range(max_retries):
            try:
                start_time = time.time()

                # Call OpenAI API
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self._create_system_prompt()},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=self.temperature,
                    response_format={"type": "json_object"}  # Force JSON output
                )

                generation_time = time.time() - start_time

                # Parse response
                content = response.choices[0].message.content
                plan_data = json.loads(content)

                # Validate against schema (basic check)
                self._validate_plan(plan_data)

                # Add metadata
                plan_data["metadata"] = {
                    "llm_model": self.model,
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "generation_time": generation_time,
                    "schema_version": "1.0.0"
                }

                # Convert to TaskPlan object
                task_plan = self._dict_to_task_plan(plan_data)

                print(f"✓ Generated {len(task_plan.tasks)} tasks in {generation_time:.2f}s")

                # Check feasibility
                if not task_plan.feasibility.is_feasible:
                    print(f"⚠️  Plan marked as infeasible (confidence: {task_plan.feasibility.confidence:.2f})")
                    for warning in task_plan.feasibility.warnings:
                        print(f"    - {warning}")

                return task_plan

            except json.JSONDecodeError as e:
                print(f"⚠️  Attempt {attempt + 1}/{max_retries}: Invalid JSON - {e}")
                if attempt == max_retries - 1:
                    raise ValueError(f"Failed to generate valid JSON after {max_retries} attempts")
                time.sleep(2 ** attempt)  # Exponential backoff

            except Exception as e:
                print(f"⚠️  Attempt {attempt + 1}/{max_retries}: Error - {e}")
                if attempt == max_retries - 1:
                    raise ValueError(f"Plan generation failed: {e}")
                time.sleep(2 ** attempt)

    def _validate_plan(self, plan_data: Dict) -> None:
        """Basic validation of plan structure"""
        required_keys = ["tasks", "feasibility"]
        for key in required_keys:
            if key not in plan_data:
                raise ValueError(f"Missing required key: {key}")

        if not isinstance(plan_data["tasks"], list):
            raise ValueError("Tasks must be a list")

        if len(plan_data["tasks"]) == 0:
            raise ValueError("Plan must contain at least one task")

    def _dict_to_task_plan(self, data: Dict) -> TaskPlan:
        """Convert dictionary to TaskPlan object"""
        tasks = [
            Task(
                task_id=t["task_id"],
                task_type=t["task_type"],
                parameters=t["parameters"],
                preconditions=t.get("preconditions", []),
                expected_duration=t.get("expected_duration", 10.0)
            )
            for t in data["tasks"]
        ]

        feasibility = FeasibilityAssessment(
            is_feasible=data["feasibility"]["is_feasible"],
            confidence=data["feasibility"]["confidence"],
            warnings=data["feasibility"].get("warnings", [])
        )

        metadata = PlanMetadata(**data["metadata"])

        return TaskPlan(tasks=tasks, feasibility=feasibility, metadata=metadata)

    def plan_to_json(self, plan: TaskPlan) -> str:
        """Convert TaskPlan to JSON string"""
        return json.dumps(asdict(plan), indent=2)


def main():
    """Demo: Generate task plan from command"""
    import argparse

    parser = argparse.ArgumentParser(description="LLM Task Planner Demo")
    parser.add_argument(
        "--command",
        type=str,
        default="Navigate to the kitchen and pick up the red cup",
        help="Natural language command"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4",
        help="OpenAI model to use"
    )

    args = parser.parse_args()

    # Initialize planner
    try:
        planner = LLMPlanner(model=args.model)
    except ValueError as e:
        print(f"❌ {e}")
        print("Set OPENAI_API_KEY environment variable or use .env file")
        return

    # Generate plan
    print("\n🤖 LLM Task Planner Demo")
    print("=" * 60)

    try:
        plan = planner.generate_plan(
            command=args.command,
            environment_context={
                "known_objects": ["red cup", "table", "chair"],
                "known_locations": ["kitchen", "living room"]
            }
        )

        # Display results
        print("\n" + "=" * 60)
        print("📋 Generated Task Plan")
        print("=" * 60)
        print(planner.plan_to_json(plan))
        print("=" * 60)

        print(f"\n✅ Success! {len(plan.tasks)} tasks generated")
        print(f"   Feasibility: {plan.feasibility.confidence:.0%}")
        print(f"   Total estimated time: {sum(t.expected_duration for t in plan.tasks):.1f}s")

    except ValueError as e:
        print(f"\n❌ Planning failed: {e}")


if __name__ == "__main__":
    main()
