import numpy as np
import math

class CanonicalLetters:

    # ==========================================
    # Helper: rotation
    # ==========================================
    @staticmethod
    def _rotate_point(x, y, cx, cy, angle_deg):
        rad = math.radians(angle_deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        dx = x - cx
        dy = y - cy

        new_x = cx + dx * cos_a - dy * sin_a
        new_y = cy + dx * sin_a + dy * cos_a

        return int(new_x), int(new_y)

    # ==========================================
    # LETTER A 
    # ==========================================
    @staticmethod
    def draw_A(skeleton, top_width=0, crossbar_h_shift=0,
               base_width_factor=1.0, shear_x=0, thickness=6, **kwargs):

        skeleton.clear()

        CENTER_X = 100 - int(shear_x // 2)
        TOP_Y = 40
        BOTTOM_Y = 175
        HEIGHT = BOTTOM_Y - TOP_Y

        base_width = int(100 * base_width_factor)
        top_width = int(top_width)

        def shear(x, y):
            factor = (BOTTOM_Y - y) / HEIGHT
            return max(5, min(195, int(x + shear_x * factor))), y

        bl = shear(CENTER_X - base_width // 2, BOTTOM_Y) # Bottom Left
        br = shear(CENTER_X + base_width // 2, BOTTOM_Y) # Bottom Right
        tl = shear(CENTER_X - top_width // 2, TOP_Y)     # Top Left
        tr = shear(CENTER_X + top_width // 2, TOP_Y)     # Top Right

        skeleton.draw_line(bl, tl, thickness)
        skeleton.draw_line(br, tr, thickness)

        if top_width > 0:
            skeleton.draw_line(tl, tr, thickness)

        bar_y = (TOP_Y + BOTTOM_Y) // 2 - crossbar_h_shift
        bar_y = max(TOP_Y + 20, min(BOTTOM_Y - 25, bar_y))
    
        total_h = BOTTOM_Y - TOP_Y
        if total_h == 0: total_h = 1 
        
        ratio = (bar_y - TOP_Y) / total_h 

        bar_left_x = tl[0] + (bl[0] - tl[0]) * ratio
        bar_right_x = tr[0] + (br[0] - tr[0]) * ratio

        skeleton.draw_line((int(bar_left_x), bar_y), (int(bar_right_x), bar_y), thickness)


    # ==========================================
    # LETTER B 
    # ==========================================
    @staticmethod
    def draw_B(skeleton, width_factor=1.0, waist_y_shift=0,
               rotation_deg=0, vertical_squash=1.0, thickness=6, **kwargs):

        skeleton.clear()

        LEFT_X = 60
        TOP_Y = 30
        BOTTOM_Y = 170
        CENTER_Y = 100
        WIDTH = int(70 * width_factor)

        def squash(y):
            return int(CENTER_Y + (y - CENTER_Y) * vertical_squash)

        top = squash(TOP_Y)
        bottom = squash(BOTTOM_Y)
        waist = squash(100 - waist_y_shift)

        p1 = CanonicalLetters._rotate_point(LEFT_X, top, 100, 100, rotation_deg)
        p2 = CanonicalLetters._rotate_point(LEFT_X, bottom, 100, 100, rotation_deg)
        skeleton.draw_line(p1, p2, thickness)

        skeleton.draw_curve(
            center=CanonicalLetters._rotate_point(LEFT_X, (top + waist)//2, 100, 100, rotation_deg),
            axes=(WIDTH, abs(waist-top)//2),
            angle=rotation_deg,
            start_angle=-90,
            end_angle=90,
            thickness=thickness
        )

        skeleton.draw_curve(
            center=CanonicalLetters._rotate_point(LEFT_X, (waist + bottom)//2, 100, 100, rotation_deg),
            axes=(WIDTH, abs(bottom-waist)//2),
            angle=rotation_deg,
            start_angle=-90,
            end_angle=90,
            thickness=thickness
        )

    # ==========================================
    # LETTER C 
    # ==========================================
    @staticmethod
    def draw_C(skeleton, rotation_deg=0, cut_top=0,
               cut_bottom=0, vertical_squash=1.0, thickness=6, **kwargs):

        skeleton.clear()

        CENTER_X = 110
        CENTER_Y = 100
        R = 75

        start_angle = 45 + cut_bottom
        end_angle = 315 - cut_top

        skeleton.draw_curve(
            center=(CENTER_X, CENTER_Y),
            axes=(R, int(R * vertical_squash)),
            angle=rotation_deg,
            start_angle=start_angle, 
            end_angle=end_angle,
            thickness=thickness
        )

    # ==========================================
    # LETTER F 
    # ==========================================
    @staticmethod
    def draw_F(skeleton, bar_length=1.0, middle_bar_shift=0,
               shear_x=0, spine_height=1.0, thickness=6, **kwargs):

        skeleton.clear()

        LEFT_X = 55
        TOP_Y = 30
        HEIGHT = int((170 - 30) * spine_height)
        bottom_y = TOP_Y + HEIGHT
        bar_len = int(90 * bar_length)

        def shear(x, y):
            factor = (bottom_y - y) / HEIGHT if HEIGHT != 0 else 0
            return max(5, min(195, int(x + shear_x * factor))), y

        skeleton.draw_line(shear(LEFT_X, TOP_Y), shear(LEFT_X, bottom_y), thickness)
        
        skeleton.draw_line(shear(LEFT_X, TOP_Y), shear(LEFT_X + bar_len, TOP_Y), thickness)

        mid_y = TOP_Y + int(HEIGHT * 0.45) + middle_bar_shift
        skeleton.draw_line(
            shear(LEFT_X, mid_y),
            shear(LEFT_X + int(bar_len * 0.5), mid_y),
            thickness
        )

    # ==========================================
    # LETTER X
    # ==========================================
    @staticmethod
    def draw_X(skeleton, cross_ratio=0.5, spread_angle=0, rotation_deg=0,
               asymmetry=0, thickness=6, **kwargs):

        skeleton.clear()
        center_x, center_y = 100, 100
        
        # 1. Base Width calculation
        # spread_angle adds to the width (range -20 to 20 approx)
        base_half_width = 50 + (spread_angle * 1.5)
        
        # 2. Adjust Top vs Bottom width based on cross_ratio
        # ratio 0.5 -> Equal widths
        # ratio < 0.5 -> Top narrower (cross moves up)
        # ratio > 0.5 -> Top wider (cross moves down)
        top_scale = cross_ratio * 2.0
        bot_scale = (1.0 - cross_ratio) * 2.0
        
        # Calculate X coordinates relative to center
        # We clamp scales slightly to prevent width becoming 0
        w_top = int(base_half_width * max(0.2, top_scale))
        w_bot = int(base_half_width * max(0.2, bot_scale))
        
        # Define the 4 corners
        # Top-Left, Top-Right (Shifted by asymmetry)
        tl = (center_x - w_top, 30)
        tr = (center_x + w_top + int(asymmetry), 30)
        
        # Bottom-Left, Bottom-Right (Shifted by asymmetry)
        bl = (center_x - w_bot + int(asymmetry), 170)
        br = (center_x + w_bot, 170)

        # 3. Apply Rotation (Optional)
        if rotation_deg != 0:
            tl = CanonicalLetters._rotate_point(*tl, center_x, center_y, rotation_deg)
            tr = CanonicalLetters._rotate_point(*tr, center_x, center_y, rotation_deg)
            bl = CanonicalLetters._rotate_point(*bl, center_x, center_y, rotation_deg)
            br = CanonicalLetters._rotate_point(*br, center_x, center_y, rotation_deg)

        # 4. Draw the two diagonals
        skeleton.draw_line(tl, br, thickness)
        skeleton.draw_line(tr, bl, thickness)

    # ==========================================
    #  LETTER W 
    # ==========================================
    @staticmethod
    def draw_W(skeleton, peak_depth=0.7, width_factor=1.0,
               middle_height=0.5, shear_x=0, thickness=6, **kwargs):

        skeleton.clear()

        CX = 100
        TOP = 30
        BOT = 170
        HEIGHT = BOT - TOP

        width = int(160 * width_factor)
        half = width // 2
        quarter = width // 4

        valley = TOP + int(HEIGHT * peak_depth)
        mid_peak = TOP + int(HEIGHT * (1 - middle_height))

        def shear(x, y):
            factor = (BOT - y) / HEIGHT
            return max(5, min(195, int(x + shear_x * factor))), y

        p1 = shear(CX - half, TOP)
        p2 = shear(CX - quarter, valley)
        p3 = shear(CX, mid_peak)
        p4 = shear(CX + quarter, valley)
        p5 = shear(CX + half, TOP)

        skeleton.draw_line(p1, p2, thickness)
        skeleton.draw_line(p2, p3, thickness)
        skeleton.draw_line(p3, p4, thickness)
        skeleton.draw_line(p4, p5, thickness)