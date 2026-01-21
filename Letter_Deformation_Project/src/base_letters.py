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
    # LETTER A (unchanged)
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

        bl = shear(CENTER_X - base_width // 2, BOTTOM_Y)
        br = shear(CENTER_X + base_width // 2, BOTTOM_Y)
        tl = shear(CENTER_X - top_width // 2, TOP_Y)
        tr = shear(CENTER_X + top_width // 2, TOP_Y)

        skeleton.draw_line(bl, tl, thickness)
        skeleton.draw_line(br, tr, thickness)

        if top_width > 0:
            skeleton.draw_line(tl, tr, thickness)

        bar_y = (TOP_Y + BOTTOM_Y) // 2 - crossbar_h_shift
        bar_y = max(TOP_Y + 20, min(BOTTOM_Y - 25, bar_y))

        skeleton.draw_line((tl[0], bar_y), (tr[0], bar_y), thickness)

    # ==========================================
    # LETTER B (unchanged)
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
    # LETTER C (unchanged)
    # ==========================================
    @staticmethod
    def draw_C(skeleton, rotation_deg=0, cut_top=0,
               cut_bottom=0, vertical_squash=1.0, thickness=6, **kwargs):

        skeleton.clear()

        CENTER_X = 110
        CENTER_Y = 100
        R = 75

        skeleton.draw_curve(
            center=(CENTER_X, CENTER_Y),
            axes=(R, int(R * vertical_squash)),
            angle=rotation_deg,
            start_angle=45,
            end_angle=315 - cut_top,
            thickness=thickness
        )

    # ==========================================
    # 🔥 LETTER F — EXTREME
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
            factor = (bottom_y - y) / HEIGHT
            return max(5, min(195, int(x + shear_x * factor * factor))), y

        skeleton.draw_line(shear(LEFT_X, TOP_Y), shear(LEFT_X, bottom_y), thickness)
        skeleton.draw_line(shear(LEFT_X, TOP_Y), shear(LEFT_X + bar_len, TOP_Y), thickness)

        mid_y = TOP_Y + int(HEIGHT * 0.45) + middle_bar_shift
        skeleton.draw_line(
            shear(LEFT_X, mid_y),
            shear(LEFT_X + int(bar_len * 0.5), mid_y),
            thickness
        )

    # ==========================================
    # 🔥 LETTER X — SCALE + ROTATION
    # ==========================================
    @staticmethod
    def draw_X(skeleton, spread_angle=0, rotation_deg=0,
               asymmetry=0, scale=1.0, thickness=6, **kwargs):

        skeleton.clear()

        CX, CY = 100, 100
        TOP, BOT = 30, 170
        base = 45 + spread_angle

        def scale_pt(x, y):
            return int(CX + (x-CX)*scale), int(CY + (y-CY)*scale)

        tl = scale_pt(CX - base - asymmetry, TOP)
        tr = scale_pt(CX + base + asymmetry, TOP)
        bl = scale_pt(CX - base, BOT)
        br = scale_pt(CX + base, BOT)

        tl = CanonicalLetters._rotate_point(*tl, CX, CY, rotation_deg)
        tr = CanonicalLetters._rotate_point(*tr, CX, CY, rotation_deg)
        bl = CanonicalLetters._rotate_point(*bl, CX, CY, rotation_deg)
        br = CanonicalLetters._rotate_point(*br, CX, CY, rotation_deg)

        skeleton.draw_line(tl, br, thickness)
        skeleton.draw_line(tr, bl, thickness)

    # ==========================================
    # 🔥 LETTER W — EXTREME SHEAR
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
            return max(5, min(195, int(x + shear_x * factor * factor))), y

        p1 = shear(CX - half, TOP)
        p2 = shear(CX - quarter, valley)
        p3 = shear(CX, mid_peak)
        p4 = shear(CX + quarter, valley)
        p5 = shear(CX + half, TOP)

        skeleton.draw_line(p1, p2, thickness)
        skeleton.draw_line(p2, p3, thickness)
        skeleton.draw_line(p3, p4, thickness)
        skeleton.draw_line(p4, p5, thickness)
