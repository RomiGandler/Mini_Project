import os
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters

# ==========================================
# SSIM Function
# ==========================================

def get_similarity(img1, img2):
    """
    SSIM - Structural Similarity Index
    RANGE: -1 to 1 (1 means identical)  
    """
    return ssim(img1, img2, data_range=img1.max() - img1.min())

# ==========================================
# Create Base Letters
# ==========================================

def create_base_letters():
    """Creates the three basic letters"""
    model = LetterSkeleton(size=(200, 200))
    
    CanonicalLetters.draw_A(model)
    base_A = model.apply_morphology(thickness=6).copy()
    
    CanonicalLetters.draw_B(model)
    base_B = model.apply_morphology(thickness=6).copy()
    
    CanonicalLetters.draw_C(model)
    base_C = model.apply_morphology(thickness=6).copy()
    
    return {'A': base_A, 'B': base_B, 'C': base_C}

# ==========================================
# Create Max Deformed Letters
# ==========================================

def create_max_deformed_letters():
    """Creates the three letters with maximum deformation"""
    model = LetterSkeleton(size=(200, 200))
    
    # A with maximum deformation
    CanonicalLetters.draw_A(model, 
                            top_width=140,           # Very round head  
                            base_width_factor=2.0,   # Very wide legs
                            crossbar_h_shift=50)     # Crossbar shifted down
    deformed_A = model.apply_morphology(thickness=6).copy()
    
    # B with maximum deformation
    CanonicalLetters.draw_B(model,
                            width_factor=0.5,        # Very thin
                            waist_y_shift=40,        # Waist shifted down
                            rotation_deg=-35)        # Rotated
    deformed_B = model.apply_morphology(thickness=6).copy()
    
    # C with maximum deformation
    CanonicalLetters.draw_C(model,
                            cut_top=-40,             # Closed
                            cut_bottom=-40,          # Closed
                            elongation_factor=1.6,   # Squished
                            rotation_deg=60)         # Rotated
    deformed_C = model.apply_morphology(thickness=6).copy()
    
    return {'A': deformed_A, 'B': deformed_B, 'C': deformed_C}

# ==========================================
# SSIM Matrix Creation
# ==========================================

def create_ssim_matrix(letters_dict):
    """Creates an SSIM matrix from a dictionary of letters"""
    letters = list(letters_dict.keys())
    n = len(letters)
    matrix = np.zeros((n, n))
    
    for i, letter1 in enumerate(letters):
        for j, letter2 in enumerate(letters):
            matrix[i, j] = get_similarity(letters_dict[letter1], letters_dict[letter2])
    
    return matrix

# ==========================================
# Compare Original Letters
# ==========================================

def compare_original_letters(base_letters, output_dir):
    """Compares original letters"""
    print("\n📊 Comparing Original Letters...")
    
    letters = list(base_letters.keys())
    n = len(letters)
    
    original_matrix = create_ssim_matrix(base_letters)

    # Create Visualization
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Inter-letter Comparison: Original Letters (SSIM)", fontsize=16)

    # Images
    axes[0].axis('off')
    axes[0].set_title("Original Letters", fontsize=14, fontweight='bold')
    for idx, letter in enumerate(letters):
        ax_small = fig.add_axes([0.08 + idx*0.11, 0.25, 0.09, 0.5])
        ax_small.imshow(base_letters[letter], cmap='gray')
        ax_small.set_title(f"{letter}", fontsize=14, fontweight='bold')
        ax_small.axis('off')

    # Matrix
    im = axes[1].imshow(original_matrix, cmap='RdYlGn', vmin=0, vmax=1)
    axes[1].set_title("SSIM Matrix - Original", fontsize=14)
    axes[1].set_xticks(range(n))
    axes[1].set_yticks(range(n))
    axes[1].set_xticklabels(letters, fontsize=12)
    axes[1].set_yticklabels(letters, fontsize=12)
    for i in range(n):
        for j in range(n):
            axes[1].text(j, i, f'{original_matrix[i,j]:.2f}', ha='center', va='center', fontsize=12, fontweight='bold')
    plt.colorbar(im, ax=axes[1])
    
    plt.tight_layout()
    filename = os.path.join(output_dir, "inter_letter_original.png")
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   Saved: {filename}")
    
    return original_matrix

# ==========================================
# Compare Deformed Letters
# ==========================================

def compare_deformed_letters(deformed_letters, output_dir):
    """Compares deformed letters"""
    print("\n📊 Comparing Max Deformed Letters...")
    
    letters = list(deformed_letters.keys())
    n = len(letters)
    
    deformed_matrix = create_ssim_matrix(deformed_letters)

    # Create Visualization
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Inter-letter Comparison: Max Deformed Letters (SSIM)", fontsize=16)

    # Images
    axes[0].axis('off')
    axes[0].set_title("Max Deformed Letters", fontsize=14, fontweight='bold')
    for idx, letter in enumerate(letters):
        ax_small = fig.add_axes([0.08 + idx*0.11, 0.25, 0.09, 0.5])
        ax_small.imshow(deformed_letters[letter], cmap='gray')
        ax_small.set_title(f"{letter}'", fontsize=14, fontweight='bold')
        ax_small.axis('off')

    # Matrix
    im = axes[1].imshow(deformed_matrix, cmap='RdYlGn', vmin=0, vmax=1)
    axes[1].set_title("SSIM Matrix - Max Deformed", fontsize=14)
    axes[1].set_xticks(range(n))
    axes[1].set_yticks(range(n))
    axes[1].set_xticklabels([f"{l}'" for l in letters], fontsize=12)
    axes[1].set_yticklabels([f"{l}'" for l in letters], fontsize=12)
    for i in range(n):
        for j in range(n):
            axes[1].text(j, i, f'{deformed_matrix[i,j]:.2f}', ha='center', va='center', fontsize=12, fontweight='bold')
    plt.colorbar(im, ax=axes[1])
    
    plt.tight_layout()
    filename = os.path.join(output_dir, "inter_letter_deformed.png")
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   Saved: {filename}")
    
    return deformed_matrix

# ==========================================
# Main
# ==========================================

def run_inter_letter_analysis(output_dir='analysis'):
    """Runs inter-letter comparison analysis"""
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("🚀 Starting Inter-letter Analysis...")

    # Create Letters
    base_letters = create_base_letters()
    deformed_letters = create_max_deformed_letters()

    # Compare Original Letters
    compare_original_letters(base_letters, output_dir)

    # Compare Deformed Letters
    compare_deformed_letters(deformed_letters, output_dir)
    
    print("\n✅ Inter-letter Analysis Complete!")

if __name__ == "__main__":
    run_inter_letter_analysis(output_dir='analysis')