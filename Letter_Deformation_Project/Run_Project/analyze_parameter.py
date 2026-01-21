import sys
import os
import matplotlib.pyplot as plt
import numpy as np
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

# Central output directory: analysis/parameter_plots
OUTPUT_DIR = os.path.join(parent_dir, "analysis", "parameter_plots")
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
# Analysis Logic
# =========================

def run_analysis(letter, param, start, end, steps, show_plot=False, save_prefix=""):
    """
    Runs the analysis for a single parameter.
    Generates a report containing both the image sequence and the distance graph.
    """
    print(f"   -> Analyzing {letter}: {param}...")
    
    model = LetterSkeleton(size=(200, 200))
    base_img = get_base_image(letter)
    
    values = np.linspace(start, end, steps)
    images, scores = [], []
    default_params = {k: v['default'] for k, v in PARAM_CONFIG[letter].items()}

    for val in values:
        model.clear()
        current_params = default_params.copy()
        
        # Handle int vs float parameters
        if isinstance(current_params[param], int):
            current_params[param] = int(round(val))
        else:
            current_params[param] = float(val)

        thick = int(current_params.pop('thickness', 6))
        DRAW_FUNCS[letter](model, **current_params, thickness=thick)
        img = model.apply_morphology(thickness=thick)

        images.append(img)
        scores.append(calculate_distance(base_img, img))

    # --- Visualization ---
    
    fig = plt.figure(figsize=(16, 8))
    fig.suptitle(f"Parameter Analysis: {letter} – '{param}'", fontsize=18, fontweight='bold')

    # Top row: Images (limit to 12 max to prevent crowding)
    display_steps = min(steps, 12) 
    indices = np.linspace(0, steps-1, display_steps, dtype=int)
    
    for i, idx in enumerate(indices):
        ax = fig.add_subplot(2, display_steps, i + 1)
        ax.imshow(images[idx], cmap='gray')
        
        score = scores[idx]
        color = 'green' if score < 0.25 else 'orange' if score < 0.5 else 'red'
        
        ax.set_title(f"{values[idx]:.1f}\n{score:.2f}", fontsize=9, color=color)
        ax.axis('off')

    # Bottom row: Graph
    ax_plot = fig.add_subplot(2, 1, 2)
    ax_plot.plot(values, scores, marker='o', linestyle='-', color='#88C0D0', linewidth=2)
    ax_plot.axhline(y=0.25, color='green', linestyle='--', alpha=0.5, label='Match (0.25)')
    ax_plot.axhline(y=0.50, color='red', linestyle='--', alpha=0.5, label='Distorted (0.50)')
    
    ax_plot.set_xlabel(f"Parameter Value: {param}", fontsize=12)
    ax_plot.set_ylabel("Distance (1 - SSIM)", fontsize=12)
    ax_plot.legend()
    ax_plot.grid(alpha=0.3)

    filename = f"{save_prefix}{letter}_{param}_analysis.png"
    path = os.path.join(OUTPUT_DIR, filename)
    plt.tight_layout()
    plt.savefig(path, dpi=100)
    print(f"      Saved: {path}")
    
    if show_plot:
        plt.show() 
    plt.close()

# =========================
# Modes
# =========================

def mode_interactive():
    print("\n--- 🔍 Interactive Parameter Analysis ---")
    letter = input("Choose letter (A, B, C, F, X, W): ").upper().strip()
    if letter not in DRAW_FUNCS: return print("❌ Invalid letter")

    print(f"Available params: {list(PARAM_CONFIG[letter].keys())}")
    param = input("Parameter to vary: ").strip()
    if param not in PARAM_CONFIG[letter]: return print("❌ Invalid parameter")

    p_min = PARAM_CONFIG[letter][param]['min']
    p_max = PARAM_CONFIG[letter][param]['max']
    
    try:
        s_in = input(f"Start value ({p_min}): ")
        e_in = input(f"End value ({p_max}): ")
        st_in = input("Steps (10): ")
        
        start = float(s_in) if s_in else p_min
        end = float(e_in) if e_in else p_max
        steps = int(st_in) if st_in else 10
        
        run_analysis(letter, param, start, end, steps, show_plot=True)
    except ValueError:
        print("❌ Invalid input.")

def mode_batch_report():
    print("\n--- 📑 Generating Standard 1D Report (All Letters) ---")
    
    # Run the standard suite for all letters
    run_analysis('A', 'shear_x', -30, 30, 12, save_prefix="report_")
    run_analysis('B', 'vertical_squash', 0.4, 1.0, 12, save_prefix="report_")
    run_analysis('C', 'cut_top', -20, 80, 12, save_prefix="report_")
    run_analysis('F', 'bar_length', 0.5, 1.5, 12, save_prefix="report_")
    run_analysis('X', 'cross_ratio', 0.3, 0.7, 12, save_prefix="report_")
    run_analysis('W', 'peak_depth', 0.3, 0.9, 12, save_prefix="report_")
    
    print("\n✅ Batch Report Completed.")

if __name__ == "__main__":
    # Check if run from main.py with --batch argument
    if "--batch" in sys.argv:
        mode_batch_report()
    else:
        print("\n📈 Parameter Analysis Tool")
        print("1. Interactive Mode (Explore one param with GUI)")
        print("2. Batch Mode (Generate report for all letters)")
        
        choice = input("\nSelect option (1 or 2): ").strip()
        
        if choice == '1':
            mode_interactive()
        elif choice == '2':
            mode_batch_report()
        else:
            print("Invalid selection.")