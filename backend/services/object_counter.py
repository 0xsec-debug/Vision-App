# Object Counter Service
# services/object_counter.py

import cv2
import numpy as np

class ObjectCounter:
    def __init__(self):
        self.min_contour_area = 500  # Minimum area to be considered an object
        
    def count_objects(self, image, method='contour'):
        """
        Count objects in image using different methods
        
        Methods:
        - 'contour': Uses contour detection (good for distinct objects)
        - 'blob': Uses blob detection (good for circular objects)
        - 'template': Uses template matching (for specific objects)
        """
        if method == 'contour':
            return self._count_by_contours(image)
        elif method == 'blob':
            return self._count_by_blobs(image)
        else:
            return self._count_by_contours(image)
    
    def _count_by_contours(self, image):
        """
        Count objects using contour detection
        Works well for counting distinct objects like fingers, coins, etc.
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11, 2
        )
        
        # Morphological operations to clean up
        kernel = np.ones((3, 3), np.uint8)
        morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
        morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel, iterations=1)
        
        # Find contours
        contours, _ = cv2.findContours(
            morph,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Filter contours by area
        valid_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > self.min_contour_area:
                # Get bounding box
                x, y, w, h = cv2.boundingRect(contour)
                
                # Calculate properties
                perimeter = cv2.arcLength(contour, True)
                circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
                
                valid_contours.append({
                    'bbox': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)},
                    'area': float(area),
                    'circularity': float(circularity),
                    'contour': contour
                })
        
        return {
            'count': len(valid_contours),
            'method': 'contour',
            'objects': valid_contours
        }
    
    def _count_by_blobs(self, image):
        """
        Count objects using blob detection
        Works well for circular objects
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Setup SimpleBlobDetector parameters
        params = cv2.SimpleBlobDetector_Params()
        
        # Filter by Area
        params.filterByArea = True
        params.minArea = self.min_contour_area
        params.maxArea = 100000
        
        # Filter by Circularity
        params.filterByCircularity = True
        params.minCircularity = 0.1
        
        # Filter by Convexity
        params.filterByConvexity = True
        params.minConvexity = 0.5
        
        # Filter by Inertia
        params.filterByInertia = True
        params.minInertiaRatio = 0.01
        
        # Create detector
        detector = cv2.SimpleBlobDetector_create(params)
        
        # Detect blobs
        keypoints = detector.detect(gray)
        
        # Extract blob info
        objects = []
        for kp in keypoints:
            objects.append({
                'center': {'x': float(kp.pt[0]), 'y': float(kp.pt[1])},
                'size': float(kp.size),
                'response': float(kp.response)
            })
        
        return {
            'count': len(keypoints),
            'method': 'blob',
            'objects': objects
        }
    
    def count_specific_color_objects(self, image, color_range):
        """
        Count objects of a specific color range
        
        color_range: dict with 'lower' and 'upper' HSV values
        Example: {'lower': [0, 50, 50], 'upper': [10, 255, 255]} for red
        """
        # Convert to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Create mask
        lower = np.array(color_range['lower'])
        upper = np.array(color_range['upper'])
        mask = cv2.inRange(hsv, lower, upper)
        
        # Apply morphological operations
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter by area
        valid_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > self.min_contour_area:
                x, y, w, h = cv2.boundingRect(contour)
                valid_contours.append({
                    'bbox': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)},
                    'area': float(area),
                    'contour': contour
                })
        
        return {
            'count': len(valid_contours),
            'method': 'color_detection',
            'objects': valid_contours
        }
    
    def draw_results(self, image, results):
        """Draw detected objects on image"""
        if results['count'] == 0:
            return image
        
        image_copy = image.copy()
        
        if results['method'] == 'contour' or results['method'] == 'color_detection':
            for obj in results['objects']:
                bbox = obj['bbox']
                # Draw rectangle
                cv2.rectangle(
                    image_copy,
                    (bbox['x'], bbox['y']),
                    (bbox['x'] + bbox['width'], bbox['y'] + bbox['height']),
                    (0, 255, 0),
                    2
                )
                # Draw area
                cv2.putText(
                    image_copy,
                    f"Area: {int(obj['area'])}",
                    (bbox['x'], bbox['y'] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    1
                )
        
        elif results['method'] == 'blob':
            for obj in results['objects']:
                center = obj['center']
                size = obj['size']
                # Draw circle
                cv2.circle(
                    image_copy,
                    (int(center['x']), int(center['y'])),
                    int(size),
                    (0, 255, 0),
                    2
                )
        
        # Draw total count
        cv2.putText(
            image_copy,
            f"Objects: {results['count']}",
            (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 255, 0),
            3
        )
        
        return image_copy
    
    def analyze_image(self, image):
        """
        Comprehensive analysis of image
        Tries multiple methods and returns best result
        """
        # Try contour detection
        contour_result = self._count_by_contours(image)
        
        # Try blob detection
        blob_result = self._count_by_blobs(image)
        
        # Choose best result (more objects detected)
        if contour_result['count'] >= blob_result['count']:
            return contour_result
        else:
            return blob_result


# Predefined color ranges for common objects
COLOR_RANGES = {
    'red': {
        'lower': [0, 50, 50],
        'upper': [10, 255, 255]
    },
    'green': {
        'lower': [40, 40, 40],
        'upper': [80, 255, 255]
    },
    'blue': {
        'lower': [100, 50, 50],
        'upper': [130, 255, 255]
    },
    'yellow': {
        'lower': [20, 100, 100],
        'upper': [30, 255, 255]
    },
    'orange': {
        'lower': [10, 100, 100],
        'upper': [20, 255, 255]
    }
}
