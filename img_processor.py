import cv2
import numpy as np


class ImageProcessor:
    def __init__(self):
        self._original_image = None
        self._current_image = None
        self._history = []
        self._history_index = -1

    def load_image(self, filepath):
        try:
            image = cv2.imread(filepath)
            if image is None:
                return False
            self._original_image = image.copy()
            self._current_image = image.copy()
            self._history = [image.copy()]
            self._history_index = 0
            return True
        except Exception:
            return False

    def save_image(self, filepath):
        try:
            if self._current_image is None:
                return False
            success = cv2.imwrite(filepath, self._current_image)
            return success
        except Exception:
            return False

    def get_current_image(self):
        if self._current_image is None:
            return None
        return self._current_image.copy()

    def get_image_info(self):
        if self._current_image is None:
            return {"width": 0, "height": 0, "channels": 0}
        height, width = self._current_image.shape[:2]
        channels = 3 if len(self._current_image.shape) == 3 else 1
        return {"width": width, "height": height, "channels": channels}

    def _add_to_history(self, image):
        self._history = self._history[:self._history_index + 1]
        self._history.append(image.copy())
        self._history_index += 1
        if len(self._history) > 20:
            self._history.pop(0)
            self._history_index -= 1

    def undo(self):
        if self._history_index > 0:
            self._history_index -= 1
            self._current_image = self._history[self._history_index].copy()
            return True
        else:
            return False

    def redo(self):
        if self._history_index < len(self._history) - 1:
            self._history_index += 1
            self._current_image = self._history[self._history_index].copy()
            return True
        else:
            return False

    def reset_to_original(self):
        if self._original_image is not None:
            self._current_image = self._original_image.copy()
            self._add_to_history(self._current_image)

    def convert_to_grayscale(self):
        if self._current_image is None:
            return
        gray = cv2.cvtColor(self._current_image, cv2.COLOR_BGR2GRAY)
        self._current_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        self._add_to_history(self._current_image)

    def apply_blur(self, intensity=5):
        if self._current_image is None:
            return
        intensity = max(1, intensity)
        if intensity % 2 == 0:
            intensity += 1
        blurred = cv2.GaussianBlur(self._current_image, (intensity, intensity), 0)
        self._current_image = blurred
        self._add_to_history(self._current_image)

    def detect_edges(self):
        if self._current_image is None:
            return
        gray = cv2.cvtColor(self._current_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        self._current_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        self._add_to_history(self._current_image)

    def adjust_brightness(self, value):
        if self._current_image is None:
            return
        value = max(-100, min(100, value))
        adjusted = cv2.convertScaleAbs(self._current_image, alpha=1, beta=value)
        self._current_image = adjusted
        self._add_to_history(self._current_image)

    def adjust_contrast(self, value):
        if self._current_image is None:
            return
        value = max(0.5, min(3.0, value))
        adjusted = cv2.convertScaleAbs(self._current_image, alpha=value, beta=0)
        self._current_image = adjusted
        self._add_to_history(self._current_image)

    def rotate_image(self, angle):
        if self._current_image is None:
            return
        if angle == 90:
            rotated = cv2.rotate(self._current_image, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            rotated = cv2.rotate(self._current_image, cv2.ROTATE_180)
        elif angle == 270:
            rotated = cv2.rotate(self._current_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            return
        self._current_image = rotated
        self._add_to_history(self._current_image)

    def flip_image(self, direction):
        if self._current_image is None:
            return
        if direction == 'horizontal':
            flipped = cv2.flip(self._current_image, 1)
        elif direction == 'vertical':
            flipped = cv2.flip(self._current_image, 0)
        else:
            return
        self._current_image = flipped
        self._add_to_history(self._current_image)

    def resize_image(self, width, height):
        if self._current_image is None:
            return
        if width <= 0 or height <= 0:
            return
        resized = cv2.resize(self._current_image, (width, height))
        self._current_image = resized
        self._add_to_history(self._current_image)

    def scale_image(self, percent):
        if self._current_image is None:
            return
        percent = max(25, min(200, percent))
        height, width = self._current_image.shape[:2]
        new_width = int(width * percent / 100)
        new_height = int(height * percent / 100)
        self.resize_image(new_width, new_height)