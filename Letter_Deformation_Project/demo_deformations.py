import matplotlib.pyplot as plt
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters

def show_deformations():
    # יצירת המודל הגרפי
    model = LetterSkeleton(size=(200, 200))
    
    # נגדיר רשימה של עיוותים שאנחנו רוצים לבדוק על האות A
    # המבנה של כל פריט: (כותרת לתצוגה, רוחב_החלק_העליון, הזזת_קו_אמצע)
    configs = [
        ("Base A (Canonical)", 0, 0),
        ("Round Top (Level 1)", 40, 0),     # שינינו את השם
        ("Round Top (Level 2)", 80, 0),     # שינינו את השם
        ("Crossbar Up", 0, -30),
        ("Crossbar Down", 0, 30),
        ("Mixed: Round + Down", 60, 20)     # שינינו את השם
    ]
    
    # הגדרת הגודל של החלון שייפתח
    plt.figure(figsize=(15, 8))
    plt.suptitle("Deformation Analysis for Letter A", fontsize=16)
    
    for i, (title, top_w, bar_h) in enumerate(configs):
        # 1. ציור האות עם הפרמטרים הספציפיים
        # אנחנו קוראים לפונקציה שעדכנו ב-base_letters.py
        CanonicalLetters.draw_A(model, top_width=top_w, crossbar_h_shift=bar_h)
        
        # 2. קבלת התמונה המעובה (אחרי המורפולוגיה)
        img = model.apply_morphology(thickness=6)
        
        # 3. הצגה בגרף
        plt.subplot(2, 3, i+1)
        plt.imshow(img, cmap='gray')
        plt.title(f"{title}\ntop_width={top_w}, shift={bar_h}")
        plt.axis('off')
        
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    show_deformations()