import sys
import os

# --- PATH CONFIGURATION START ---
# Get the directory where this script is located (run_project)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (Letter_Deformation_Project)
parent_dir = os.path.dirname(current_dir)
# Add parent directory to Python's search path to find 'src'
sys.path.append(parent_dir)
# Define the absolute path to the config file
CONFIG_PATH = os.path.join(parent_dir, 'param_config.json')
# --- PATH CONFIGURATION END ---

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from skimage.metrics import structural_similarity as ssim
from skimage.filters import gaussian
import numpy as np
import json

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
# 1. Configuration & JSON Loading
# ==========================================

# Mapping technical parameter names to GUI labels
PARAM_LABELS = {
    'base_width_factor': 'Leg Width',
    'width_factor': 'Width',
    'top_width': 'Top Width',
    'crossbar_h_shift': 'Bar Height',
    'shear_x': 'Shear / Tilt',
    'thickness': 'Thickness',
    'waist_y_shift': 'Waist Shift',
    'rotation_deg': 'Rotation',
    'vertical_squash': 'Squash',
    'cut_top': 'Cut Opening',
    'bar_length': 'Bar Length',
    'middle_bar_shift': 'Mid-Bar Shift',
    'spine_height': 'Spine Height',
    'cross_ratio': 'Cross Point',
    'spread_angle': 'Spread Angle',
    'asymmetry': 'Asymmetry',
    'peak_depth': 'Peak Depth',
    'middle_height': 'Middle Peak'
}

def load_params_from_json(filepath):
    """
    Loads parameters from JSON and converts them to the list format 
    expected by the GUI: (key, min, max, default, label)
    """
    if not os.path.exists(filepath):
        print(f"❌ Error: Config file '{filepath}' not found!")
        exit(1)
        
    with open(filepath, 'r') as f:
        config = json.load(f)
    
    gui_params = {}
    
    for letter, params in config.items():
        letter_list = []
        for key, props in params.items():
            label = PARAM_LABELS.get(key, key) # Get pretty name or use key
            # Tuple format: (key, min, max, default, label)
            letter_list.append((key, props['min'], props['max'], props['default'], label))
        
        gui_params[letter] = letter_list
        
    print("✅ Loaded parameters from JSON successfully.")
    return gui_params

# Load the parameters dynamically using the absolute path
PARAMS = load_params_from_json(CONFIG_PATH)

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
    """
    Calculates distance using Gaussian Blur + SSIM.
    This matches the logic used in 'generate_dataset.py'.
    """
    if img1.shape != img2.shape: return 0.0
    
    # Apply Gaussian blur to soften edges (Tolerance for thickness)
    img1_blur = gaussian(img1, sigma=1.5)
    img2_blur = gaussian(img2, sigma=1.5)
    
    d_range = img1_blur.max() - img1_blur.min()
    if d_range == 0: d_range = 1
    
    similarity = ssim(img1_blur, img2_blur, data_range=d_range)
    return max(0, 1.0 - similarity)

def generate_base_image():
    global base_image
    # Extract defaults from the loaded JSON structure
    defaults = {p[0]: p[3] for p in PARAMS[current_letter]}
    
    thick = int(defaults.pop('thickness', 6))
    DRAW_FUNCS[current_letter](model, **defaults, thickness=thick)
    base_image = model.apply_morphology(thickness=thick)

# ==========================================
# 4. Create the GUI
# ==========================================

fig = plt.figure(figsize=(14, 9), facecolor=COLORS['bg'])
fig.canvas.manager.set_window_title('Letter Deformation - Interactive JSON Mode')

# --- Header Titles ---
fig.text(0.5, 0.93, "LETTER DEFORMATIONS (JSON CONFIG)", ha='center', fontsize=24, 
         fontweight='bold', color=COLORS['text'])

score_text_obj = fig.text(0.5, 0.87, "DIST SCORE: 0.000", ha='center', 
                          fontsize=18, fontweight='bold', color=COLORS['success'])

# --- Image Area ---
ax_img = fig.add_axes([0.38, 0.32, 0.55, 0.50]) 
ax_img.axis('off') 

# --- Letter Selection Area ---
# Dynamically get available letters from the config
available_letters = tuple(PARAMS.keys())
ax_radio = fig.add_axes([0.03, 0.70, 0.18, 0.22], facecolor=COLORS['bg'])
radio = RadioButtons(ax_radio, available_letters, active=0,
                    label_props={'color': [COLORS['text']]*len(available_letters), 'fontsize': [14]*len(available_letters)},
                    radio_props={'s': [100]*len(available_letters), 'facecolor': [COLORS['accent']]*len(available_letters)})
for spine in ax_radio.spines.values(): spine.set_visible(False)

# --- Controls Title ---
fig.text(0.38, 0.25, "CONTROLS (Loaded from param_config.json)", color=COLORS['accent'], 
         fontsize=12, weight='bold', ha='left')

# Create space for sliders (Max 6 params supported by layout, but expandable)
slider_positions = [0.21, 0.17, 0.13, 0.09, 0.05, 0.01] 
for pos in slider_positions:
    ax = fig.add_axes([0.38, pos, 0.50, 0.03], facecolor=COLORS['panel'])
    for spine in ax.spines.values(): spine.set_edgecolor(COLORS['panel'])
    slider_axes.append(ax)

# ==========================================
# 5. Define Interaction Functions
# ==========================================

def update_image(val=None):
    current_params = {}
    
    # Iterate only through the number of active parameters for this letter
    num_params = len(PARAMS[current_letter])
    
    for i in range(num_params):
        if i >= len(sliders): break
        
        slider = sliders[i]
        param_info = PARAMS[current_letter][i]
        name = param_info[0] # The technical name
        val = slider.val
        
        # Round integers if necessary (heuristic based on name)
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

    # Color coding based on score
    color = COLORS['success'] if dist < 0.25 else '#ff8c00' if dist < 0.5 else COLORS['danger']
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
        # Reset to default value (index 3 in tuple)
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
Select a letter
and adjust sliders.

Green  < 0.25
Orange < 0.50
Red    > 0.50

Params loaded
from JSON.
"""
fig.text(0.03, 0.45, info_text, fontsize=9, 
         color=COLORS['text'], alpha=0.7, va='top')

# Initial run
generate_base_image()
create_sliders()
update_image()

plt.show()