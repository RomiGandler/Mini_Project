import numpy as np
import math

class CanonicalLetters:
    
    @staticmethod
    def _rotate_point(x, y, cx, cy, angle_deg):
        """Rotates a point around a center point by a given angle."""
        rad = math.radians(angle_deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        dx = x - cx
        dy = y - cy
        
        new_x = cx + dx * cos_a - dy * sin_a
        new_y = cy + dx * sin_a + dy * cos_a
        
        return int(new_x), int(new_y)

    @staticmethod
    def draw_A(skeleton, top_width=0, crossbar_h_shift=0, base_width_factor=1.0, shear_x=0, thickness=6, **kwargs):
        skeleton.clear()

        # === 1. Calculate Dynamic Center ===
        CANVAS_CENTER_X = 100 - (int(shear_x) // 2)
        
        TOP_Y = 40
        BOTTOM_Y = 175
        HEIGHT = BOTTOM_Y - TOP_Y
        DEFAULT_BASE_WIDTH = 100
        
        current_base_width = int(DEFAULT_BASE_WIDTH * base_width_factor)
        current_top_width = int(top_width)
        
        base_left_x = CANVAS_CENTER_X - (current_base_width // 2)
        base_right_x = CANVAS_CENTER_X + (current_base_width // 2)
        
        top_left_x = CANVAS_CENTER_X - (current_top_width // 2)
        top_right_x = CANVAS_CENTER_X + (current_top_width // 2)

        # === 2. Shear Function ===
        def apply_shear_and_clamp(x, y):
            factor = (BOTTOM_Y - y) / HEIGHT if HEIGHT != 0 else 0
            shifted_x = x + int(shear_x * factor)
            clamped_x = max(5, min(195, shifted_x))
            return clamped_x, y

        p_base_left = apply_shear_and_clamp(base_left_x, BOTTOM_Y)
        p_base_right = apply_shear_and_clamp(base_right_x, BOTTOM_Y)
        p_top_left = apply_shear_and_clamp(top_left_x, TOP_Y)
        p_top_right = apply_shear_and_clamp(top_right_x, TOP_Y)
        
        skeleton.draw_line(p_base_left, p_top_left, thickness)
        skeleton.draw_line(p_base_right, p_top_right, thickness)
        
        if current_top_width > 0:
            skeleton.draw_line(p_top_left, p_top_right, thickness)

        # === 3. Calculate Crossbar ===
        bar_y_base = (TOP_Y + BOTTOM_Y) // 2 + 10
        raw_bar_y = bar_y_base - int(crossbar_h_shift)
        
        sharpness_penalty = 20 if current_top_width < 20 else 0
        safe_distance_from_top = int(thickness * 1.5) + 10 + sharpness_penalty
        min_allowed_y = TOP_Y + safe_distance_from_top
        
        bar_y = max(raw_bar_y, min_allowed_y)
        max_allowed_y = BOTTOM_Y - 25
        bar_y = min(bar_y, max_allowed_y)

        # Calculate Crossbar
        if p_base_left[0] == p_top_left[0]:
             bar_x_left = p_base_left[0]
        else:
             m = (p_base_left[1] - p_top_left[1]) / (p_base_left[0] - p_top_left[0])
             bar_x_left = (bar_y - p_top_left[1]) / m + p_top_left[0]

        if p_base_right[0] == p_top_right[0]:
             bar_x_right = p_base_right[0]
        else:
             m = (p_base_right[1] - p_top_right[1]) / (p_base_right[0] - p_top_right[0])
             bar_x_right = (bar_y - p_top_right[1]) / m + p_top_right[0]
        
        skeleton.draw_line((int(bar_x_left), int(bar_y)), (int(bar_x_right), int(bar_y)), thickness)

    @staticmethod
    def draw_B(skeleton, width_factor=1.0, waist_y_shift=0, rotation_deg=0, vertical_squash=1.0, thickness=6, **kwargs):
        skeleton.clear()
        
        LEFT_X = 60
        TOP_Y = 30
        BOTTOM_Y = 170
        WAIST_Y_DEFAULT = 100
        WIDTH_DEFAULT = 70
        CENTER_Y_CANVAS = 100
        
        def squash_y(y):
            dy = y - CENTER_Y_CANVAS
            return int(CENTER_Y_CANVAS + dy * vertical_squash)
            
        current_top_y = squash_y(TOP_Y)
        current_bottom_y = squash_y(BOTTOM_Y)
        current_waist_y = squash_y(WAIST_Y_DEFAULT - int(waist_y_shift))
        current_width = int(WIDTH_DEFAULT * width_factor)
        
        top_left = (LEFT_X, current_top_y)
        bottom_left = (LEFT_X, current_bottom_y)
        
        p1 = CanonicalLetters._rotate_point(*top_left, 100, 100, rotation_deg)
        p2 = CanonicalLetters._rotate_point(*bottom_left, 100, 100, rotation_deg)
        skeleton.draw_line(p1, p2, thickness)
        
        top_height = abs(current_waist_y - current_top_y)
        top_radius_y = top_height // 2
        top_center_y = min(current_top_y, current_waist_y) + top_radius_y
        p_top_center = CanonicalLetters._rotate_point(LEFT_X, top_center_y, 100, 100, rotation_deg)
        
        skeleton.draw_curve(
            center=p_top_center, 
            axes=(current_width, int(top_radius_y)), 
            angle=rotation_deg, 
            start_angle=-90, 
            end_angle=90,
            thickness=thickness
        )
        
        # Lower Loop
        bottom_height = abs(current_bottom_y - current_waist_y)
        bottom_radius_y = bottom_height // 2
        bottom_center_y = min(current_waist_y, current_bottom_y) + bottom_radius_y
        p_bottom_center = CanonicalLetters._rotate_point(LEFT_X, bottom_center_y, 100, 100, rotation_deg)
        
        skeleton.draw_curve(
            center=p_bottom_center, 
            axes=(current_width, int(bottom_radius_y)), 
            angle=rotation_deg, 
            start_angle=-90, 
            end_angle=90,
            thickness=thickness
        )

    @staticmethod
    def draw_C(skeleton, rotation_deg=0, cut_top=0, cut_bottom=0, vertical_squash=1.0, thickness=6, **kwargs):
        skeleton.clear()
        CENTER_X = 110
        CENTER_Y = 100
        BASE_RADIUS = 75 
        
        radius_x = BASE_RADIUS
        radius_y = int(BASE_RADIUS * vertical_squash)
        
        base_start = 45
        base_end = 315
        
        safe_cut_top = max(-50, min(120, cut_top))
        
        current_start = base_start # safe_cut_bottom
        current_end = base_end - safe_cut_top
        
        if current_end <= current_start:
             current_end = current_start + 10

        skeleton.draw_curve(
            center=(CENTER_X, CENTER_Y),
            axes=(radius_x, radius_y),
            angle=rotation_deg,
            start_angle=current_start,
            end_angle=current_end,
            thickness=thickness
        )