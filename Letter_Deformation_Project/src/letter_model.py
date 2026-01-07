import numpy as np
import cv2
from skimage.morphology import dilation, square

class LetterSkeleton:
    def __init__(self, size=(200, 200)):
        self.h, self.w = size
        self.canvas = np.zeros((self.h, self.w), dtype=np.uint8)

    def clear(self):
        self.canvas.fill(0)

    def draw_line(self, p1, p2, thickness=1):
        # Convert points to integer tuples
        pt1 = (int(round(p1[0])), int(round(p1[1])))
        pt2 = (int(round(p2[0])), int(round(p2[1])))
        cv2.line(self.canvas, pt1, pt2, color=255, thickness=thickness, lineType=cv2.LINE_AA)

    def draw_curve(self, points=None, center=None, axes=None, angle=0, start_angle=0, end_angle=360, thickness=1):
        """
        A smart function that can draw both a list of points and complex ellipses
        depending on what base_letters sends it.
        """
        # Case 1: We received an ellipse definition
        if center is not None and axes is not None:
            # Convert to integers
            c = (int(round(center[0])), int(round(center[1])))
            ax = (int(round(axes[0])), int(round(axes[1])))
            
            cv2.ellipse(self.canvas, c, ax, angle, start_angle, end_angle, 255, thickness, cv2.LINE_AA)

        # Case 2: We received a regular list of points
        elif points is not None:
            pts = np.array(points, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(self.canvas, [pts], isClosed=False, color=255, thickness=thickness, lineType=cv2.LINE_AA)
            
    def apply_morphology(self, thickness=6):
        return dilation(self.canvas, square(thickness))