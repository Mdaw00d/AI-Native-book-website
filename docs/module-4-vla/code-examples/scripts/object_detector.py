#!/usr/bin/env python3
"""
Object Detection Module for VLA Integration

This module provides object detection and 3D pose estimation using YOLOv8
for the VLA pipeline. It processes RGB-D images to detect objects and
compute their 3D positions in the robot's coordinate frame.

Requirements:
    - ultralytics: YOLOv8 object detection
    - opencv-python: Image processing
    - numpy: Numerical computations

Usage:
    from object_detector import ObjectDetector

    detector = ObjectDetector(model_size="n")
    detections = detector.detect_objects(rgb_image, depth_image)
    for det in detections:
        print(f"{det.class_name}: {det.confidence:.2f} at {det.position_3d}")
"""

import cv2
import numpy as np
from ultralytics import YOLO
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class BoundingBox:
    """2D bounding box in image coordinates"""
    x1: int  # Top-left x
    y1: int  # Top-left y
    x2: int  # Bottom-right x
    y2: int  # Bottom-right y

    @property
    def width(self) -> int:
        return self.x2 - self.x1

    @property
    def height(self) -> int:
        return self.y2 - self.y1

    @property
    def center(self) -> Tuple[int, int]:
        return ((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)

    @property
    def area(self) -> int:
        return self.width * self.height


@dataclass
class Detection:
    """Object detection result with 3D pose"""
    class_id: int
    class_name: str
    confidence: float
    bbox: BoundingBox
    position_3d: Optional[Tuple[float, float, float]] = None  # (x, y, z) in meters
    depth_confidence: float = 0.0  # Confidence in depth measurement


@dataclass
class CameraIntrinsics:
    """Camera intrinsic parameters for depth projection"""
    fx: float  # Focal length x
    fy: float  # Focal length y
    cx: float  # Principal point x
    cy: float  # Principal point y
    width: int
    height: int


class ObjectDetector:
    """
    Object detector using YOLOv8 with 3D pose estimation from RGB-D data.

    This class handles:
    - Object detection in RGB images using YOLOv8
    - 3D position estimation using depth maps
    - Confidence thresholding and filtering
    - NMS (Non-Maximum Suppression) for overlapping detections

    Attributes:
        model_size (str): YOLOv8 model size (n, s, m, l, x)
        confidence_threshold (float): Minimum confidence for detections
        iou_threshold (float): IoU threshold for NMS
        model (YOLO): Loaded YOLOv8 model
        camera_intrinsics (CameraIntrinsics): Camera parameters for 3D projection
    """

    def __init__(
        self,
        model_size: str = "n",
        confidence_threshold: float = 0.5,
        iou_threshold: float = 0.45,
        camera_intrinsics: Optional[CameraIntrinsics] = None,
        device: Optional[str] = None
    ):
        """
        Initialize object detector.

        Args:
            model_size: YOLOv8 model size (n=nano, s=small, m=medium, l=large, x=xlarge)
            confidence_threshold: Minimum confidence score (0-1)
            iou_threshold: IoU threshold for NMS
            camera_intrinsics: Camera parameters (uses default if None)
            device: Device for inference (cpu, cuda, mps)
        """
        self.model_size = model_size
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        self.device = device or 'cpu'

        # Default camera intrinsics (typical RGB-D camera)
        self.camera_intrinsics = camera_intrinsics or CameraIntrinsics(
            fx=525.0,  # Focal length x (pixels)
            fy=525.0,  # Focal length y (pixels)
            cx=319.5,  # Principal point x
            cy=239.5,  # Principal point y
            width=640,
            height=480
        )

        # Load YOLOv8 model
        model_name = f"yolov8{model_size}.pt"
        logger.info(f"Loading YOLOv8 model: {model_name}")

        try:
            self.model = YOLO(model_name)
            logger.info(f"YOLOv8{model_size} loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load YOLOv8 model: {e}")
            raise

        # COCO class names (80 classes)
        self.class_names = self.model.names

    def detect_objects(
        self,
        rgb_image: np.ndarray,
        depth_image: Optional[np.ndarray] = None,
        target_classes: Optional[List[str]] = None
    ) -> List[Detection]:
        """
        Detect objects in RGB image and estimate 3D positions from depth.

        Args:
            rgb_image: RGB image (H, W, 3) as numpy array
            depth_image: Depth image (H, W) in meters (optional)
            target_classes: Filter detections to specific class names (optional)

        Returns:
            List of Detection objects with bounding boxes and 3D positions
        """
        logger.info(f"Running object detection on image shape {rgb_image.shape}")

        # Run YOLOv8 inference
        results = self.model(
            rgb_image,
            conf=self.confidence_threshold,
            iou=self.iou_threshold,
            verbose=False
        )

        detections = []

        # Process results
        for result in results:
            boxes = result.boxes

            for i in range(len(boxes)):
                # Extract box data
                box = boxes.xyxy[i].cpu().numpy()  # [x1, y1, x2, y2]
                conf = float(boxes.conf[i].cpu().numpy())
                cls_id = int(boxes.cls[i].cpu().numpy())
                cls_name = self.class_names[cls_id]

                # Filter by target classes if specified
                if target_classes and cls_name not in target_classes:
                    continue

                # Create bounding box
                bbox = BoundingBox(
                    x1=int(box[0]),
                    y1=int(box[1]),
                    x2=int(box[2]),
                    y2=int(box[3])
                )

                # Estimate 3D position if depth available
                position_3d = None
                depth_conf = 0.0

                if depth_image is not None:
                    position_3d, depth_conf = self._estimate_3d_position(
                        bbox, depth_image
                    )

                detection = Detection(
                    class_id=cls_id,
                    class_name=cls_name,
                    confidence=conf,
                    bbox=bbox,
                    position_3d=position_3d,
                    depth_confidence=depth_conf
                )

                detections.append(detection)

        logger.info(f"Detected {len(detections)} objects")
        return detections

    def _estimate_3d_position(
        self,
        bbox: BoundingBox,
        depth_image: np.ndarray
    ) -> Tuple[Optional[Tuple[float, float, float]], float]:
        """
        Estimate 3D position of detected object from depth map.

        Args:
            bbox: 2D bounding box of detected object
            depth_image: Depth image in meters

        Returns:
            Tuple of (position_3d, confidence)
            position_3d: (x, y, z) in meters in camera frame, or None if invalid
            confidence: Depth measurement confidence (0-1)
        """
        # Extract depth region within bounding box
        y1, y2 = max(0, bbox.y1), min(depth_image.shape[0], bbox.y2)
        x1, x2 = max(0, bbox.x1), min(depth_image.shape[1], bbox.x2)

        if x2 <= x1 or y2 <= y1:
            return None, 0.0

        depth_roi = depth_image[y1:y2, x1:x2]

        # Filter invalid depth values (0 or NaN)
        valid_depths = depth_roi[(depth_roi > 0) & (~np.isnan(depth_roi))]

        if len(valid_depths) == 0:
            logger.warning(f"No valid depth values in bounding box")
            return None, 0.0

        # Use median depth (more robust to outliers than mean)
        depth_z = float(np.median(valid_depths))

        # Calculate confidence based on depth variance
        depth_std = float(np.std(valid_depths))
        depth_conf = 1.0 / (1.0 + depth_std)  # Higher variance = lower confidence

        # Get center point of bounding box
        cx, cy = bbox.center

        # Project to 3D using camera intrinsics
        # Standard pinhole camera model:
        # X = (u - cx) * Z / fx
        # Y = (v - cy) * Z / fy
        # Z = depth

        x_3d = (cx - self.camera_intrinsics.cx) * depth_z / self.camera_intrinsics.fx
        y_3d = (cy - self.camera_intrinsics.cy) * depth_z / self.camera_intrinsics.fy
        z_3d = depth_z

        logger.debug(f"3D position: ({x_3d:.2f}, {y_3d:.2f}, {z_3d:.2f}), conf: {depth_conf:.2f}")

        return (x_3d, y_3d, z_3d), depth_conf

    def draw_detections(
        self,
        image: np.ndarray,
        detections: List[Detection],
        show_3d: bool = True
    ) -> np.ndarray:
        """
        Draw bounding boxes and labels on image.

        Args:
            image: Input image to draw on (will be copied)
            detections: List of Detection objects
            show_3d: Show 3D position in label if available

        Returns:
            Image with drawn detections
        """
        output = image.copy()

        for det in detections:
            bbox = det.bbox

            # Choose color based on class (deterministic from class_id)
            np.random.seed(det.class_id)
            color = tuple(np.random.randint(0, 255, 3).tolist())

            # Draw bounding box
            cv2.rectangle(
                output,
                (bbox.x1, bbox.y1),
                (bbox.x2, bbox.y2),
                color,
                2
            )

            # Prepare label
            label = f"{det.class_name}: {det.confidence:.2f}"

            if show_3d and det.position_3d:
                x, y, z = det.position_3d
                label += f" | ({x:.2f}, {y:.2f}, {z:.2f})m"

            # Draw label background
            (text_width, text_height), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
            )

            cv2.rectangle(
                output,
                (bbox.x1, bbox.y1 - text_height - 5),
                (bbox.x1 + text_width, bbox.y1),
                color,
                -1
            )

            # Draw label text
            cv2.putText(
                output,
                label,
                (bbox.x1, bbox.y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )

        return output

    def detect_and_visualize(
        self,
        rgb_image: np.ndarray,
        depth_image: Optional[np.ndarray] = None,
        save_path: Optional[Path] = None
    ) -> Tuple[List[Detection], np.ndarray]:
        """
        Detect objects and return visualization.

        Args:
            rgb_image: RGB image
            depth_image: Depth image (optional)
            save_path: Path to save visualization (optional)

        Returns:
            Tuple of (detections, annotated_image)
        """
        detections = self.detect_objects(rgb_image, depth_image)
        annotated = self.draw_detections(rgb_image, detections, show_3d=(depth_image is not None))

        if save_path:
            cv2.imwrite(str(save_path), cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR))
            logger.info(f"Saved visualization to {save_path}")

        return detections, annotated

    def filter_by_confidence(
        self,
        detections: List[Detection],
        min_confidence: float
    ) -> List[Detection]:
        """
        Filter detections by minimum confidence threshold.

        Args:
            detections: List of detections
            min_confidence: Minimum confidence (0-1)

        Returns:
            Filtered list of detections
        """
        return [d for d in detections if d.confidence >= min_confidence]

    def filter_by_depth_range(
        self,
        detections: List[Detection],
        min_depth: float = 0.0,
        max_depth: float = 10.0
    ) -> List[Detection]:
        """
        Filter detections by depth range.

        Args:
            detections: List of detections
            min_depth: Minimum depth in meters
            max_depth: Maximum depth in meters

        Returns:
            Filtered list of detections
        """
        filtered = []
        for det in detections:
            if det.position_3d:
                _, _, z = det.position_3d
                if min_depth <= z <= max_depth:
                    filtered.append(det)
        return filtered

    def get_closest_detection(
        self,
        detections: List[Detection],
        target_class: Optional[str] = None
    ) -> Optional[Detection]:
        """
        Get closest detection to camera.

        Args:
            detections: List of detections
            target_class: Filter by class name (optional)

        Returns:
            Closest detection or None
        """
        # Filter by class if specified
        if target_class:
            detections = [d for d in detections if d.class_name == target_class]

        if not detections:
            return None

        # Filter detections with valid 3D positions
        valid = [d for d in detections if d.position_3d]

        if not valid:
            return None

        # Find closest by Z distance
        return min(valid, key=lambda d: d.position_3d[2])


