import os
import matplotlib.pyplot as plt
import numpy as np
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters
from skimage.metrics import structural_similarity as ssim

def get_similarity(img1, img2):
    return ssim(img1, img2, data_range=img1.max() - img1.min())

def run_experiment(param_name, start_val, end_val, total_steps=300, num_snapshots=15):
    """
    מריץ ניסוי של 300 צעדים לגרף, ושולף 15 תמונות לתצוגה.
    """
    model = LetterSkeleton(size=(200, 200))
    base_defaults = {'base_width_factor': 1.0, 'top_width': 0, 'crossbar_h_shift': 0}
    
    # יצירת מקור
    CanonicalLetters.draw_A(model, **base_defaults)
    ref_image = model.apply_morphology(thickness=6)
    
    scores = []
    t_values = []
    snapshots_data = []
    
    # חישוב האינדקסים המדויקים של 15 התמונות שנרצה לשמור
    # np.linspace יוצר סדרה של מספרים במרווחים שווים מ-0 ועד הסוף
    snapshot_indices = np.linspace(0, total_steps, num_snapshots, dtype=int)
    
    print(f"Testing {param_name} ({total_steps} steps)...")
    
    for i in range(total_steps + 1):
        t = i / total_steps
        current_val = start_val + (end_val - start_val) * t
        
        current_params = base_defaults.copy()
        
        # טיפול ב-int/float ופורמט לכיתוב קצר
        if 'factor' in param_name:
            current_params[param_name] = current_val
            # כיתוב קצר לגריד
            label_val = f"{current_val:.2f}"
        else:
            val_val = int(current_val)
            current_params[param_name] = val_val
            label_val = f"{val_val}px"
        
        CanonicalLetters.draw_A(model, **current_params)
        test_img = model.apply_morphology(thickness=6)
        
        score = get_similarity(ref_image, test_img)
        scores.append(score)
        t_values.append(t)
        
        # שמירת תמונה אם זה אחד מ-15 האינדקסים הנבחרים
        if i in snapshot_indices:
            snapshots_data.append({
                'image': test_img,
                'score': score,
                'label': label_val
            })
            
    return t_values, scores, snapshots_data

def run_combined_experiment(total_steps=300, num_snapshots=15):
    model = LetterSkeleton(size=(200, 200))
    base_defaults = {'base_width_factor': 1.0, 'top_width': 0, 'crossbar_h_shift': 0}
    
    CanonicalLetters.draw_A(model, **base_defaults)
    ref_image = model.apply_morphology(thickness=6)
    
    scores = []
    t_values = []
    snapshots_data = []
    
    snapshot_indices = np.linspace(0, total_steps, num_snapshots, dtype=int)
    
    print(f"Testing COMBINED ({total_steps} steps)...")
    
    for i in range(total_steps + 1):
        t = i / total_steps
        
        p_width = 1.0 + (1.5 * t)
        p_top = int(0 + (120 * t))
        p_bar = int(0 + (50 * t))
        
        current_params = {
            'base_width_factor': p_width,
            'top_width': p_top,
            'crossbar_h_shift': p_bar
        }
        
        CanonicalLetters.draw_A(model, **current_params)
        test_img = model.apply_morphology(thickness=6)
        
        score = get_similarity(ref_image, test_img)
        scores.append(score)
        t_values.append(t)
        
        if i in snapshot_indices:
            snapshots_data.append({
                'image': test_img,
                'score': score,
                'label': f"t={t:.2f}"
            })
        
    return t_values, scores, snapshots_data

def save_high_res_graph(results):
    """יוצר גרף המבוסס על כל 300 הנקודות"""
    plt.figure(figsize=(12, 8))
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'] 
    
    for i, (label, (t, scores, _)) in enumerate(results.items()):
        linewidth = 4 if label == "COMBINED" else 2.5
        linestyle = '--' if label == "COMBINED" else '-'
        
        plt.plot(t, scores, label=label, linewidth=linewidth, linestyle=linestyle, color=colors[i])
    
    plt.title("Sensitivity Analysis: Letter 'A' (300 Steps Resolution)", fontsize=18)
    plt.xlabel("Deformation Intensity (0=Original -> 1=Max Deformed)", fontsize=14)
    plt.ylabel("Similarity Score (SSIM)", fontsize=14)
    plt.axhline(y=1.0, color='grey', linestyle=':', alpha=0.5)
    plt.axhline(y=0.75, color='red', linestyle=':', alpha=0.8, label='Similarity Threshold')
    
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    
    filename = "A_graph_300_steps.png"
    plt.savefig(filename, dpi=300)
    print(f"📈 Graph saved: {os.path.abspath(filename)}")

def save_wide_grid_15(results):
    """יוצר גריד רחב של 15 תמונות לכל שורה"""
    rows = len(results)
    cols = 15 # מספר התמונות שביקשת
    
    # יצירת תמונה רחבה מאוד כדי שהתמונות הקטנות לא ימעכו
    fig, axes = plt.subplots(rows, cols, figsize=(25, 8))
    fig.suptitle(f"Visual Progression: 15 Snapshots per Deformation", fontsize=20, y=0.98)
    
    experiment_names = list(results.keys())
    
    for row_idx, name in enumerate(experiment_names):
        _, _, snapshots_list = results[name]
        
        # כותרת צד לכל שורה
        # שמנו אותה בצד שמאל, מסובבת
        axes[row_idx, 0].set_ylabel(name, fontsize=12, fontweight='bold', rotation=90, labelpad=50)
        
        for col_idx in range(cols):
            ax = axes[row_idx, col_idx]
            
            if col_idx < len(snapshots_list):
                data = snapshots_list[col_idx]
                img = data['image']
                score = data['score']
                label_val = data['label']
                
                ax.imshow(img, cmap='gray')
                
                # כיתוב קומפקטי: ערך למעלה, ציון למטה
                # הקטנו את הפונט כדי שייכנס ב-15 עמודות
                ax.set_title(f"{label_val}\n{score:.2f}", fontsize=8)
            
            # ביטול מסגרות
            ax.set_xticks([])
            ax.set_yticks([])
            # אם זו לא העמודה הראשונה, נבטל גם את ה-ylabel של הציר כדי שיהיה נקי
            if col_idx > 0:
                ax.set_yticklabels([])
                ax.set_ylabel("")

    plt.tight_layout()
    
    filename = "A_grid_15_snapshots.png"
    plt.savefig(filename, dpi=150)
    print(f"🖼️  Wide Grid saved: {os.path.abspath(filename)}")

if __name__ == "__main__":
    results = {}
    STEPS = 300      # כמות הדגימות לגרף (חלק)
    SNAPSHOTS = 15   # כמות התמונות לתצוגה ויזואלית
    
    # הרצת הניסויים
    results['Leg Spread'] = run_experiment('base_width_factor', 1.0, 2.5, STEPS, SNAPSHOTS)
    results['Flat Top'] = run_experiment('top_width', 0, 120, STEPS, SNAPSHOTS)
    results['Bar Shift'] = run_experiment('crossbar_h_shift', 0, 50, STEPS, SNAPSHOTS)
    results['COMBINED'] = run_combined_experiment(STEPS, SNAPSHOTS)
    
    # שמירת התוצרים
    save_high_res_graph(results)
    save_wide_grid_15(results)
    
    plt.show()