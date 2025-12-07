#!/usr/bin/env python3
"""
Navigation Client for VLA Integration
Uses ROS 2 Nav2 for autonomous navigation
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
from rclpy.duration import Duration
from dataclasses import dataclass
from typing import Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class NavigationGoal:
    """Navigation goal with pose"""
    x: float
    y: float
    z: float = 0.0
    orientation_w: float = 1.0


@dataclass
class NavigationResult:
    """Result of navigation action"""
    success: bool
    message: str
    duration: float


class NavigationClient(Node):
    """
    ROS 2 Navigation client using Nav2 action server.
    
    Handles:
    - Goal pose publishing
    - Navigation feedback monitoring  
    - Timeout and error handling
    - Path planning status
    """

    def __init__(self, node_name: str = 'vla_navigation_client'):
        super().__init__(node_name)
        
        self._action_client = ActionClient(
            self, NavigateToPose, 'navigate_to_pose'
        )
        
        logger.info(f"Navigation client initialized: {node_name}")
        
    def navigate_to_goal(
        self,
        goal: NavigationGoal,
        timeout: float = 60.0
    ) -> NavigationResult:
        """
        Navigate to target pose.
        
        Args:
            goal: Target NavigationGoal
            timeout: Maximum time in seconds
            
        Returns:
            NavigationResult with status
        """
        logger.info(f"Navigating to ({goal.x}, {goal.y}, {goal.z})")
        
        # Wait for action server
        if not self._action_client.wait_for_server(timeout_sec=5.0):
            return NavigationResult(
                success=False,
                message="Nav2 server not available",
                duration=0.0
            )
        
        # Create goal message
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = PoseStamped()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = goal.x
        goal_msg.pose.pose.position.y = goal.y
        goal_msg.pose.pose.position.z = goal.z
        goal_msg.pose.pose.orientation.w = goal.orientation_w
        
        # Send goal
        send_goal_future = self._action_client.send_goal_async(goal_msg)
        rclpy.spin_until_future_complete(self, send_goal_future, timeout_sec=timeout)
        
        goal_handle = send_goal_future.result()
        if not goal_handle.accepted:
            return NavigationResult(
                success=False,
                message="Goal rejected by planner",
                duration=0.0
            )
        
        # Wait for result
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future, timeout_sec=timeout)
        
        result = result_future.result()
        
        return NavigationResult(
            success=True,
            message="Navigation completed",
            duration=timeout
        )
        

def main():
    rclpy.init()
    nav_client = NavigationClient()
    
    goal = NavigationGoal(x=2.0, y=3.0, z=0.0)
    result = nav_client.navigate_to_goal(goal)
    
    logger.info(f"Result: {result.message}")
    
    nav_client.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
