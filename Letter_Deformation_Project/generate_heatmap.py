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
    'F': CanonicalLetters.draw_F,
    'X': CanonicalLetters.draw_X,
    'W': CanonicalLetters.draw_W,
}

OUTPUT_DIR = "results/heatmaps"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def calculate_distance(img1, img2):
    d_range = img1.max() - img1.min()
    if d_range == 0: d_range = 1
    sim = ssim(img1, img2, data_range=d_range)
    return max(0, 1.0 - sim)

def get_base_image(letter_char):
    model = LetterSkeleton(size=(200, 200))
    params = {k: v['default'] for k, v in PARAM_CONFIG[letter_char].items()}
    DRAW_FUNCS[letter_char](model, **params)
    return model.apply_morphology(thickness=params['thickness'])

def generate_heatmap():
    print("\n--- 2D Parameter Heatmap Generator ---")
    print(f"Available letters: {list(DRAW_FUNCS.keys())}")
    
    letter = input("Which letter (A, B, C, F, X, W)? ").upper().strip()
    if letter not in DRAW_FUNCS:
        print("Invalid letter!")
        return

    print(f"\nAvailable parameters for {letter}: {list(PARAM_CONFIG[letter].keys())}")
    
    param1 = input("Select Parameter X (horizontal): ").strip()
    param2 = input("Select Parameter Y (vertical): ").strip()
    
    if param1 not in PARAM_CONFIG[letter] or param2 not in PARAM_CONFIG[letter]:
        print("Invalid parameters.")
        return

    cfg1 = PARAM_CONFIG[letter][param1]
    cfg2 = PARAM_CONFIG[letter][param2]

    steps = 10
    x_values = np.linspace(cfg1['min'], cfg1['max'], steps)
    y_values = np.linspace(cfg2['min'], cfg2['max'], steps)
    
    heatmap_data = np.zeros((steps, steps))
    
    base_img = get_base_image(letter)
    model = LetterSkeleton(size=(200, 200))

    print("Calculating grid...")

    for i, y_val in enumerate(y_values):
        for j, x_val in enumerate(x_values):
            current_params = {k: v['default'] for k, v in PARAM_CONFIG[letter].items()}

            # Handle data types
            if isinstance(cfg1['default'], float):
                current_params[param1] = float(x_val)
            else:
                current_params[param1] = int(x_val)
                
            if isinstance(cfg2['default'], float):
                current_params[param2] = float(y_val)
            else:
                current_params[param2] = int(y_val)
            
            model.clear()
            DRAW_FUNCS[letter](model, **current_params)
            img = model.apply_morphology(thickness=current_params['thickness'])
            
            score = calculate_distance(base_img, img)
            heatmap_data[i, j] = score

    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="coolwarm",
                     xticklabels=[f"{x:.1f}" for x in x_values],
                     yticklabels=[f"{y:.1f}" for y in y_values])
    
    plt.title(f"Distance Score Heatmap: {letter}\n{param1} vs {param2}")
    plt.xlabel(param1)
    plt.ylabel(param2)
    
    filename = f"heatmap_{letter}_{param1}_{param2}.png"
    save_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(save_path)
    print(f"Heatmap saved to {save_path}")
    plt.show()

if __name__ == "__main__":
    generate_heatmap()
