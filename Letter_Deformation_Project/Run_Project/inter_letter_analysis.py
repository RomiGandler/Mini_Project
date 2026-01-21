import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim

# --- PATH CONFIGURATION START ---
# Getting the current script directory and parent directory to access 'src'
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
# --- PATH CONFIGURATION END ---

from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters

# Central analysis directory for similarity matrices
OUTPUT_DIR = os.path.join(parent_dir, "analysis", "inter_letter")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_similarity(img1, img2):
    """
    Calculates the Structural Similarity Index (SSIM) between two letter images.
    Range: 0.0 to 1.0 (1.0 means identical).
    """
    d_range = img1.max() - img1.min()
    if d_range == 0: d_range = 1.0
    return ssim(img1, img2, data_range=d_range)

def create_base_letters():
    """
    Generates the 6 canonical base letters (A, B, C, F, X, W) 
    using default parameters for comparison.
    """
    model = LetterSkeleton(size=(200, 200))
    letters = {}
    
    # Mapping characters to their drawing functions in src.base_letters
    draw_methods = {
        'A': CanonicalLetters.draw_A, 'B': CanonicalLetters.draw_B,
        'C': CanonicalLetters.draw_C, 'F': CanonicalLetters.draw_F,
        'X': CanonicalLetters.draw_X, 'W': CanonicalLetters.draw_W
    }
    
    for char, func in draw_methods.items():
        model.clear()
        # Drawing with default thickness
        func(model, thickness=6)
        # Apply morphology to get the final binary image
        letters[char] = model.apply_morphology(thickness=6).copy()
        
    return letters

def run_matrix_analysis():
    """
    Performs a cross-comparison between all letters to create a similarity matrix.
    Saves the resulting heatmap to the analysis folder.
    """
    print("🚀 Running Inter-letter Similarity Analysis...")
    
    base_letters = create_base_letters()
    char_list = list(base_letters.keys())
    n = len(char_list)
    matrix = np.zeros((n, n))
    
    # Nested loops to compare every letter with every other letter
    for i, char1 in enumerate(char_list):
        for j, char2 in enumerate(char_list):
            matrix[i, j] = get_similarity(base_letters[char1], base_letters[char2])

    # Visualization using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 8))
    # Using 'RdYlGn' colormap (Red for different, Green for similar)
    im = ax.imshow(matrix, cmap='RdYlGn', vmin=0, vmax=1)
    
    ax.set_title("Inter-letter Similarity Matrix (SSIM)", fontsize=14, fontweight='bold')
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(char_list)
    ax.set_yticklabels(char_list)
    
    # Adding numeric labels to each cell in the matrix
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f'{matrix[i,j]:.2f}', ha='center', va='center', 
                    fontweight='bold', color='black')
            
    plt.colorbar(im, label='SSIM Score (1.0 = Perfect Match)')
    
    # Saving the output to the dedicated analysis folder
    save_path = os.path.join(OUTPUT_DIR, "similarity_matrix.png")
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Inter-letter similarity matrix saved to: {save_path}")

if __name__ == "__main__":
    run_matrix_analysis()