import os
import itertools
import matplotlib.pyplot as plt
import numpy as np
from skimage.metrics import structural_similarity as ssim
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters

# ==========================================
# 1. Configuration Definitions
# ==========================================

CONFIGS = {
    'A': {
        'base_width_factor': (1.0, 1.8), 
        'top_width': (0, 80),            
        'crossbar_h_shift': (0, 40),     
        'shear_x': (0, 35),              
        'thickness': (6, 18)             
    },
    'B': {
        'width_factor': (1.0, 0.5),
        'waist_y_shift': (0, 40),
        'rotation_deg': (0, -30),
        'vertical_squash': (1.0, 0.6),
        'thickness': (6, 18)
    },
    'C': {
        'cut_top': (40, -60),
        'vertical_squash': (1.0, 0.45),
        'rotation_deg': (0, 45),
        'thickness': (6, 18)
    }
}

PARAM_SHORT_NAMES = {
    'base_width_factor': 'Legs',
    'width_factor': 'W',
    'top_width': 'Top',
    'crossbar_h_shift': 'Bar',
    'waist_y_shift': 'Waist',
    'rotation_deg': 'Rot',
    'vertical_squash': 'Squash',
    'elongation_factor': 'Elong',
    'cut_top': 'Cut',
    'shear_x': 'Shear',
    'thickness': 'Thick'
}

# ==========================================
# 2. Helper Functions
# ==========================================

def calculate_distance(img1, img2):
    if img1.shape != img2.shape:
        return 0.0
    d_range = img1.max() - img1.min()
    if d_range == 0: d_range = 1 
    
    similarity = ssim(img1, img2, data_range=d_range)
    return max(0, 1.0 - similarity)

def get_interpolated_params(letter_char, active_keys, t):
    config = CONFIGS[letter_char]
    current_params = {}
    
    for key, (start_val, end_val) in config.items():
        current_params[key] = start_val

    for key in active_keys:
        start_val, end_val = config[key]
        val = start_val + (end_val - start_val) * t
        
        if isinstance(start_val, int) and isinstance(end_val, int):
            current_params[key] = int(val)
        else:
            current_params[key] = val
            
    return current_params

def get_all_combinations(param_keys):
    all_combos = []
    for r in range(1, len(param_keys) + 1):
        combinations = list(itertools.combinations(param_keys, r))
        all_combos.extend(combinations)
    return all_combos

# ==========================================
# 3. Grid Drawing and Analysis
# ==========================================

def generate_full_matrix_for_letter(letter_char, draw_func, output_dir):
    print(f"Generating FULL matrix with SCORES for Letter {letter_char}...")
    
    param_keys = list(CONFIGS[letter_char].keys())
    combinations = get_all_combinations(param_keys)
    
    num_rows = len(combinations)
    steps = 10 
    
    fig_height = num_rows * 2.2 
    fig_width = steps * 1.8
    
    fig, axes = plt.subplots(num_rows, steps, figsize=(fig_width, fig_height))
    fig.suptitle(f"Letter {letter_char}: Analysis (Value & Distance Score)", fontsize=24, y=1.002)

    model = LetterSkeleton(size=(200, 200))

    # --- Base Image for Comparison ---
    base_params = get_interpolated_params(letter_char, [], 0)
    # Using pop to remove thickness from the dictionary to avoid duplication
    base_thick = int(base_params.pop('thickness', 6))
    
    draw_func(model, **base_params, thickness=base_thick)
    base_img = model.apply_morphology(thickness=base_thick)

    # --- Main Loop ---
    for row_idx, combo in enumerate(combinations):
        
        display_name = " + ".join([PARAM_SHORT_NAMES.get(k, k) for k in combo])
        
        for col_idx in range(steps):
            t = col_idx / (steps - 1)
            params = get_interpolated_params(letter_char, combo, t)

            # This removes thickness from the params dictionary, so it won't be passed twice.
            thickness_val = params.pop('thickness', 6)
            if isinstance(thickness_val, float): thickness_val = int(thickness_val)

            draw_func(model, **params, thickness=thickness_val)
            
            img = model.apply_morphology(thickness=thickness_val)

            # Calculate the score
            dist_score = calculate_distance(base_img, img)

            # Creating text for parameters
            info_texts = []
            for k in combo:
                # Since we did pop, thickness is not in params
                if k == 'thickness':
                    val = thickness_val
                else:
                    val = params.get(k)
                
                if isinstance(val, float): val_str = f"{val:.1f}"
                else: val_str = f"{val}"
                
                short_name = PARAM_SHORT_NAMES.get(k, k)
                info_texts.append(f"{short_name}:{val_str}")
            
            if len(info_texts) > 2:
                mid = len(info_texts) // 2
                param_str = ",".join(info_texts[:mid]) + "\n" + ",".join(info_texts[mid:])
            else:
                param_str = "\n".join(info_texts)

            # Display
            ax = axes[row_idx, col_idx]
            ax.imshow(img, cmap='gray')
            ax.axis('off')
            
            title_text = f"Dist: {dist_score:.2f}\n{param_str}"
            ax.set_title(title_text, fontsize=7, pad=2)
            
            if col_idx == 0:
                ax.text(-50, 100, display_name, fontsize=11, weight='bold', va='center', ha='right')

    plt.tight_layout()
    filename = os.path.join(output_dir, f"FULL_MATRIX_{letter_char}_SCORED.png")
    plt.savefig(filename, dpi=70, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filename}")

def main():
    OUTPUT_DIR = 'full_matrices_scored'
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    generate_full_matrix_for_letter('A', CanonicalLetters.draw_A, OUTPUT_DIR)
    generate_full_matrix_for_letter('B', CanonicalLetters.draw_B, OUTPUT_DIR)
    generate_full_matrix_for_letter('C', CanonicalLetters.draw_C, OUTPUT_DIR)
    
    print(f"\n✅ Done! Check '{OUTPUT_DIR}' folder.")

if __name__ == "__main__":
    main()