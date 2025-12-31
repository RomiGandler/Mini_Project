import numpy as np
import math

class CanonicalLetters:
    
    @staticmethod
    def _rotate_point(x, y, cx, cy, angle_deg):
        """פונקציית עזר לסיבוב נקודה סביב ציר"""
        rad = math.radians(angle_deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        dx = x - cx
        dy = y - cy
        
        new_x = cx + dx * cos_a - dy * sin_a
        new_y = cy + dx * sin_a + dy * cos_a
        
        return int(new_x), int(new_y)

    @staticmethod
    def draw_A(skeleton, top_width=0, crossbar_h_shift=0, base_width_factor=1.0):
        skeleton.clear()
        CANVAS_CENTER_X = 100
        DEFAULT_TOP_Y = 30
        DEFAULT_BOTTOM_Y = 170
        DEFAULT_BASE_WIDTH = 100
        
        target_base_width = int(DEFAULT_BASE_WIDTH * base_width_factor)
        current_base_width = max(20, min(195, target_base_width))  # הרחבנו טווח
        max_allowed_top = int(current_base_width * 1.5)  # שינוי: היה 0.8, עכשיו 1.5
        current_top_width = min(top_width, max_allowed_top)
        
        radius = current_top_width // 2
        current_top_y = DEFAULT_TOP_Y + radius
        current_bottom_y = DEFAULT_BOTTOM_Y
        
        top_left_x = CANVAS_CENTER_X - radius
        top_right_x = CANVAS_CENTER_X + radius
        bottom_left_x = CANVAS_CENTER_X - (current_base_width // 2)
        bottom_right_x = CANVAS_CENTER_X + (current_base_width // 2)
        
        mid_y_geometric = (current_top_y + current_bottom_y) / 2
        bar_y = int(mid_y_geometric + crossbar_h_shift)
        bar_y = max(int(current_top_y) + 5, min(current_bottom_y - 5, bar_y))  # הרחבנו טווח
        
        full_height = current_bottom_y - current_top_y
        if full_height == 0: full_height = 1
        ratio = (bar_y - current_top_y) / full_height
        
        bar_x_left = int(top_left_x + (bottom_left_x - top_left_x) * ratio)
        bar_x_right = int(top_right_x + (bottom_right_x - top_right_x) * ratio)
        
        skeleton.draw_line((int(bottom_left_x), current_bottom_y), (int(top_left_x), int(current_top_y)))
        skeleton.draw_line((int(bottom_right_x), current_bottom_y), (int(top_right_x), int(current_top_y)))
        skeleton.draw_line((bar_x_left, bar_y), (bar_x_right, bar_y))
        
        if current_top_width > 0:
            skeleton.draw_curve((CANVAS_CENTER_X, int(current_top_y)), (radius, radius), angle=0, start_angle=180, end_angle=360)

    @staticmethod
    def draw_B(skeleton, waist_y_shift=0, width_factor=1.0, rotation_deg=0):
        skeleton.clear()
        TOP_Y = 30
        BOTTOM_Y = 170
        LEFT_X = 50
        DEFAULT_WAIST_Y = 100
        DEFAULT_WIDTH_RADIUS = 40
        PIVOT_X, PIVOT_Y = 50, 100
        
        target_waist_y = DEFAULT_WAIST_Y + waist_y_shift
        waist_y = max(TOP_Y + 15, min(BOTTOM_Y - 15, target_waist_y))  # שינוי: היה 30, עכשיו 15
        target_radius_x = int(DEFAULT_WIDTH_RADIUS * width_factor)
        radius_x = max(10, min(120, target_radius_x))  # שינוי: היה 20-90, עכשיו 10-120
        
        # שינוי: הרחבנו את טווח הסיבוב
        safe_rotation = max(-40, min(40, rotation_deg))  # היה בלי הגבלה, עכשיו -40 עד 40
        
        p_top = CanonicalLetters._rotate_point(LEFT_X, TOP_Y, PIVOT_X, PIVOT_Y, safe_rotation)
        p_bottom = CanonicalLetters._rotate_point(LEFT_X, BOTTOM_Y, PIVOT_X, PIVOT_Y, safe_rotation)
        skeleton.draw_line(p_top, p_bottom)
        
        top_height = waist_y - TOP_Y
        top_center_y = TOP_Y + (top_height // 2)
        top_radius_y = top_height // 2
        p_top_center = CanonicalLetters._rotate_point(LEFT_X, top_center_y, PIVOT_X, PIVOT_Y, safe_rotation)
        
        skeleton.draw_curve(center=p_top_center, axes=(radius_x, int(top_radius_y)), angle=safe_rotation, start_angle=-90, end_angle=90)
        
        bottom_height = BOTTOM_Y - waist_y
        bottom_center_y = waist_y + (bottom_height // 2)
        bottom_radius_y = bottom_height // 2
        p_bottom_center = CanonicalLetters._rotate_point(LEFT_X, bottom_center_y, PIVOT_X, PIVOT_Y, safe_rotation)
        
        skeleton.draw_curve(center=p_bottom_center, axes=(radius_x, int(bottom_radius_y)), angle=safe_rotation, start_angle=-90, end_angle=90)

    @staticmethod
    def draw_C(skeleton, rotation_deg=0, cut_top=0, cut_bottom=0, elongation_factor=1.0):
        skeleton.clear()
        CENTER_X = 110
        CENTER_Y = 100
        BASE_RADIUS = 75 
        
        base_start = 45
        base_end = 315
        
        safe_cut_top = max(-50, min(120, cut_top))  # שינוי: היה -40 עד 100
        safe_cut_bottom = max(-50, min(120, cut_bottom))  # שינוי: היה -40 עד 100
        
        current_start = base_start + safe_cut_bottom
        current_end = base_end - safe_cut_top
        
        if current_end <= current_start:
             current_end = current_start + 10

        radius_y = BASE_RADIUS
        radius_x = int(BASE_RADIUS * elongation_factor)
        radius_x = max(20, min(150, radius_x))  # שינוי: היה 30-110, עכשיו 20-150
        safe_rotation = max(-80, min(80, rotation_deg))  # שינוי: היה -30 עד 30, עכשיו -80 עד 80
        
        skeleton.draw_curve(
            center=(CENTER_X, CENTER_Y),
            axes=(radius_x, radius_y),
            angle=safe_rotation,
            start_angle=current_start,
            end_angle=current_end
        )