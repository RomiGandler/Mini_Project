import sys
import os

# --- PATH CONFIGURATION START ---
# Get the directory where this script is located (run_project)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (Letter_Deformation_Project)
parent_dir = os.path.dirname(current_dir)
# Add parent directory to Python's search path to find 'src'
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
# Define the absolute path to the config file
CONFIG_PATH = os.path.join(parent_dir, 'param_config.json')
# --- PATH CONFIGURATION END ---

import json
import itertools
import matplotlib.pyplot as plt
import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.filters import gaussian
import matplotlib

# Use Agg backend to save memory and avoid GUI windows during batch processing
matplotlib.use('Agg')

from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters

# ==========================================
# 1. Global Setup & Short Names
# ==========================================

PARAM_CONFIG = {}

PARAM_SHORT_NAMES = {
    'base_width_factor': 'Legs',
    'width_factor': 'W',
    'top_width': 'Top',
    'crossbar_h_shift': 'Bar',
    'waist_y_shift': 'Waist',
    'rotation_deg': 'Rot',
    'vertical_squash': 'Squash',
    'cut_top': 'Cut',
    'shear_x': 'Shear',
    'thickness': 'Thick',
    'bar_length': 'BarLen',
    'middle_bar_shift': 'MidBar',
    'spine_height': 'Spine',
    'cross_ratio': 'Cross',
    'spread_angle': 'Spread',
    'asymmetry': 'Asym',
    'peak_depth': 'Peak',
    'middle_height': 'MidH'
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
# 2. Helper Functions
# ==========================================

def load_param_config(filepath):
    """Loads the external configuration file with path fallback."""
    if not os.path.exists(filepath):
        # Fallback to check relative path if absolute fails
        filepath = os.path.join(parent_dir, 'param_config.json')
        if not os.path.exists(filepath):
            print(f"❌ Error: Config file not found at {filepath}")
            sys.exit(1)
    
    with open(filepath, 'r') as f:
        print(f"✅ Loaded configuration from {filepath}")
        return json.load(f)

def get_user_steps():
    """
    Prompts user for steps or uses default.
    Supports command line arguments for automation.
    """
    # Check if steps were passed as an argument (e.g., python script.py 5)
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        return int(sys.argv[1])

    default_steps = 10
    try:
        user_input = input(f"Enter number of deformation steps (default {default_steps}): ").strip()
        if user_input.isdigit():
            return int(user_input)
    except KeyboardInterrupt:
        sys.exit()
    print(f"Using default steps: {default_steps}")
    return default_steps

def calculate_distance(img1, img2):
    """
    Calculates distance with tolerance for thickness changes
    using Gaussian Blur before SSIM comparison.
    Range: 0.0 (Identical) to 1.0 (Different).
    """
    if img1.shape != img2.shape: return 0.0
    
    # Apply Gaussian blur to soften edges (reduces pixel-perfect requirements)
    img1_blur = gaussian(img1, sigma=1.5)
    img2_blur = gaussian(img2, sigma=1.5)
    
    d_range = img1_blur.max() - img1_blur.min()
    if d_range == 0: d_range = 1.0
    
    similarity = ssim(img1_blur, img2_blur, data_range=d_range)
    return max(0.0, 1.0 - similarity)

def get_interpolated_params(letter_char, active_keys, t):
    """
    Interpolates parameters based on 't' (0.0 to 1.0).
    Active keys move from Min to Max. Inactive keys stay at Default.
    """
    letter_config = PARAM_CONFIG[letter_char]
    current_params = {}
    
    # 1. Set defaults for all parameters
    for key, props in letter_config.items():
        current_params[key] = props['default']

    # 2. Calculate values for active parameters (interpolation)
    for key in active_keys:
        props = letter_config[key]
        start_val = props['min']
        end_val = props['max']
        
        # Linear interpolation
        val = start_val + (end_val - start_val) * t
        
        if isinstance(start_val, int) and isinstance(end_val, int):
            current_params[key] = int(round(val))
        else:
            current_params[key] = val
            
    return current_params

def get_all_combinations(param_keys):
    """Generates all possible combinations of parameters."""
    all_combos = []
    for r in range(1, len(param_keys) + 1):
        combinations = list(itertools.combinations(param_keys, r))
        all_combos.extend(combinations)
    return all_combos

def get_color_for_score(score):
    """Returns a color string based on the distance score."""
    if score < 0.25:
        return 'green'   # Excellent match
    elif score < 0.50:
        return '#ff8c00' # Dark Orange (Moderate match)
    else:
        return 'red'     # Poor match / High distortion

def save_single_image(img, title, filepath, score=0.0):
    """Saves a single image with a color-coded title."""
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.imshow(img, cmap='gray')
    
    title_color = get_color_for_score(score)
    ax.set_title(title, fontsize=8, color=title_color, fontweight='bold')
    
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(filepath, dpi=100)
    plt.close(fig)

def save_summary_matrix(images, titles, scores, main_title, filepath):
    """
    Saves a grid of images as a summary contact sheet.
    """
    if not images: return
    num_imgs = len(images)
    rows = int(np.ceil(np.sqrt(num_imgs)))
    cols = int(np.ceil(num_imgs / rows))
    
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 2.5, rows * 3.0))
    fig.suptitle(f"Family: {main_title}", fontsize=16, y=1.02)
    
    if num_imgs > 1: axes_flat = axes.flatten()
    else: axes_flat = [axes]

    for i, ax in enumerate(axes_flat):
        if i < num_imgs:
            ax.imshow(images[i], cmap='gray')
            c = get_color_for_score(scores[i])
            ax.set_title(titles[i], fontsize=7, color=c, fontweight='bold')
            ax.axis('off')
        else:
            ax.axis('off')
            
    plt.tight_layout()
    plt.savefig(filepath, dpi=100, bbox_inches='tight')
    plt.close(fig)

