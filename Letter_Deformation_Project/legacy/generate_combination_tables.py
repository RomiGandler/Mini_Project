import matplotlib.pyplot as plt
import numpy as np
import os
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters

def generate_combination_row(model, letter_func, param1_name, param1_val, param2_name, param2_range):
    """Generate a row of images with one parameter fixed and the other varying"""
    images = []
    labels = []
    
    for val2 in param2_range:
        params = {param1_name: param1_val, param2_name: val2}
        letter_func(model, **params)
        img = model.apply_morphology(thickness=6)
        images.append(img)
        labels.append(f"{val2}")
    
    return images, labels

def create_combination_table(letter_name, letter_func, combinations, output_filename, cols=10):
    """
    Create a table of combinations
    combinations: List of tuples: (param1_name, param1_value, param2_name, param2_range, display_name)
    """
    model = LetterSkeleton(size=(200, 200))
    
    num_rows = len(combinations)
    
    fig, axes = plt.subplots(num_rows, cols, figsize=(cols * 1.8, num_rows * 2.2))
    fig.suptitle(f"Letter '{letter_name}': Combined Deformations", fontsize=18, fontweight='bold')
    
    for row_idx, (p1_name, p1_val, p2_name, p2_range, display_name) in enumerate(combinations):
        images, labels = generate_combination_row(model, letter_func, p1_name, p1_val, p2_name, p2_range)
        
        for col_idx in range(cols):
            ax = axes[row_idx, col_idx] if num_rows > 1 else axes[col_idx]
            
            if col_idx < len(images):
                ax.imshow(images[col_idx], cmap='gray')
                ax.set_title(f"{p2_name[:3]}={labels[col_idx]}", fontsize=7)
            
            ax.set_xticks([])
            ax.set_yticks([])
            
            if col_idx == 0:
                ax.set_ylabel(display_name, fontsize=9, fontweight='bold', rotation=0, 
                            ha='right', va='center', labelpad=60)
    
    plt.tight_layout()
    plt.savefig(output_filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_filename}")

def main():
    if not os.path.exists('combinations'):
        os.makedirs('combinations')

    # === Combinations for Letter A ===
    # Parameters: top_width, crossbar_h_shift, base_width_factor
    a_combinations = [
        # Round + Base Width
        ('top_width', 0, 'base_width_factor', [0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0, 2.2, 2.4], 'Round=0\n+Width'),
        ('top_width', 60, 'base_width_factor', [0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0, 2.2, 2.4], 'Round=60\n+Width'),
        ('top_width', 120, 'base_width_factor', [0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0, 2.2, 2.4], 'Round=120\n+Width'),
        # Round + Crossbar Shift
        ('top_width', 0, 'crossbar_h_shift', [-50, -35, -20, -10, 0, 10, 20, 35, 50, 60], 'Round=0\n+Bar'),
        ('top_width', 60, 'crossbar_h_shift', [-50, -35, -20, -10, 0, 10, 20, 35, 50, 60], 'Round=60\n+Bar'),
        ('top_width', 120, 'crossbar_h_shift', [-50, -35, -20, -10, 0, 10, 20, 35, 50, 60], 'Round=120\n+Bar'),
        # Width + Crossbar Shift
        ('base_width_factor', 0.5, 'crossbar_h_shift', [-50, -35, -20, -10, 0, 10, 20, 35, 50, 60], 'Width=0.5\n+Bar'),
        ('base_width_factor', 1.5, 'crossbar_h_shift', [-50, -35, -20, -10, 0, 10, 20, 35, 50, 60], 'Width=1.5\n+Bar'),
    ]
    create_combination_table('A', CanonicalLetters.draw_A, a_combinations, 'combinations/table_A_combinations.png')
    
    # === Combinations for Letter B ===
    # Parameters: waist_y_shift, width_factor, rotation_deg
    b_combinations = [
        # Waist + Width
        ('waist_y_shift', -30, 'width_factor', [0.4, 0.6, 0.8, 1.0, 1.3, 1.6, 1.9, 2.2, 2.5, 2.8], 'Waist=-30\n+Width'),
        ('waist_y_shift', 0, 'width_factor', [0.4, 0.6, 0.8, 1.0, 1.3, 1.6, 1.9, 2.2, 2.5, 2.8], 'Waist=0\n+Width'),
        ('waist_y_shift', 30, 'width_factor', [0.4, 0.6, 0.8, 1.0, 1.3, 1.6, 1.9, 2.2, 2.5, 2.8], 'Waist=30\n+Width'),
        # Waist + Rotation
        ('waist_y_shift', -30, 'rotation_deg', [-35, -25, -15, -5, 0, 5, 15, 25, 35, 40], 'Waist=-30\n+Rot'),
        ('waist_y_shift', 0, 'rotation_deg', [-35, -25, -15, -5, 0, 5, 15, 25, 35, 40], 'Waist=0\n+Rot'),
        ('waist_y_shift', 30, 'rotation_deg', [-35, -25, -15, -5, 0, 5, 15, 25, 35, 40], 'Waist=30\n+Rot'),
        # Width + Rotation
        ('width_factor', 0.6, 'rotation_deg', [-35, -25, -15, -5, 0, 5, 15, 25, 35, 40], 'Width=0.6\n+Rot'),
        ('width_factor', 1.8, 'rotation_deg', [-35, -25, -15, -5, 0, 5, 15, 25, 35, 40], 'Width=1.8\n+Rot'),
    ]
    create_combination_table('B', CanonicalLetters.draw_B, b_combinations, 'combinations/table_B_combinations.png')

    # === Combinations for Letter C ===
    # Parameters: cut_top, cut_bottom, elongation_factor, rotation_deg
    c_combinations = [
        # Cut Top + Elongation
        ('cut_top', -30, 'elongation_factor', [0.5, 0.7, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2], 'CutTop=-30\n+Elong'),
        ('cut_top', 40, 'elongation_factor', [0.5, 0.7, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2], 'CutTop=40\n+Elong'),
        ('cut_top', 80, 'elongation_factor', [0.5, 0.7, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2], 'CutTop=80\n+Elong'),
        # Cut Top + Rotation
        ('cut_top', -30, 'rotation_deg', [-60, -40, -20, -10, 0, 10, 20, 40, 60, 80], 'CutTop=-30\n+Rot'),
        ('cut_top', 40, 'rotation_deg', [-60, -40, -20, -10, 0, 10, 20, 40, 60, 80], 'CutTop=40\n+Rot'),
        # Elongation + Rotation
        ('elongation_factor', 0.6, 'rotation_deg', [-60, -40, -20, -10, 0, 10, 20, 40, 60, 80], 'Elong=0.6\n+Rot'),
        ('elongation_factor', 1.0, 'rotation_deg', [-60, -40, -20, -10, 0, 10, 20, 40, 60, 80], 'Elong=1.0\n+Rot'),
        ('elongation_factor', 1.6, 'rotation_deg', [-60, -40, -20, -10, 0, 10, 20, 40, 60, 80], 'Elong=1.6\n+Rot'),
    ]
    create_combination_table('C', CanonicalLetters.draw_C, c_combinations, 'combinations/table_C_combinations.png')
    
    print("\n✅ All combination tables generated!")

if __name__ == "__main__":
    main()