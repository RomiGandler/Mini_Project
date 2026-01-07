import matplotlib.pyplot as plt
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters
from src.param_config import PARAM_CONFIG, get_limits

DRAW_FUNCS = {
    'A': CanonicalLetters.draw_A,
    'B': CanonicalLetters.draw_B,
    'C': CanonicalLetters.draw_C,
}

OUTPUT_DIR = "results/custom_sequences"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def calculate_distance(img1, img2):
    d_range = img1.max() - img1.min()
    if d_range == 0: d_range = 1
    sim = ssim(img1, img2, data_range=d_range)
    return max(0, 1.0 - sim)

def get_base_image(letter_char):
    model = LetterSkeleton(size=(200, 200))
    # Retrieve default values from the configuration
    params = {k: v['default'] for k, v in PARAM_CONFIG[letter_char].items()}
    DRAW_FUNCS[letter_char](model, **params)
    return model.apply_morphology(thickness=params['thickness'])

def run_sequence():
    print("\n--- Custom Deformation Generator (Safe Mode) ---")
    
    letter = input("Which letter (A, B, C)? ").upper().strip()
    if letter not in DRAW_FUNCS:
        print("Invalid letter!")
        return

    print(f"\nAvailable parameters for {letter}:")
    # Display the parameters with their limits
    for key, val in PARAM_CONFIG[letter].items():
        print(f" - {key} [Min: {val['min']}, Max: {val['max']}]")
    
    param_name = input("\nWhich parameter to change? ").strip()
    if param_name not in PARAM_CONFIG[letter]:
        print("Invalid parameter name!")
        return

    limits = get_limits(letter, param_name)
    
    try:
        start_raw = float(input(f"Start value (Limit {limits['min']}): "))
        end_raw = float(input(f"End value (Limit {limits['max']}): "))
        steps = int(input("Number of steps (e.g., 5 or 10): "))
    except ValueError:
        print("Please enter valid numbers.")
        return

    # === Clamping ===
    start_val = max(limits['min'], min(limits['max'], start_raw))
    end_val = max(limits['min'], min(limits['max'], end_raw))
    
    if start_val != start_raw or end_val != end_raw:
        print(f"⚠️ Note: Values were clamped to safe limits: {start_val} to {end_val}")

    # Prepare the model
    model = LetterSkeleton(size=(200, 200))
    base_img = get_base_image(letter)
    
    param_values = np.linspace(start_val, end_val, steps)
    images = []
    scores = []
    
    print(f"\nGenerating {steps} variations...")

    for val in param_values:
        model.canvas.fill(0)

        # Build the dictionary for the current parameters
        current_params = {k: v['default'] for k, v in PARAM_CONFIG[letter].items()}

        # Update the selected parameter
        if param_name in ['base_width_factor', 'width_factor', 'vertical_squash']:
            current_params[param_name] = float(val)
        else:
            current_params[param_name] = int(val)
            
        DRAW_FUNCS[letter](model, **current_params)
        img = model.apply_morphology(thickness=current_params['thickness'])
        
        images.append(img)
        scores.append(calculate_distance(base_img, img))

    # Draw the graph (same code as before)
    fig = plt.figure(figsize=(15, 8))
    fig.suptitle(f"Analysis of '{letter}' varying '{param_name}'", fontsize=16, fontweight='bold')

    for i in range(steps):
        ax = fig.add_subplot(2, steps, i + 1)
        ax.imshow(images[i], cmap='gray')
        ax.set_title(f"{param_values[i]:.1f}\nScore: {scores[i]:.2f}", fontsize=9)
        ax.axis('off')

    ax_graph = fig.add_subplot(2, 1, 2)
    ax_graph.plot(param_values, scores, marker='o', linestyle='-', color='#88C0D0', linewidth=2)
    ax_graph.set_xlabel(f"{param_name} Value")
    ax_graph.set_ylabel("Distance Score (Lower is Better)")
    ax_graph.grid(True, alpha=0.3)
    
    for x, y in zip(param_values, scores):
        ax_graph.text(x, y, f"{y:.2f}", fontsize=8, ha='right', va='bottom')

    plt.tight_layout()
    filename = f"{letter}_{param_name}_{start_val:.1f}_to_{end_val:.1f}.png"
    save_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(save_path)
    print(f"\nDone! Saved result to:\n{save_path}")
    plt.show()

if __name__ == "__main__":
    run_sequence()