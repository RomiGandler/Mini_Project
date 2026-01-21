import os
import matplotlib.pyplot as plt
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters
from src.param_config import PARAM_CONFIG

# Configuration for the output directory
OUTPUT_DIR = "results/report_examples"
os.makedirs(OUTPUT_DIR, exist_ok=True)

DRAW_FUNCS = {
    'A': CanonicalLetters.draw_A,
    'B': CanonicalLetters.draw_B,
    'C': CanonicalLetters.draw_C,
    'F': CanonicalLetters.draw_F,
    'X': CanonicalLetters.draw_X,
    'W': CanonicalLetters.draw_W,
}

def save_example(letter, param_name, param_value, filename):
    """
    Generates and saves a letter image with a single modified parameter.
    Used for creating visual examples for the methodology section.
    """
    model = LetterSkeleton(size=(200, 200))
    
    # Load default parameters from the central configuration
    params = {k: v['default'] for k, v in PARAM_CONFIG[letter].items()}
    
    # Update the specific parameter for demonstration purposes
    params[param_name] = param_value
    
    # Draw the specific letter based on the input char
    DRAW_FUNCS[letter](model, **params)
        
    # Apply morphology (thickness) to get the final raster image
    img = model.apply_morphology(thickness=params['thickness'])
    
    # Plotting setup: Remove axes and whitespace for clean report figures
    plt.figure(figsize=(3, 3))
    plt.imshow(img, cmap='gray')
    plt.axis('off')
    plt.tight_layout(pad=0)
    
    # Save the file
    save_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    plt.close()
    print(f"Saved: {filename}")

if __name__ == "__main__":
    print("Generating visual examples for the report...")

    # --- Letter A Examples ---
    save_example('A', 'shear_x', 30, "A_shear.png")
    save_example('A', 'base_width_factor', 1.6, "A_width.png")
    save_example('A', 'crossbar_h_shift', 30, "A_crossbar.png")
    save_example('A', 'top_width', 60, "A_top_width.png")

    # --- Letter B Examples ---
    save_example('B', 'vertical_squash', 0.6, "B_squash.png")
    save_example('B', 'waist_y_shift', -25, "B_waist.png")
    save_example('B', 'rotation_deg', 15, "B_rotation.png")

    # --- Letter C Examples ---
    save_example('C', 'cut_top', -10, "C_closed.png")
    save_example('C', 'cut_top', 70, "C_open.png")
    save_example('C', 'vertical_squash', 0.6, "C_squash.png")

    # --- Letter F Examples ---
    save_example('F', 'bar_length', 1.4, "F_bar_long.png")
    save_example('F', 'bar_length', 0.6, "F_bar_short.png")
    save_example('F', 'middle_bar_shift', 25, "F_mid_down.png")
    save_example('F', 'shear_x', 25, "F_shear.png")

    # --- Letter X Examples ---
    save_example('X', 'cross_ratio', 0.35, "X_cross_high.png")
    save_example('X', 'cross_ratio', 0.65, "X_cross_low.png")
    save_example('X', 'spread_angle', 15, "X_spread.png")
    save_example('X', 'rotation_deg', 25, "X_rotation.png")

    # --- Letter W Examples ---
    save_example('W', 'peak_depth', 0.85, "W_deep.png")
    save_example('W', 'peak_depth', 0.4, "W_shallow.png")
    save_example('W', 'width_factor', 1.3, "W_wide.png")
    save_example('W', 'middle_height', 0.35, "W_mid_low.png")
    
    print(f"\nDone! Please check the folder: {OUTPUT_DIR}")
