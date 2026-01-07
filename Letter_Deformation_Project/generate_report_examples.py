import os
import matplotlib.pyplot as plt
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters
from src.param_config import PARAM_CONFIG

# Configuration for the output directory
OUTPUT_DIR = "results/report_examples"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_example(letter, param_name, param_value, filename):
    """
    Generates and saves a letter image with a single modified parameter.
    Used for creating visual examples for the methodology section.
    """
    # Initialize the skeleton model
    model = LetterSkeleton(size=(200, 200))
    
    # Load default parameters from the central configuration
    params = {k: v['default'] for k, v in PARAM_CONFIG[letter].items()}
    
    # Update the specific parameter for demonstration purposes
    params[param_name] = param_value
    
    # Draw the specific letter based on the input char
    if letter == 'A':
        CanonicalLetters.draw_A(model, **params)
    elif letter == 'B':
        CanonicalLetters.draw_B(model, **params)
    elif letter == 'C':
        CanonicalLetters.draw_C(model, **params)
        
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
    # 1. Strong Shear (Tilt)
    save_example('A', 'shear_x', 30, "A_shear.png")
    # 2. Significant Widening
    save_example('A', 'base_width_factor', 1.6, "A_width.png")
    # 3. Lower Crossbar position
    save_example('A', 'crossbar_h_shift', 30, "A_crossbar.png")
    # 4. Wide Top (Flat head A)
    save_example('A', 'top_width', 60, "A_top_width.png")

    # --- Letter B Examples ---
    # 1. Vertical Squash (Flattening)
    save_example('B', 'vertical_squash', 0.6, "B_squash.png")
    # 2. High Waist (Shifted middle intersection)
    save_example('B', 'waist_y_shift', -30, "B_waist.png")
    # 3. Rotation
    save_example('B', 'rotation_deg', 15, "B_rotation.png")

    # --- Letter C Examples ---
    # 1. Closed Shape (Almost like 'O')
    save_example('C', 'cut_top', -10, "C_closed.png")
    # 2. Wide Opening
    save_example('C', 'cut_top', 70, "C_open.png")
    # 3. Vertical Squash
    save_example('C', 'vertical_squash', 0.6, "C_squash.png")
    
    print(f"\nDone! Please check the folder: {OUTPUT_DIR}")