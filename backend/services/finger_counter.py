# Finger Counter Service
# services/finger_counter.py
# Compatible with mediapipe >= 0.10.x on Windows

import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class FingerCounter:
    def __init__(self):
        base_options = python.BaseOptions(
            model_asset_path=self._get_model_path()
        )
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=2,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

        self.finger_tips  = [4, 8, 12, 16, 20]
        self.finger_pips  = [3, 6, 10, 14, 18]
        self.finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']

    # ------------------------------------------------------------------
    def _get_model_path(self):
        """Download hand_landmarker.task if missing and return its path."""
        import os, urllib.request

        model_dir  = os.path.join(os.path.dirname(__file__), '..', 'models')
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, 'hand_landmarker.task')

        if not os.path.exists(model_path):
            print("Downloading hand_landmarker.task (~5 MB) ...")
            url = (
                "https://storage.googleapis.com/mediapipe-models/"
                "hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
            )
            urllib.request.urlretrieve(url, model_path)
            print("hand_landmarker.task downloaded!")

        return model_path

    # ------------------------------------------------------------------
    def count_fingers(self, image):
        """Count raised fingers in a BGR image. Returns dict with results."""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image  = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)

        detection_result = self.detector.detect(mp_image)

        if not detection_result.hand_landmarks:
            return {
                'hands_detected': 0,
                'total_fingers' : 0,
                'hands'         : []
            }

        hands_data    = []
        total_fingers = 0

        for idx, hand_lm in enumerate(detection_result.hand_landmarks):
            handedness = (
                detection_result.handedness[idx][0].display_name
                if detection_result.handedness else "Unknown"
            )

            fingers_up   = self._count_fingers_for_hand(hand_lm)
            finger_count = sum(fingers_up)
            total_fingers += finger_count
            raised = [n for n, up in zip(self.finger_names, fingers_up) if up]

            hands_data.append({
                'hand'          : handedness,
                'fingers_up'    : finger_count,
                'raised_fingers': raised,
                'finger_status' : {
                    n: bool(up)
                    for n, up in zip(self.finger_names, fingers_up)
                }
            })

        return {
            'hands_detected': len(detection_result.hand_landmarks),
            'total_fingers' : total_fingers,
            'hands'         : hands_data
        }

    # ------------------------------------------------------------------
    def _count_fingers_for_hand(self, landmarks):
        """Returns list of 5 booleans — True if finger is raised."""
        fingers_up = []

        # Thumb: horizontal distance from wrist
        palm_x = landmarks[0].x
        fingers_up.append(
            abs(landmarks[4].x - palm_x) > abs(landmarks[3].x - palm_x)
        )

        # Other four fingers: tip y above pip y = finger is up
        for tip_idx, pip_idx in zip(self.finger_tips[1:], self.finger_pips[1:]):
            fingers_up.append(landmarks[tip_idx].y < landmarks[pip_idx].y)

        return fingers_up

    # ------------------------------------------------------------------
    def draw_results(self, image, results):
        """Draw finger count text on image. No landmark drawing (Windows safe)."""
        if results.get('hands_detected', 0) == 0:
            return image

        image_copy = image.copy()

        # Draw total count
        cv2.putText(
            image_copy,
            f"Fingers: {results['total_fingers']}",
            (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3
        )

        # Draw per-hand info
        y = 100
        for hand_data in results['hands']:
            cv2.putText(
                image_copy,
                f"{hand_data['hand']}: {hand_data['fingers_up']} fingers",
                (10, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
            )
            y += 40

        return image_copy

    # ------------------------------------------------------------------
    def process_video_frame(self, frame):
        results         = self.count_fingers(frame)
        annotated_frame = self.draw_results(frame, results)
        return results, annotated_frame

    # ------------------------------------------------------------------
    def __del__(self):
        if hasattr(self, 'detector'):
            try:
                self.detector.close()
            except Exception:
                pass
