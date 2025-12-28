import matplotlib.pyplot as plt
import os
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters

# יצירת תיקיית פלט אם לא קיימת
if not os.path.exists('output'):
    os.makedirs('output')

def main():
    # 1. יצירת המודל הגרפי (המכחול)
    model = LetterSkeleton(size=(200, 200))
    
    # 2. מיפוי האותיות לפונקציות הציור שלהן
    letters_map = {
        'A': CanonicalLetters.draw_A,
        'B': CanonicalLetters.draw_B,
        'C': CanonicalLetters.draw_C
    }
    
    # הגדרת הגרף לתצוגה
    plt.figure(figsize=(10, 6))
    plt.suptitle("Milestone 1: Canonical Letter Representation (A, B, C)", fontsize=16)
    
    for i, (name, draw_func) in enumerate(letters_map.items()):
        # -- שלב א': ציור השלד --
        draw_func(model)
        skeleton_img = model.get_skeleton()
        
        # -- שלב ב': עיבוי (מורפולוגיה) --
        final_img = model.apply_morphology(thickness=6)
        
        # שמירת התמונות לתיקייה
        plt.imsave(f'output/base_{name}.png', final_img, cmap='gray')
        
        # הצגה בגרף
        # שורה עליונה - שלדים
        plt.subplot(2, 3, i + 1)
        plt.title(f"Skeleton {name}")
        plt.imshow(skeleton_img, cmap='gray')
        plt.axis('off')
        
        # שורה תחתונה - תוצאה סופית
        plt.subplot(2, 3, i + 4)
        plt.title(f"Final Shape {name}")
        plt.imshow(final_img, cmap='gray')
        plt.axis('off')

    plt.tight_layout()
    plt.show()
    print("Success! Check the 'output' folder for images.")

if __name__ == "__main__":
    main()