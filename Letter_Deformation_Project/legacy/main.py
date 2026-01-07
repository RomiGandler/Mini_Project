import matplotlib.pyplot as plt
import os
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters

# Create output directory if it doesn't exist
if not os.path.exists('output'):
    os.makedirs('output')

def main():
    # 1. Create the graphic model (the brush)
    model = LetterSkeleton(size=(200, 200))

    # 2. Map letters to their drawing functions
    letters_map = {
        'A': CanonicalLetters.draw_A,
        'B': CanonicalLetters.draw_B,
        'C': CanonicalLetters.draw_C
    }
    
    # Define figure for displaying results
    plt.figure(figsize=(10, 6))
    plt.suptitle("Milestone 1: Canonical Letter Representation (A, B, C)", fontsize=16)
    
    for i, (name, draw_func) in enumerate(letters_map.items()):
        # -- Step 1: Draw the skeleton --
        draw_func(model)
        skeleton_img = model.get_skeleton()

        # -- Step 2: Apply morphology (thickening) --
        final_img = model.apply_morphology(thickness=6)

        # Save images to directory
        plt.imsave(f'output/base_{name}.png', final_img, cmap='gray')

        # Display in graph
        # Top row - skeletons
        plt.subplot(2, 3, i + 1)
        plt.title(f"Skeleton {name}")
        plt.imshow(skeleton_img, cmap='gray')
        plt.axis('off')

        # -- Bottom row - final results
        plt.subplot(2, 3, i + 4)
        plt.title(f"Final Shape {name}")
        plt.imshow(final_img, cmap='gray')
        plt.axis('off')

    plt.tight_layout()
    plt.show()
    print("Success! Check the 'output' folder for images.")

if __name__ == "__main__":
    main()