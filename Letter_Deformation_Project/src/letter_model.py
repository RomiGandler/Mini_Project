import numpy as np
import cv2

class LetterSkeleton:
    def __init__(self, size=(200, 200)):
        """
        מאתחל את משטח הציור (קנבס) בגודל נתון.
        """
        self.h, self.w = size
        self.canvas = np.zeros((self.h, self.w), dtype=np.uint8)
    
    def clear(self):
        """מנקה את המשטח (מוחק הכל ומשאיר שחור)."""
        self.canvas = np.zeros((self.h, self.w), dtype=np.uint8)

    def draw_line(self, p1, p2):
        """
        מצייר קו דק (שלד) בין שתי נקודות.
        p1, p2: (x, y) tuples
        """
        # thickness=1 כי זה השלד
        cv2.line(self.canvas, p1, p2, color=255, thickness=1, lineType=cv2.LINE_AA)

    def draw_curve(self, center, axes, angle=0, start_angle=0, end_angle=360):
        """
        מצייר קשת (חלק מאליפסה) עבור אותיות עגולות כמו B ו-C.
        center: (x, y) מרכז האליפסה
        axes: (radius_x, radius_y) חצי רוחב וחצי גובה
        """
        cv2.ellipse(self.canvas, center, axes, angle, start_angle, end_angle, color=255, thickness=1, lineType=cv2.LINE_AA)

    def get_skeleton(self):
        """מחזיר את תמונת השלד הנוכחית (לפני עיבוי)."""
        return self.canvas.copy()

    def apply_morphology(self, thickness=5):
        """
        מבצע פעולת Dilation כדי לעבות את השלד ולהפוך אותו לצורה מלאה.
        """
        kernel = np.ones((thickness, thickness), np.uint8)
        thickened_image = cv2.dilate(self.canvas, kernel, iterations=1)
        return thickened_image