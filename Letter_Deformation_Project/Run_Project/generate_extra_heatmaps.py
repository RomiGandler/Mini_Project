import sys
import os

# --- PATH CONFIGURATION START ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
CONFIG_PATH = os.path.join(parent_dir, 'param_config.json')
# --- PATH CONFIGURATION END ---

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import json
from skimage.metrics import structural_similarity as ssim
from skimage.filters import gaussian

from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters

# =========================
# Configuration
# =========================

DRAW_FUNCS = {
    'A': CanonicalLetters.draw_A,
    'B': CanonicalLetters.draw_B,
    'C': CanonicalLetters.draw_C,
    'F': CanonicalLetters.draw_F,
    'X': CanonicalLetters.draw_X,
    'W': CanonicalLetters.draw_W,
}

OUTPUT_DIR = os.path.join(parent_dir, "analysis_results", "heatmaps")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# Utilities
# =========================

def load_param_config(filepath):
    if not os.path.exists(filepath):
        print(f"❌ Error: Config file '{filepath}' not found!")
        exit(1)
    with open(filepath, 'r') as f:
        return json.load(f)

PARAM_CONFIG = load_param_config(CONFIG_PATH)

def calculate_distance(img1, img2):
    """Consistent distance metric using Gaussian blur + SSIM."""
    if img1.shape != img2.shape: return 0.0
    
    img1_blur = gaussian(img1, sigma=1.5)
    img2_blur = gaussian(img2, sigma=1.5)
    
    d_range = img1_blur.max() - img1_blur.min()
    if d_range == 0: d_range = 1 
    
    sim = ssim(img1_blur, img2_blur, data_range=d_range)
    return max(0.0, 1.0 - sim)

def get_base_image(letter_char):
    model = LetterSkeleton(size=(200, 200))
    params = {k: v['default'] for k, v in PARAM_CONFIG[letter_char].items()}
    thick = int(params.pop('thickness', 6))
    DRAW_FUNCS[letter_char](model, **params, thickness=thick)
    return model.apply_morphology(thickness=thick)

def generate_single_heatmap(letter, param1, range1, steps1, param2, range2, steps2, filename_suffix=""):
    """Core function to generate and save one heatmap."""
    print(f"   -> Generating: {letter} ({param1} vs {param2})...")

    x_values = np.linspace(range1[0], range1[1], steps1)
    y_values = np.linspace(range2[0], range2[1], steps2)

    heatmap_data = np.zeros((steps2, steps1))
    
    base_img = get_base_image(letter)
    model = LetterSkeleton(size=(200, 200))

    # Get defaults
    default_params = {k: v['default'] for k, v in PARAM_CONFIG[letter].items()}
    cfg1_default = PARAM_CONFIG[letter][param1]['default']
    cfg2_default = PARAM_CONFIG[letter][param2]['default']

    for i, y_val in enumerate(y_values):
        for j, x_val in enumerate(x_values):
            current_params = default_params.copy()

            # Handle types
            if isinstance(cfg1_default, int): current_params[param1] = int(round(x_val))
            else: current_params[param1] = float(x_val)
                
            if isinstance(cfg2_default, int): current_params[param2] = int(round(y_val))
            else: current_params[param2] = float(y_val)
            
            thick = int(current_params.pop('thickness', 6))
            
            model.clear()
            DRAW_FUNCS[letter](model, **current_params, thickness=thick)
            img = model.apply_morphology(thickness=thick)
            
            score = calculate_distance(base_img, img)
            heatmap_data[i, j] = score

    # Plot
    plt.figure(figsize=(10, 8))
    # Flip data so Y-min is at the bottom
    ax = sns.heatmap(np.flipud(heatmap_data), annot=True, fmt=".2f", cmap="coolwarm",
                     xticklabels=[f"{x:.1f}" for x in x_values],
                     yticklabels=[f"{y:.1f}" for y in np.flip(y_values)])
    
    plt.title(f"Distance Score Heatmap: {letter}\n{param1} (X) vs {param2} (Y)", fontsize=14, fontweight='bold')
    plt.xlabel(param1, fontsize=12)
    plt.ylabel(param2, fontsize=12)
    
    if filename_suffix:
        fname = f"heatmap_{letter}_{param1}_{param2}_{filename_suffix}.png"
    else:
        fname = f"heatmap_{letter}_{param1}_{param2}.png"
        
    save_path = os.path.join(OUTPUT_DIR, fname)
    plt.savefig(save_path)
    plt.close()
    print(f"      Saved to: {save_path}")

# =========================
# Modes
# =========================

def mode_interactive():
    print("\n--- 🖐️ Interactive Heatmap Mode ---")
    letter = input("Which letter (A, B, C, F, X, W)? ").upper().strip()
    if letter not in DRAW_FUNCS: return print("❌ Invalid letter!")

    print(f"Available parameters: {list(PARAM_CONFIG[letter].keys())}")
    p1 = input("Param X: ").strip()
    p2 = input("Param Y: ").strip()
    if p1 not in PARAM_CONFIG[letter] or p2 not in PARAM_CONFIG[letter]: return print("❌ Invalid params.")

    # Use config limits
    r1 = (PARAM_CONFIG[letter][p1]['min'], PARAM_CONFIG[letter][p1]['max'])
    r2 = (PARAM_CONFIG[letter][p2]['min'], PARAM_CONFIG[letter][p2]['max'])
    
    generate_single_heatmap(letter, p1, r1, 10, p2, r2, 10, filename_suffix="custom")

def mode_batch_report():
    print("\n--- 📑 Generating Standard Report (All Letters) ---")
    
    # 1. Letter A: Shear vs Width
    generate_single_heatmap('A', 'shear_x', (-40, 40), 10, 'base_width_factor', (0.5, 1.8), 10)

    # 2. Letter B: Squash vs Waist
    generate_single_heatmap('B', 'vertical_squash', (0.4, 1.0), 10, 'waist_y_shift', (-30, 30), 10)

    # 3. Letter C: Cut Angle vs Squash
    generate_single_heatmap('C', 'cut_top', (-20, 80), 10, 'vertical_squash', (0.4, 1.0), 10)

    # 4. Letter F: Bar Length vs Shear
    generate_single_heatmap('F', 'bar_length', (0.5, 1.5), 10, 'shear_x', (-30, 30), 10)

    # 5. Letter X: Cross Ratio vs Spread
    generate_single_heatmap('X', 'cross_ratio', (0.3, 0.7), 10, 'spread_angle', (-20, 20), 10)

    # 6. Letter W: Peak Depth vs Width
    generate_single_heatmap('W', 'peak_depth', (0.3, 0.9), 10, 'width_factor', (0.6, 1.4), 10)
    
    print("\n✅ Batch Report Completed.")

# =========================
# Main Menu
# =========================

if __name__ == "__main__":
    print("\n🔍 Parameter Heatmap Tool")
    print("1. Interactive Mode (Choose your own params)")
    print("2. Batch Mode (Generate standard report for all letters)")
    
    choice = input("\nSelect option (1 or 2): ").strip()
    
    if choice == '1':
        mode_interactive()
    elif choice == '2':
        mode_batch_report()
    else:
        print("Invalid selection.")