import matplotlib.pyplot as plt
import numpy as np
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters

def generate_row(model, letter_func, param_name, param_range, fixed_params={}):
    """
    Create a row of images by varying one parameter while keeping others fixed.
    """
    images = []
    labels = []
    
    for val in param_range:
        params = fixed_params.copy()
        params[param_name] = val
        letter_func(model, **params)
        img = model.apply_morphology(thickness=6)
        images.append(img)
        labels.append(f"{val}")
    
    return images, labels

def create_letter_table(letter_name, letter_func, param_configs, output_filename):
    """
    Create a table of letter deformations for given parameters.
    param_configs: List of tuples: (param_name, param_range, display_name)
    """
    model = LetterSkeleton(size=(200, 200))
    
    num_rows = len(param_configs)
    num_cols = len(param_configs[0][1])  # Number of values in the range
    
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(num_cols * 2, num_rows * 2.5))
    fig.suptitle(f"Letter '{letter_name}': All Deformations", fontsize=20, fontweight='bold')
    
    for row_idx, (param_name, param_range, display_name) in enumerate(param_configs):
        images, labels = generate_row(model, letter_func, param_name, param_range)
        
        for col_idx, (img, label) in enumerate(zip(images, labels)):
            ax = axes[row_idx, col_idx] if num_rows > 1 else axes[col_idx]
            ax.imshow(img, cmap='gray')
            ax.set_xticks([])
            ax.set_yticks([])
            # Top title only for the first row
            if row_idx == 0:
                ax.set_title(label, fontsize=10)
            else:
                ax.set_title(label, fontsize=10)

            # Parameter name on the left only for the first column
            if col_idx == 0:
                ax.set_ylabel(display_name, fontsize=12, fontweight='bold', rotation=0, 
                            ha='right', va='center', labelpad=50)
    
    plt.tight_layout()
    plt.savefig(output_filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_filename}")

def main():
    import os
    if not os.path.exists('output'):
        os.makedirs('output')
    # === Table for Letter A ===
    a_configs = [
        ('top_width', [0, 20, 40, 60, 80, 100, 120, 140], 'Top\nRound'),
        ('crossbar_h_shift', [-50, -35, -20, 0, 20, 35, 50, 60], 'Bar\nShift'),
        ('base_width_factor', [0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0], 'Leg\nWidth'),
    ]
    create_letter_table('A', CanonicalLetters.draw_A, a_configs, 'output/table_A.png')    
    # === Table for Letter B ===
    b_configs = [
        ('waist_y_shift', [-40, -25, -10, 0, 10, 25, 40, 50], 'Waist\nShift'),
        ('width_factor', [0.4, 0.6, 0.8, 1.0, 1.3, 1.6, 1.9, 2.2], 'Width'),
        ('rotation_deg', [-20, -14, -7, 0, 7, 14, 20, 25], 'Rotation'),
    ]
    create_letter_table('B', CanonicalLetters.draw_B, b_configs, 'output/table_B.png')

    # === Table for Letter C ===
    c_configs = [
        ('cut_top', [-40, -20, 0, 20, 40, 60, 80, 100], 'Cut\nTop'),
        ('cut_bottom', [-40, -20, 0, 20, 40, 60, 80, 100], 'Cut\nBottom'),
        ('elongation_factor', [0.5, 0.7, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8], 'Elongation'),
        ('rotation_deg', [-60, -40, -20, 0, 20, 40, 60, 80], 'Rotation'),
    ]
    create_letter_table('C', CanonicalLetters.draw_C, c_configs, 'output/table_C.png')
    
    print("\n✅ All tables generated!")

if __name__ == "__main__":
    main()