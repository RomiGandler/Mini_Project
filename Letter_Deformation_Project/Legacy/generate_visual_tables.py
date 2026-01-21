import matplotlib.pyplot as plt
import os
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters

# ==============================
# Letter draw functions
# ==============================

DRAW_FUNCS = {
    'A': CanonicalLetters.draw_A,
    'B': CanonicalLetters.draw_B,
    'C': CanonicalLetters.draw_C,
    'F': CanonicalLetters.draw_F,
    'X': CanonicalLetters.draw_X,
    'W': CanonicalLetters.draw_W,
}

# ==============================
# Generate one row of deformations
# ==============================

def generate_row(model, letter_func, param_name, param_range, fixed_params=None):
    """
    Generate a list of images by varying a single parameter.
    """
    if fixed_params is None:
        fixed_params = {}

    images = []
    labels = []

    for val in param_range:
        model.clear()
        params = fixed_params.copy()
        params[param_name] = val
        letter_func(model, **params)
        img = model.apply_morphology(thickness=6)
        images.append(img)
        labels.append(str(val))

    return images, labels

# ==============================
# Create deformation table
# ==============================

def create_letter_table(letter_name, letter_func, param_configs, output_filename):
    """
    param_configs: list of (param_name, param_range, display_name)
    """
    model = LetterSkeleton(size=(200, 200))

    num_rows = len(param_configs)
    num_cols = max(len(param_range) for _, param_range, _ in param_configs)

    fig, axes = plt.subplots(
        num_rows, num_cols,
        figsize=(num_cols * 2.2, num_rows * 2.6)
    )

    fig.suptitle(
        f"Letter '{letter_name}': Parameter Deformations",
        fontsize=20,
        fontweight='bold'
    )

    for row_idx, (param_name, param_range, display_name) in enumerate(param_configs):
        images, labels = generate_row(model, letter_func, param_name, param_range)

        for col_idx, (img, label) in enumerate(zip(images, labels)):
            ax = axes[row_idx, col_idx]
            ax.imshow(img, cmap='gray')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title(label, fontsize=10)

            if col_idx == 0:
                ax.set_ylabel(
                    display_name,
                    fontsize=12,
                    fontweight='bold',
                    rotation=0,
                    ha='right',
                    va='center',
                    labelpad=50
                )

        # Hide unused cells
        for empty_col in range(len(images), num_cols):
            axes[row_idx, empty_col].axis('off')

    plt.tight_layout()
    plt.savefig(output_filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_filename}")

# ==============================
# Main
# ==============================

def main():
    os.makedirs('output', exist_ok=True)

    # ---- Letter A ----
    a_configs = [
        ('top_width', [0, 20, 40, 60, 80, 100], 'Top\nRound'),
        ('crossbar_h_shift', [-40, -20, 0, 20, 40], 'Bar\nShift'),
        ('base_width_factor', [0.5, 0.8, 1.0, 1.4, 1.8], 'Leg\nWidth'),
        ('shear_x', [-30, -15, 0, 15, 30], 'Shear'),
    ]
    create_letter_table('A', CanonicalLetters.draw_A, a_configs, 'output/table_A.png')

    # ---- Letter B ----
    b_configs = [
        ('waist_y_shift', [-30, -15, 0, 15, 30], 'Waist\nShift'),
        ('width_factor', [0.6, 0.8, 1.0, 1.3, 1.6], 'Width'),
        ('rotation_deg', [-20, -10, 0, 10, 20], 'Rotation'),
        ('vertical_squash', [0.4, 0.6, 0.8, 1.0], 'Squash'),
    ]
    create_letter_table('B', CanonicalLetters.draw_B, b_configs, 'output/table_B.png')

    # ---- Letter C ----
    c_configs = [
        ('cut_top', [-20, 0, 20, 40, 60, 80], 'Cut\nTop'),
        ('vertical_squash', [0.4, 0.6, 0.8, 1.0], 'Squash'),
        ('rotation_deg', [-30, -15, 0, 15, 30], 'Rotation'),
    ]
    create_letter_table('C', CanonicalLetters.draw_C, c_configs, 'output/table_C.png')

    # ---- Letter F ----
    f_configs = [
        ('bar_length', [0.5, 0.75, 1.0, 1.25, 1.5], 'Bar\nLength'),
        ('middle_bar_shift', [-30, -15, 0, 15, 30], 'Mid Bar\nShift'),
        ('shear_x', [-30, -15, 0, 15, 30], 'Shear'),
        ('spine_height', [0.6, 0.8, 1.0, 1.2], 'Spine\nHeight'),
    ]
    create_letter_table('F', CanonicalLetters.draw_F, f_configs, 'output/table_F.png')

    # ---- Letter X ----
    x_configs = [
        ('cross_ratio', [0.3, 0.4, 0.5, 0.6, 0.7], 'Cross\nPos'),
        ('spread_angle', [-20, -10, 0, 10, 20], 'Spread'),
        ('rotation_deg', [-30, -15, 0, 15, 30], 'Rotation'),
        ('asymmetry', [-20, -10, 0, 10, 20], 'Asymmetry'),
    ]
    create_letter_table('X', CanonicalLetters.draw_X, x_configs, 'output/table_X.png')

    # ---- Letter W ----
    w_configs = [
        ('peak_depth', [0.3, 0.5, 0.7, 0.9], 'Peak\nDepth'),
        ('width_factor', [0.6, 0.8, 1.0, 1.2, 1.4], 'Width'),
        ('middle_height', [0.3, 0.5, 0.7], 'Mid\nHeight'),
        ('shear_x', [-25, -12, 0, 12, 25], 'Shear'),
    ]
    create_letter_table('W', CanonicalLetters.draw_W, w_configs, 'output/table_W.png')

    print("\n✅ All visual tables generated successfully!")

if __name__ == "__main__":
    main()
