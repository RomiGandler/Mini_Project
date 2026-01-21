import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from skimage.metrics import structural_similarity as ssim
import numpy as np
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters

# ==========================================
#  Define global colors and styles
# ==========================================
COLORS = {
    'bg': '#2E3440',        # Dark background
    'panel': '#3B4252',     # Panel background
    'text': '#ECEFF4',      # White text
    'accent': '#88C0D0',    # Turquoise
    'accent_red': '#BF616A',# Red
    'success': '#A3BE8C',   # Green
    'warning': '#EBCB8B',   # Yellow
    'danger': '#BF616A'     # Dark Red
}

# Define global font 
plt.rcParams['font.family'] = 'monospace'

# ==========================================
# 1. Parameter Definitions (including F, X, W)
# ==========================================
PARAMS = {
    'A': [
        ('base_width_factor', 1.0, 1.8, 1.0, 'Leg Width'),
        ('top_width', 0, 80, 0, 'Top Width'),
        ('crossbar_h_shift', 0, 40, 0, 'Bar Shift'),
        ('shear_x', 0, 35, 0, 'Shear X'),
        ('thickness', 6, 18, 6, 'Thickness')
    ],
    'B': [
        ('width_factor', 0.5, 1.0, 1.0, 'Width'),
        ('waist_y_shift', 0, 40, 0, 'Waist Shift'),
        ('rotation_deg', -30, 0, 0, 'Rotation'),
        ('vertical_squash', 0.6, 1.0, 1.0, 'Squash'),
        ('thickness', 6, 18, 6, 'Thickness')
    ],
    'C': [
        ('cut_top', -60, 40, 40, 'Cut Top'), 
        ('vertical_squash', 0.45, 1.0, 1.0, 'Squash'),
        ('rotation_deg', 0, 45, 0, 'Rotation'),
        ('thickness', 6, 18, 6, 'Thickness')
    ],
    'F': [
        ('bar_length', 0.5, 1.5, 1.0, 'Bar Length'),
        ('middle_bar_shift', -30, 30, 0, 'Mid Bar Shift'),
        ('shear_x', -30, 30, 0, 'Shear X'),
        ('spine_height', 0.6, 1.2, 1.0, 'Spine Height'),
        ('thickness', 6, 18, 6, 'Thickness')
    ],
    'X': [
        ('cross_ratio', 0.3, 0.7, 0.5, 'Cross Pos'),
        ('spread_angle', -20, 20, 0, 'Spread'),
        ('rotation_deg', -30, 30, 0, 'Rotation'),
        ('asymmetry', -20, 20, 0, 'Asymmetry'),
        ('thickness', 6, 18, 6, 'Thickness')
    ],
    'W': [
        ('peak_depth', 0.3, 0.9, 0.7, 'Peak Depth'),
        ('width_factor', 0.6, 1.4, 1.0, 'Width'),
        ('middle_height', 0.3, 0.8, 0.5, 'Mid Height'),
        ('shear_x', -25, 25, 0, 'Shear X'),
        ('thickness', 6, 18, 6, 'Thickness')
    ]
}

DRAW_FUNCS = {
    'A': CanonicalLetters.draw_A,
    'B': CanonicalLetters.draw_B,
    'C': CanonicalLetters.draw_C,
    'F': CanonicalLetters.draw_F,
    'X': CanonicalLetters.draw_X,
    'W': CanonicalLetters.draw_W,
}

# ==========================================
# 2. Initialize Variables
# ==========================================
model = LetterSkeleton(size=(200, 200))
current_letter = 'A'
sliders = []
slider_axes = []
base_image = None
score_text_obj = None

# ==========================================
# 3. Helper Functions
# ==========================================
def calculate_distance(img1, img2):
    if img1.shape != img2.shape: return 0.0
    d_range = img1.max() - img1.min()
    if d_range == 0: d_range = 1
    similarity = ssim(img1, img2, data_range=d_range)
    return max(0, 1.0 - similarity)

def generate_base_image():
    global base_image
    defaults = {p[0]: p[3] for p in PARAMS[current_letter]}
    thick = int(defaults.pop('thickness', 6))
    DRAW_FUNCS[current_letter](model, **defaults, thickness=thick)
    base_image = model.apply_morphology(thickness=thick)

# ==========================================
# 4. Create the GUI
# ==========================================

fig = plt.figure(figsize=(14, 9), facecolor=COLORS['bg'])
fig.canvas.manager.set_window_title('Letter Deformation - Extended (A,B,C,F,X,W)')

# --- Header Titles ---
fig.text(0.5, 0.93, "LETTER DEFORMATIONS", ha='center', fontsize=24, 
         fontweight='bold', color=COLORS['text'])