# ==========================================
# 3. Main Generation Logic
# ==========================================

def main():
    global PARAM_CONFIG
    
    # Load config
    PARAM_CONFIG = load_param_config(CONFIG_PATH)
    steps = get_user_steps()
    
    # Define output directory at project root
    root_dir = os.path.join(parent_dir, "OUTPUT_DATASET")
    os.makedirs(root_dir, exist_ok=True)
    
    print(f"\n🚀 Starting Dataset Generation...")
    print(f"📂 Output Directory: {os.path.abspath(root_dir)}\n")

    dataset_metadata = []

    for letter_char, draw_func in DRAW_FUNCS.items():
        if letter_char not in PARAM_CONFIG:
            continue

        letter_dir = os.path.join(root_dir, letter_char)
        os.makedirs(letter_dir, exist_ok=True)
        print(f"Processing Letter {letter_char}...", end='\r')

        model = LetterSkeleton(size=(200, 200))

        # --- Base Image Generation ---
        base_params = get_interpolated_params(letter_char, [], 0) 
        base_thick = int(base_params.pop('thickness', 6))
        
        draw_func(model, **base_params, thickness=base_thick)
        base_img = model.apply_morphology(thickness=base_thick)
        
        # Save base image
        full_base_path = os.path.join(letter_dir, "base_letter.png")
        save_single_image(base_img, f"Base {letter_char}", full_base_path, score=0.0)
        
        # Add base metadata
        dataset_metadata.append({
            "letter": letter_char,
            "type": "base",
            "deformation_family": "None",
            "filename": "base_letter.png",
            "filepath": os.path.join(letter_char, "base_letter.png"),
            "score_dist": 0.0,
            "parameters": {**base_params, "thickness": base_thick}
        })

        # --- Deformation Loop ---
        param_keys = list(PARAM_CONFIG[letter_char].keys())
        combinations = get_all_combinations(param_keys)
        
        for combo in combinations:
            deformation_name_short = "_".join([PARAM_SHORT_NAMES.get(k, k) for k in combo])
            deformation_subdir_name = f"deformation_{deformation_name_short}"
            deformation_subdir_path = os.path.join(letter_dir, deformation_subdir_name)
            os.makedirs(deformation_subdir_path, exist_ok=True)

            summary_images = []
            summary_titles = []
            summary_scores = []

            for i in range(steps):
                t = i / max(1, (steps - 1))

                params = get_interpolated_params(letter_char, combo, t)
                thickness_val = params.pop('thickness', 6)
                if isinstance(thickness_val, float): thickness_val = int(thickness_val)

                draw_func(model, **params, thickness=thickness_val)
                img = model.apply_morphology(thickness=thickness_val)
                dist_score = calculate_distance(base_img, img)

                # Construct filename
                filename_params = []
                title_params = []
                for k in combo:
                    val = thickness_val if k == 'thickness' else params.get(k)
                    val_fmt = f"{val:.1f}" if isinstance(val, float) else f"{val}"
                    short = PARAM_SHORT_NAMES.get(k, k)
                    filename_params.append(f"{short}{val_fmt}")
                    title_params.append(f"{short}:{val_fmt}")

                fname_str = "_".join(filename_params)
                filename = f"{fname_str}.png"
                rel_path = os.path.join(letter_char, deformation_subdir_name, filename)
                full_path = os.path.join(root_dir, rel_path)
                
                title_str = f"Dist: {dist_score:.2f}\n" + "\n".join(title_params)
                save_single_image(img, title_str, full_path, score=dist_score)

                # Metadata
                summary_images.append(img)
                summary_titles.append(title_str)
                summary_scores.append(dist_score)

                full_params_record = {**params, "thickness": thickness_val}
                dataset_metadata.append({
                    "letter": letter_char,
                    "type": "deformation",
                    "deformation_family": deformation_name_short,
                    "active_params": list(combo),
                    "filename": filename,
                    "filepath": rel_path,
                    "score_dist": float(f"{dist_score:.4f}"), 
                    "parameters": full_params_record
                })

            # Save summary contact sheet for this deformation family
            summary_filename = f"SUMMARY_{deformation_name_short}.png"
            summary_path = os.path.join(letter_dir, summary_filename)
            save_summary_matrix(summary_images, summary_titles, summary_scores, deformation_name_short, summary_path)

        print(f"✅ Finished Letter {letter_char}     ")

    # --- Save JSON Summary ---
    json_output_path = os.path.join(root_dir, "dataset_summary.json")
    print(f"\n💾 Saving metadata to {json_output_path}...")
    with open(json_output_path, 'w') as f:
        json.dump(dataset_metadata, f, indent=4)

    print("\n🎉 Dataset Generation Complete!")

if __name__ == "__main__":
    main()