def main():
    """
    Example usage and testing of ObjectDetector.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Object Detection for VLA Pipeline")
    parser.add_argument(
        '--model',
        default='n',
        choices=['n', 's', 'm', 'l', 'x'],
        help='YOLOv8 model size'
    )
    parser.add_argument(
        '--image',
        type=Path,
        required=True,
        help='Path to RGB image'
    )
    parser.add_argument(
        '--depth',
        type=Path,
        help='Path to depth image (optional)'
    )
    parser.add_argument(
        '--conf',
        type=float,
        default=0.5,
        help='Confidence threshold'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Path to save annotated image'
    )
    parser.add_argument(
        '--classes',
        nargs='+',
        help='Filter by class names (e.g., person cup bottle)'
    )

    args = parser.parse_args()

    # Load images
    logger.info(f"Loading RGB image: {args.image}")
    rgb_image = cv2.imread(str(args.image))
    rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB)

    depth_image = None
    if args.depth:
        logger.info(f"Loading depth image: {args.depth}")
        # Assume depth is stored as 16-bit PNG (millimeters)
        depth_image = cv2.imread(str(args.depth), cv2.IMREAD_UNCHANGED)
        depth_image = depth_image.astype(np.float32) / 1000.0  # Convert to meters

    # Initialize detector
    detector = ObjectDetector(
        model_size=args.model,
        confidence_threshold=args.conf
    )

    # Detect and visualize
    detections, annotated = detector.detect_and_visualize(
        rgb_image,
        depth_image,
        save_path=args.output
    )

    # Print results
    print("\n" + "="*60)
    print("Detection Results")
    print("="*60)

    for i, det in enumerate(detections, 1):
        print(f"\n{i}. {det.class_name}")
        print(f"   Confidence: {det.confidence:.2%}")
        print(f"   BBox: ({det.bbox.x1}, {det.bbox.y1}) - ({det.bbox.x2}, {det.bbox.y2})")
        if det.position_3d:
            x, y, z = det.position_3d
            print(f"   3D Position: ({x:.2f}, {y:.2f}, {z:.2f}) meters")
            print(f"   Depth Confidence: {det.depth_confidence:.2f}")

    print("\n" + "="*60)
    print(f"Total detections: {len(detections)}")

    if detections and detections[0].position_3d:
        closest = detector.get_closest_detection(detections)
        if closest:
            print(f"Closest object: {closest.class_name} at {closest.position_3d[2]:.2f}m")


if __name__ == "__main__":
    main()