score_text_obj = fig.text(0.5, 0.87, "DIST SCORE: 0.000", ha='center', 
                          fontsize=18, fontweight='bold', color=COLORS['success'])

# --- Image Area ---
ax_img = fig.add_axes([0.38, 0.32, 0.55, 0.50]) 
ax_img.axis('off') 

# --- Letter Selection Area (now with 6 letters) ---
ax_radio = fig.add_axes([0.03, 0.70, 0.18, 0.22], facecolor=COLORS['bg'])
radio = RadioButtons(ax_radio, ('A', 'B', 'C', 'F', 'X', 'W'), active=0,
                    label_props={'color': [COLORS['text']]*6, 'fontsize': [14]*6},
                    radio_props={'s': [100]*6, 'facecolor': [COLORS['accent']]*6})
for spine in ax_radio.spines.values(): spine.set_visible(False)

# --- Controls Title ---
fig.text(0.38, 0.25, "CONTROLS", color=COLORS['accent'], 
         fontsize=12, weight='bold', ha='left')

# Create space for sliders
slider_positions = [0.21, 0.17, 0.13, 0.09, 0.05]
for pos in slider_positions:
    ax = fig.add_axes([0.38, pos, 0.50, 0.03], facecolor=COLORS['panel'])
    for spine in ax.spines.values(): spine.set_edgecolor(COLORS['panel'])
    slider_axes.append(ax)

# ==========================================
# 5. Define Interaction Functions
# ==========================================

def update_image(val=None):
    current_params = {}
    
    for i, slider in enumerate(sliders):
        param_info = PARAMS[current_letter][i]
        name = param_info[0]
        val = slider.val
        if 'factor' not in name and 'squash' not in name and 'ratio' not in name and 'depth' not in name and 'height' not in name:
            val = int(val)
        current_params[name] = val
    
    thick = int(current_params.pop('thickness', 6))
    if isinstance(thick, float): thick = int(thick)
    
    DRAW_FUNCS[current_letter](model, **current_params, thickness=thick)
    img = model.apply_morphology(thickness=thick)

    dist = calculate_distance(base_image, img)

    ax_img.clear()
    ax_img.imshow(img, cmap='gray')
    ax_img.axis('off')

    color = COLORS['success'] if dist < 0.25 else COLORS['warning'] if dist < 0.5 else COLORS['danger']
    score_text_obj.set_text(f"DIST SCORE: {dist:.3f}")
    score_text_obj.set_color(color)

    fig.canvas.draw_idle()

def create_sliders():
    global sliders
    sliders = []
    
    letter_params = PARAMS[current_letter]
    
    for i, ax in enumerate(slider_axes):
        ax.clear()
        if i < len(letter_params):
            name, p_min, p_max, p_default, label = letter_params[i]

            try:
                s = Slider(ax, label, p_min, p_max, valinit=p_default, 
                           color=COLORS['accent'], track_color=COLORS['panel'])
            except TypeError:
                s = Slider(ax, label, p_min, p_max, valinit=p_default, 
                           color=COLORS['accent'])

            s.label.set_color(COLORS['text'])
            s.label.set_fontsize(11)
            s.label.set_fontweight('bold')
            s.valtext.set_color(COLORS['accent'])
            s.valtext.set_fontweight('bold')
            
            s.on_changed(update_image)
            sliders.append(s)
            ax.set_visible(True)
        else:
            ax.set_visible(False)

def change_letter(label):
    global current_letter
    current_letter = label
    generate_base_image()
    create_sliders()
    update_image()

def reset(event):
    letter_params = PARAMS[current_letter]
    for i, slider in enumerate(sliders):
        slider.set_val(letter_params[i][3])

# ==========================================
# 6. Define Actions
# ==========================================

radio.on_clicked(change_letter)

# Reset button
ax_reset = fig.add_axes([0.03, 0.55, 0.18, 0.06])
btn_reset = Button(ax_reset, 'RESET', color=COLORS['panel'], hovercolor=COLORS['accent_red'])
btn_reset.label.set_color(COLORS['text'])
btn_reset.label.set_fontweight('bold')
btn_reset.on_clicked(reset)
for spine in ax_reset.spines.values(): spine.set_visible(False)

# Side explanation text
info_text = """
GUIDE
-----
A: Classic triangle
B: Spine + loops
C: Open arc
F: Spine + bars
X: Crossing lines
W: Valley peaks

PARAMS
------
Width: Horizontal
Height: Vertical
Shear: Tilt/Slant
Depth: Valley/Gap

> 0.5 = HIGH DIST
"""
fig.text(0.03, 0.45, info_text, fontsize=9, 
         color=COLORS['text'], alpha=0.7, va='top')

# Initial run
generate_base_image()
create_sliders()
update_image()

plt.show()
