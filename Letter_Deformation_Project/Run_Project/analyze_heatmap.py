import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import json
from skimage.metrics import structural_similarity as ssim
from skimage.filters import gaussian

# --- PATH CONFIGURATION ---
# Fix paths so we can import from src/ even if running from Run_Project/
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters

# =========================
# Configuration
# =========================

# Central output directory: analysis/heatmaps
OUTPUT_DIR = os.path.join(parent_dir, "analysis", "heatmaps")
os.makedirs(OUTPUT_DIR, exist_ok=True)
CONFIG_PATH = os.path.join(parent_dir, 'param_config.json')

DRAW_FUNCS = {
    'A': CanonicalLetters.draw_A,
    'B': CanonicalLetters.draw_B,
    'C': CanonicalLetters.draw_C,
    'F': CanonicalLetters.draw_F,
    'X': CanonicalLetters.draw_X,
    'W': CanonicalLetters.draw_W,
}

# =========================
# Utilities
# =========================

def load_param_config(filepath):
    """Loads the parameter configuration JSON."""
    if not os.path.exists(filepath):
        print(f"❌ Error: Config file not found at {filepath}")
        sys.exit(1)
    with open(filepath, 'r') as f:
        return json.load(f)

PARAM_CONFIG = load_param_config(CONFIG_PATH)

def calculate_distance(img1, img2):
    """Calculates visual distance using blurred SSIM."""
    if img1.shape != img2.shape: return 0.0
    img1_blur = gaussian(img1, sigma=1.5)
    img2_blur = gaussian(img2, sigma=1.5)
    d_range = img1_blur.max() - img1_blur.min()
    if d_range == 0: d_range = 1 
    sim = ssim(img1_blur, img2_blur, data_range=d_range)
    return max(0.0, 1.0 - sim)

def get_base_image(letter):
    """Generates the canonical base image for a letter."""
    model = LetterSkeleton(size=(200, 200))
    params = {k: v['default'] for k, v in PARAM_CONFIG[letter].items()}
    thick = int(params.pop('thickness', 6))
    DRAW_FUNCS[letter](model, **params, thickness=thick)
    return model.apply_morphology(thickness=thick)

# =========================
# Core Logic
# =========================

def generate_heatmap(letter, param1, param2, steps=10, show_plot=False):
    """
    Generates and saves a 2D heatmap showing the interaction between two parameters.
    """
    print(f"   -> Generating Heatmap: {letter} ({param1} vs {param2})...")
    
    # Validation
    if param1 not in PARAM_CONFIG[letter] or param2 not in PARAM_CONFIG[letter]:
        print(f"❌ Error: Invalid parameters for {letter}")
        return

    # Get ranges from config
    cfg1 = PARAM_CONFIG[letter][param1]
    cfg2 = PARAM_CONFIG[letter][param2]

    x_values = np.linspace(cfg1['min'], cfg1['max'], steps)
    y_values = np.linspace(cfg2['min'], cfg2['max'], steps)
    
    heatmap_data = np.zeros((steps, steps))
    
    base_img = get_base_image(letter)
    model = LetterSkeleton(size=(200, 200))

    # Get defaults once
    default_params = {k: v['default'] for k, v in PARAM_CONFIG[letter].items()}

    for i, y_val in enumerate(y_values): # Rows (Y axis)
        for j, x_val in enumerate(x_values): # Cols (X axis)
            current_params = default_params.copy()

            # Handle types (int vs float)
            if isinstance(cfg1['default'], int): current_params[param1] = int(round(x_val))
            else: current_params[param1] = float(x_val)
                
            if isinstance(cfg2['default'], int): current_params[param2] = int(round(y_val))
            else: current_params[param2] = float(y_val)
            
            thick = int(current_params.pop('thickness', 6))
            
            model.clear()
            DRAW_FUNCS[letter](model, **current_params, thickness=thick)
            img = model.apply_morphology(thickness=thick)
            
            score = calculate_distance(base_img, img)
            heatmap_data[i, j] = score

    # Plotting
    plt.figure(figsize=(10, 8))
    
    # We use flipud (flip up-down) so that the visual Y-axis matches a graph (min at bottom)
    ax = sns.heatmap(np.flipud(heatmap_data), annot=True, fmt=".2f", cmap="coolwarm",
                     xticklabels=[f"{x:.1f}" for x in x_values],
                     yticklabels=[f"{y:.1f}" for y in np.flip(y_values)])
    
    plt.title(f"Distance Score Heatmap: {letter}\n{param1} (X) vs {param2} (Y)", fontsize=14, fontweight='bold')
    plt.xlabel(param1, fontsize=12)
    plt.ylabel(param2, fontsize=12)
    
    filename = f"heatmap_{letter}_{param1}_{param2}.png"
    save_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(save_path, bbox_inches='tight')
    print(f"      Saved: {save_path}")
    
    if show_plot:
        plt.show()
    plt.close()

# =========================
# Modes
# =========================

def mode_interactive():
    print("\n--- 🌡️ Interactive Heatmap Generator ---")
    letter = input("Which letter (A, B, C, F, X, W)? ").upper().strip()
    if letter not in DRAW_FUNCS: return print("❌ Invalid letter!")

    print(f"Params: {list(PARAM_CONFIG[letter].keys())}")
    p1 = input("Param X: ").strip()
    p2 = input("Param Y: ").strip()
    
    generate_heatmap(letter, p1, p2, steps=10, show_plot=True)

def mode_batch_report():
    print("\n--- 📑 Generating Standard Heatmap Report ---")
    
    # List of interesting parameter pairs to analyze
    pairs = [
        ('A', 'shear_x', 'base_width_factor'),
        ('B', 'vertical_squash', 'waist_y_shift'),
        ('C', 'cut_top', 'vertical_squash'),
        ('F', 'bar_length', 'middle_bar_shift'),
        ('X', 'cross_ratio', 'spread_angle'),
        ('W', 'peak_depth', 'width_factor')
    ]
    
    for l, p1, p2 in pairs:
        generate_heatmap(l, p1, p2, steps=10, show_plot=False)
    
    print("\n✅ Batch Heatmap Report Completed.")

if __name__ == "__main__":
    if "--batch" in sys.argv:
        mode_batch_report()
    else:
        print("\nHeatmap Tool")
        print("1. Interactive Mode")
        print("2. Batch Mode")
        choice = input("Select: ").strip()
        
        if choice == '1': mode_interactive()
        elif choice == '2': mode_batch_report()
        else: print("Invalid.")