import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
from skimage.metrics import structural_similarity as ssim
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters
from src.param_config import PARAM_CONFIG

DRAW_FUNCS = {
    'A': CanonicalLetters.draw_A,
    'B': CanonicalLetters.draw_B,
    'C': CanonicalLetters.draw_C,
}

OUTPUT_DIR = "results/heatmaps"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def calculate_distance(img1, img2):
    """Calculates Distance = 1 - SSIM"""
    d_range = img1.max() - img1.min()
    if d_range == 0: d_range = 1
    sim = ssim(img1, img2, data_range=d_range)
    return max(0, 1.0 - sim)

def get_base_image(letter_char):
    """Generates the canonical (base) image for a letter"""
    model = LetterSkeleton(size=(200, 200))
    params = {k: v['default'] for k, v in PARAM_CONFIG[letter_char].items()}
    DRAW_FUNCS[letter_char](model, **params)
    return model.apply_morphology(thickness=params['thickness'])

def generate_heatmap_auto(letter, param1, range1, steps1, param2, range2, steps2, output_file):
    """
    Generates a heatmap automatically (no user input).
    """
    print(f"--- Generating Heatmap for {letter}: {param1} vs {param2} ---")

    # Parameter value arrays
    x_values = np.linspace(range1[0], range1[1], steps1)
    y_values = np.linspace(range2[0], range2[1], steps2)

    # Preparing the matrix (rows x columns)
    heatmap_data = np.zeros((steps2, steps1))
    
    base_img = get_base_image(letter)
    model = LetterSkeleton(size=(200, 200))

    # Calculating the matrix
    for i, y_val in enumerate(y_values):  # Rows (Param 2)
        for j, x_val in enumerate(x_values):  # Columns (Param 1)

            # Loading defaults
            current_params = {k: v['default'] for k, v in PARAM_CONFIG[letter].items()}

            # Data type handling (int for angles/pixels, float for ratios)
            val_x_clean = int(x_val) if 'width' not in param1 and 'squash' not in param1 else x_val
            val_y_clean = int(y_val) if 'width' not in param2 and 'squash' not in param2 else y_val
            
            current_params[param1] = val_x_clean
            current_params[param2] = val_y_clean
            
            model.clear()
            DRAW_FUNCS[letter](model, **current_params)
            img = model.apply_morphology(thickness=current_params['thickness'])
            
            score = calculate_distance(base_img, img)
            heatmap_data[i, j] = score

    # Plotting the heatmap
    plt.figure(figsize=(10, 8))

    # Creating axis labels (nicely rounded)
    xtick_labels = [f"{x:.1f}" for x in x_values]
    ytick_labels = [f"{y:.1f}" for y in y_values]

    # Using Seaborn
    # Flip the Y-axis to have values run from bottom to top like a regular graph
    sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="coolwarm",
                xticklabels=xtick_labels,
                yticklabels=ytick_labels)
    
    plt.title(f"Distance Score Heatmap: {letter}\n{param1} (X) vs {param2} (Y)")
    plt.xlabel(param1)
    plt.ylabel(param2)

    # Saving
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    print(f"Saved heatmap to: {output_file}\n")


if __name__ == "__main__":
    print("Starting automated heatmap generation...\n")

    # 1. Letter B: Squash vs. Waist Shift
    generate_heatmap_auto(
        letter='B',
        param1='vertical_squash', range1=(0.4, 1.0), steps1=10,
        param2='waist_y_shift',   range2=(-40, 40), steps2=10,
        output_file='results/heatmaps/heatmap_B.png'
    )

    # 2. Letter C: Cut Angle vs. Squash
    generate_heatmap_auto(
        letter='C',
        param1='cut_top',         range1=(-20, 90), steps1=10,
        param2='vertical_squash', range2=(0.5, 1.1), steps2=10,
        output_file='results/heatmaps/heatmap_C.png'
    )

    print("Done! Check 'results/heatmaps/' folder.")