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
# Create Base Letters (now including F, X, W)
# ==========================================

def create_base_letters():
    """Creates all six basic letters"""
    model = LetterSkeleton(size=(200, 200))
    
    CanonicalLetters.draw_A(model)
    base_A = model.apply_morphology(thickness=6).copy()
    
    CanonicalLetters.draw_B(model)
    base_B = model.apply_morphology(thickness=6).copy()
    
    CanonicalLetters.draw_C(model)
    base_C = model.apply_morphology(thickness=6).copy()
    
    CanonicalLetters.draw_F(model)
    base_F = model.apply_morphology(thickness=6).copy()
    
    CanonicalLetters.draw_X(model)
    base_X = model.apply_morphology(thickness=6).copy()
    
    CanonicalLetters.draw_W(model)
    base_W = model.apply_morphology(thickness=6).copy()
    
    return {'A': base_A, 'B': base_B, 'C': base_C, 'F': base_F, 'X': base_X, 'W': base_W}

# ==========================================
# Create Max Deformed Letters
# ==========================================

def create_max_deformed_letters():
    """Creates all six letters with maximum deformation"""
    model = LetterSkeleton(size=(200, 200))
    
    # A with maximum deformation
    CanonicalLetters.draw_A(model, 
                            top_width=80,
                            base_width_factor=1.8,
                            crossbar_h_shift=30,
                            shear_x=30)
    deformed_A = model.apply_morphology(thickness=6).copy()
    
    # B with maximum deformation
    CanonicalLetters.draw_B(model,
                            width_factor=0.6,
                            waist_y_shift=25,
                            rotation_deg=-15,
                            vertical_squash=0.5)
    deformed_B = model.apply_morphology(thickness=6).copy()
    
    # C with maximum deformation
    CanonicalLetters.draw_C(model,
                            cut_top=-15,
                            vertical_squash=0.5,
                            rotation_deg=25)
    deformed_C = model.apply_morphology(thickness=6).copy()
    
    # F with maximum deformation
    CanonicalLetters.draw_F(model,
                            bar_length=1.4,
                            middle_bar_shift=25,
                            shear_x=25,
                            spine_height=0.7)
    deformed_F = model.apply_morphology(thickness=6).copy()
    
    # X with maximum deformation
    CanonicalLetters.draw_X(model,
                            cross_ratio=0.35,
                            spread_angle=15,
                            rotation_deg=25,
                            asymmetry=15)
    deformed_X = model.apply_morphology(thickness=6).copy()
    
    # W with maximum deformation
    CanonicalLetters.draw_W(model,
                            peak_depth=0.85,
                            width_factor=1.3,
                            middle_height=0.35,
                            shear_x=20)
    deformed_W = model.apply_morphology(thickness=6).copy()
    
    return {'A': deformed_A, 'B': deformed_B, 'C': deformed_C, 
            'F': deformed_F, 'X': deformed_X, 'W': deformed_W}

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

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Inter-letter Comparison: Original Letters (SSIM)", fontsize=16)

    # Images
    axes[0].axis('off')
    axes[0].set_title("Original Letters", fontsize=14, fontweight='bold')
    for idx, letter in enumerate(letters):
        ax_small = fig.add_axes([0.05 + idx*0.065, 0.25, 0.055, 0.5])
        ax_small.imshow(base_letters[letter], cmap='gray')
        ax_small.set_title(f"{letter}", fontsize=12, fontweight='bold')
        ax_small.axis('off')

    # Matrix
    im = axes[1].imshow(original_matrix, cmap='RdYlGn', vmin=0, vmax=1)
    axes[1].set_title("SSIM Matrix - Original", fontsize=14)
    axes[1].set_xticks(range(n))
    axes[1].set_yticks(range(n))
    axes[1].set_xticklabels(letters, fontsize=10)
    axes[1].set_yticklabels(letters, fontsize=10)
    for i in range(n):
        for j in range(n):
            axes[1].text(j, i, f'{original_matrix[i,j]:.2f}', ha='center', va='center', fontsize=9, fontweight='bold')
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

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Inter-letter Comparison: Max Deformed Letters (SSIM)", fontsize=16)

    # Images
    axes[0].axis('off')
    axes[0].set_title("Max Deformed Letters", fontsize=14, fontweight='bold')
    for idx, letter in enumerate(letters):
        ax_small = fig.add_axes([0.05 + idx*0.065, 0.25, 0.055, 0.5])
        ax_small.imshow(deformed_letters[letter], cmap='gray')
        ax_small.set_title(f"{letter}'", fontsize=12, fontweight='bold')
        ax_small.axis('off')

    # Matrix
    im = axes[1].imshow(deformed_matrix, cmap='RdYlGn', vmin=0, vmax=1)
    axes[1].set_title("SSIM Matrix - Max Deformed", fontsize=14)
    axes[1].set_xticks(range(n))
    axes[1].set_yticks(range(n))
    axes[1].set_xticklabels([f"{l}'" for l in letters], fontsize=10)
    axes[1].set_yticklabels([f"{l}'" for l in letters], fontsize=10)
    for i in range(n):
        for j in range(n):
            axes[1].text(j, i, f'{deformed_matrix[i,j]:.2f}', ha='center', va='center', fontsize=9, fontweight='bold')
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
    
    print("🚀 Starting Inter-letter Analysis (A, B, C, F, X, W)...")

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
