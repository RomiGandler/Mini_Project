import matplotlib.pyplot as plt
import numpy as np
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters
from skimage.metrics import structural_similarity as ssim

def measure_similarity(img1, img2):
    return ssim(img1, img2, data_range=img1.max() - img1.min())

def run_complex_deformation(letter_func, deformation_logic, steps=100):
    model = LetterSkeleton(size=(200, 200))
    
    # 1. יצירת תמונת המקור (t=0) - הקנונית המושלמת
    base_params = deformation_logic(0.0) 
    letter_func(model, **base_params)
    base_image = model.apply_morphology(thickness=6)
    
    t_values = []
    similarity_scores = []
    vis_images = []
    
    # נשמור 5 תמונות שמייצגות את התהליך (0, 0.25, 0.5, 0.75, 1.0)
    vis_indices = [0, int(steps*0.25), int(steps*0.5), int(steps*0.75), steps] 

    print(f"--- Running analysis for {letter_func.__name__} ---")
    
    for i in range(steps + 1):
        t = i / steps # t בין 0 ל-1
        
        current_params = deformation_logic(t)
        
        letter_func(model, **current_params)
        distorted_img = model.apply_morphology(thickness=6)
        
        score = measure_similarity(base_image, distorted_img)
        
        t_values.append(t)
        similarity_scores.append(score)
        
        if i in vis_indices:
            vis_images.append((t, distorted_img, score))

    return t_values, similarity_scores, vis_images

# --- הגדרת הדפורמציות עם נקודת התחלה מתוקנת ---

def deformation_A_stretch(t):
    """
    מקור (t=0): A קלאסית עם שפיץ (כמו בתמונה image_0cbf5a)
    יעד (t=1): A רחבה מאוד עם ראש שטוח ("אוהל")
    """
    return {
        # ב-t=0 זה השפיץ המושלם (0). ב-t=1 זה שטוח (120)
        'top_width': int(0 + (120 * t)),       
        
        # ב-t=0 רוחב סטנדרטי (1.0). ב-t=1 רחב מאוד (2.5)
        'base_width_factor': 1.0 + (1.5 * t),  
        
        # הקו האמצעי יורד קצת למטה ככל שהאות נמתחת
        'crossbar_h_shift': int(0 + (40 * t))  
    }

def deformation_B_squeeze(t):
    """
    מקור (t=0): B קלאסית ישרה (כמו בתמונה image_0cbf5f)
    יעד (t=1): B דקיקה מאוד ("מתוחה") ונטויה
    """
    return {
        # ב-t=0 רוחב 1.0. ב-t=1 רוחב 0.4 (דקיק)
        'width_factor': 1.0 + (-0.6 * t),      
        
        # ב-t=0 המותן במרכז. ב-t=1 המותן עולה למעלה
        'waist_y_shift': int(0 + (50 * t)),    
        
        # ב-t=0 ישרה. ב-t=1 נטויה
        'rotation_deg': int(0 - (15 * t))      
    }

def deformation_C_crush(t):
    """
    מקור (t=0): C פתוחה וסימטרית (כמו בתמונה image_0cbf79)
    יעד (t=1): C סגורה, מעוכה ומסובבת
    """
    return {
        # ב-t=0 הפתח הוא 60 (פתוח יפה). ב-t=1 הפתח הוא -30 (סגור וחופף)
        'cut_top': int(60 + (-90 * t)),        
        'cut_bottom': int(60 + (-90 * t)),     
        
        # ב-t=0 עגולה (1.0). ב-t=1 פחוסה (1.6)
        'elongation_factor': 1.0 + (0.6 * t),  
        
        # סיבוב קל
        'rotation_deg': 0 + (30 * t)           
    }

def plot_analysis(t_vals, scores, vis_images, title, filename):
    plt.figure(figsize=(14, 8))
    
    # צד שמאל: הגרף
    plt.subplot(1, 2, 1)
    plt.plot(t_vals, scores, linewidth=3, color='blue')
    
    # קו סף אדום (סתם כדוגמה, אפשר לשנות)
    plt.axhline(y=0.75, color='r', linestyle='--', label='Similarity Threshold (0.75)')
    
    plt.title(f'Similarity Drop: {title}', fontsize=16)
    plt.xlabel('Deformation Intensity (t)', fontsize=12)
    plt.ylabel('SSIM Score (Similarity)', fontsize=12)
    plt.ylim(0, 1.1) # כדי שנראה את כל הטווח
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # צד ימין: הצגת התמונות
    plt.subplot(1, 2, 2)
    plt.axis('off')
    plt.title("Visual Progression", fontsize=14)
    
    # הצגת 5 תמונות בטור
    for idx, (t_snap, img, score) in enumerate(vis_images):
        # חישוב מיקום ידני כדי שייראה יפה
        y_pos = 0.8 - (idx * 0.18) 
        
        # יצירת ציר קטן לתמונה
        ax = plt.axes([0.60, y_pos, 0.15, 0.15]) 
        ax.imshow(img, cmap='gray')
        ax.axis('off')
        
        # הוספת טקסט ליד כל תמונה
        plt.figtext(0.76, y_pos + 0.07, f"t={t_snap:.2f}", fontsize=10, fontweight='bold')
        plt.figtext(0.76, y_pos + 0.04, f"Score: {score:.2f}", fontsize=9)

    plt.savefig(filename)
    print(f"Saved graph: {filename}")
    plt.close()

if __name__ == "__main__":
    # 1. הרצת האות A
    t, scores, visuals = run_complex_deformation(
        CanonicalLetters.draw_A, 
        deformation_A_stretch, 
        steps=100
    )
    plot_analysis(t, scores, visuals, "A Deformation (Stretch)", "analysis_A_corrected.png")

    # 2. הרצת האות B
    t, scores, visuals = run_complex_deformation(
        CanonicalLetters.draw_B, 
        deformation_B_squeeze, 
        steps=100
    )
    plot_analysis(t, scores, visuals, "B Deformation (Squeeze)", "analysis_B_corrected.png")

    # 3. הרצת האות C
    t, scores, visuals = run_complex_deformation(
        CanonicalLetters.draw_C, 
        deformation_C_crush, 
        steps=100
    )
    plot_analysis(t, scores, visuals, "C Deformation (Crush)", "analysis_C_corrected.png")