import numpy as np
import matplotlib.pyplot as plt
import os
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters
from skimage.metrics import structural_similarity as ssim

# ==========================================
# Parameter Deformation Analysis
# ==========================================
RESULTS_DIR = "results/distance_analysis"
os.makedirs(RESULTS_DIR, exist_ok=True)

# ==========================================
# Help Methods   
# ==========================================

def calculate_similarity(img1, img2):
    d_range = img1.max() - img1.min()
    if d_range == 0: d_range = 1
    return ssim(img1, img2, data_range=d_range)

def analyze_single_letter(letter_char, draw_func, param_name, param_range, default_params):
    """
    Analyzes how deformation of a single parameter affects visual distance.
    """
    print(f"Analyzing Letter {letter_char} on parameter: {param_name}...")
    
    model = LetterSkeleton(size=(200, 200))

    # 1. Create the base image (Original)
    draw_func(model, **default_params)
    base_img = model.apply_morphology(thickness=6)
    
    distances = []
    values = []

    # 2. Run the loop over the parameter
    for val in param_range:
        current_params = default_params.copy()
        current_params[param_name] = val

        # Clear and redraw
        model.canvas.fill(0)
        draw_func(model, **current_params)
        deformed_img = model.apply_morphology(thickness=6)

        # Calculate distance (1 - similarity)
        sim = calculate_similarity(base_img, deformed_img)
        dist = 1 - sim
        
        distances.append(dist)
        values.append(val)

    # 3. Draw the graph
    plt.figure(figsize=(10, 6))
    plt.plot(values, distances, marker='o', linewidth=2, color='#88C0D0')
    plt.title(f"Letter {letter_char}: Deformation Distance vs {param_name}", fontsize=14)
    plt.xlabel(f"{param_name} Value", fontsize=12)
    plt.ylabel("Visual Distance (1 - SSIM)", fontsize=12)
    plt.grid(True, alpha=0.3)

    # Save to the new directory
    output_path = os.path.join(RESULTS_DIR, f"{letter_char}_distance_analysis.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Saved graph to: {output_path}")

# ==========================================
# Configuration (now including F, X, W)
# ==========================================

CONFIG = {
    'A': {
        'func': CanonicalLetters.draw_A,
        'param': 'shear_x',
        'range': np.linspace(0, 35, 20),
        'defaults': {'base_width_factor': 1.0, 'top_width': 0, 'crossbar_h_shift': 0, 'shear_x': 0, 'thickness': 6}
    },
    'B': {
        'func': CanonicalLetters.draw_B,
        'param': 'vertical_squash',
        'range': np.linspace(0.5, 1.0, 20),
        'defaults': {'width_factor': 1.0, 'waist_y_shift': 0, 'rotation_deg': 0, 'vertical_squash': 1.0, 'thickness': 6}
    },
    'C': {
        'func': CanonicalLetters.draw_C,
        'param': 'cut_top',
        'range': np.linspace(-60, 40, 20),
        'defaults': {'cut_top': 40, 'vertical_squash': 1.0, 'rotation_deg': 0, 'thickness': 6}
    },
    'F': {
        'func': CanonicalLetters.draw_F,
        'param': 'bar_length',
        'range': np.linspace(0.5, 1.5, 20),
        'defaults': {'bar_length': 1.0, 'middle_bar_shift': 0, 'shear_x': 0, 'spine_height': 1.0, 'thickness': 6}
    },
    'X': {
        'func': CanonicalLetters.draw_X,
        'param': 'cross_ratio',
        'range': np.linspace(0.3, 0.7, 20),
        'defaults': {'cross_ratio': 0.5, 'spread_angle': 0, 'rotation_deg': 0, 'asymmetry': 0, 'thickness': 6}
    },
    'W': {
        'func': CanonicalLetters.draw_W,
        'param': 'peak_depth',
        'range': np.linspace(0.3, 0.9, 20),
        'defaults': {'peak_depth': 0.7, 'width_factor': 1.0, 'middle_height': 0.5, 'shear_x': 0, 'thickness': 6}
    }
}

# ==========================================
# Main Execution
# ==========================================

if __name__ == "__main__":
    print("--- Starting Full Analysis (A, B, C, F, X, W) ---")
    
    for letter, conf in CONFIG.items():
        analyze_single_letter(
            letter_char=letter,
            draw_func=conf['func'],
            param_name=conf['param'],
            param_range=conf['range'],
            default_params=conf['defaults']
        )
        
    print("\nAll analyses completed successfully!")
    print(f"Check the results in: {RESULTS_DIR}")
