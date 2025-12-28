import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters
from skimage.metrics import structural_similarity as ssim

# ==========================================
# 1. הגדרות תשתית
# ==========================================

def get_similarity(img1, img2):
    return ssim(img1, img2, data_range=img1.max() - img1.min())

def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def format_label(param_name, value):
    """יוצר תווית קצרה וקריאה לגריד"""
    if 'factor' in param_name:
        return f"{value:.2f}"
    elif 'deg' in param_name:
        return f"{int(value)}°"
    else: # pixels
        return f"{int(value)}px"

# ==========================================
# 2. המנוע הגנרי (The Generic Engine)
# ==========================================

def run_multi_param_experiment(letter_func, base_defaults, changes_dict, steps, num_snapshots):
    """
    פונקציה אחת שמסוגלת להריץ כל קומבינציה של פרמטרים.
    changes_dict: מילון שבו המפתח הוא שם הפרמטר והערך הוא (start, end)
    """
    model = LetterSkeleton(size=(200, 200))
    
    # 1. יצירת תמונת מקור (Reference)
    letter_func(model, **base_defaults)
    ref_image = model.apply_morphology(thickness=6)
    
    scores = []
    t_values = []
    snapshots_data = []
    
    # אינדקסים לשמירת תמונות
    snapshot_indices = np.linspace(0, steps, num_snapshots, dtype=int)
    
    for i in range(steps + 1):
        t = i / steps
        
        # בניית הפרמטרים לצעד הנוכחי
        current_params = base_defaults.copy()
        label_parts = []
        
        for param_name, (start_val, end_val) in changes_dict.items():
            # חישוב הערך הנוכחי (אינטרפולציה ליניארית)
            val = start_val + (end_val - start_val) * t
            
            # אם זה פרמטר שצריך להיות int (כמו פיקסלים)
            if 'factor' not in param_name:
                val = int(val)
                current_params[param_name] = val
            else:
                current_params[param_name] = val
            
            # הוספה לתווית רק אם אנחנו באחת מנקודות הציון
            if i in snapshot_indices:
                # קיצור שמות לתצוגה נקייה
                short_name = param_name.split('_')[0][:3] # מקצר שמות ארוכים
                formatted_val = format_label(param_name, val)
                label_parts.append(f"{short_name}:{formatted_val}")

        # ציור ומדידה
        letter_func(model, **current_params)
        test_img = model.apply_morphology(thickness=6)
        score = get_similarity(ref_image, test_img)
        
        scores.append(score)
        t_values.append(t)
        
        if i in snapshot_indices:
            # יצירת תווית משולבת (למשל: wid:1.5 | rot:30)
            full_label = "\n".join(label_parts) if len(label_parts) <= 2 else f"All (t={t:.2f})"
            if i == 0: full_label = "Start"
            
            snapshots_data.append({
                'image': test_img,
                'score': score,
                'label': full_label
            })
            
    return t_values, scores, snapshots_data

# ==========================================
# 3. פונקציות שמירה (Save Results)
# ==========================================

def save_graph(results, letter_name, output_dir):
    plt.figure(figsize=(14, 9))
    
    # שימוש בפלטת צבעים שתספיק ל-7 קווים
    colors = plt.cm.tab10(np.linspace(0, 1, len(results)))
    
    for i, (label, (t, scores, _)) in enumerate(results.items()):
        # הדגשה: קו עבה ל"הכל ביחד", בינוני לזוגות, דק ליחידים
        if label == "ALL COMBINED":
            lw = 4; ls = '--'
        elif "+" in label: # זוגות
            lw = 2.5; ls = '-.'
        else: # יחידים
            lw = 2; ls = '-'
            
        plt.plot(t, scores, label=label, linewidth=lw, linestyle=ls, color=colors[i])
    
    plt.title(f"Sensitivity Analysis: Letter '{letter_name}' (All Combinations)", fontsize=18)
    plt.xlabel("Deformation Intensity (t)", fontsize=14)
    plt.ylabel("Similarity Score (SSIM)", fontsize=14)
    plt.axhline(y=0.75, color='red', linestyle=':', alpha=0.8, label='Similarity Threshold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10, loc='lower left')
    
    filename = os.path.join(output_dir, f"{letter_name}_analysis_graph.png")
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"   Saved Graph: {filename}")

def save_grid(results, letter_name, output_dir, num_snapshots):
    rows = len(results)
    cols = num_snapshots
    
    # הגדלנו את הגובה כי עכשיו יש 7 שורות
    fig, axes = plt.subplots(rows, cols, figsize=(40, 16))
    fig.suptitle(f"Letter '{letter_name}': Pairwise & Combined Deformations", fontsize=24, y=0.98)
    
    experiment_names = list(results.keys())
    
    for row_idx, name in enumerate(experiment_names):
        _, _, snapshots_list = results[name]
        
        # עיצוב כותרת הצד
        display_name = name.replace(" + ", "\n+\n") # שבירת שורות בשמות ארוכים
        axes[row_idx, 0].set_ylabel(display_name, fontsize=14, fontweight='bold', rotation=0, ha='right', va='center', labelpad=20)
        
        for col_idx in range(cols):
            ax = axes[row_idx, col_idx]
            if col_idx < len(snapshots_list):
                data = snapshots_list[col_idx]
                ax.imshow(data['image'], cmap='gray')
                
                # פונט קטן יותר כדי שהכיתוב ייכנס
                ax.set_title(f"{data['label']}\n{data['score']:.2f}", fontsize=8)
            
            ax.set_xticks([]); ax.set_yticks([])
            # הסרת מסגרות פנימיות
            for spine in ax.spines.values(): spine.set_visible(False)

    plt.tight_layout()
    # התאמה ידנית לשוליים שמאליים (בגלל כותרות הצד הארוכות)
    plt.subplots_adjust(left=0.08, top=0.92)
    
    filename = os.path.join(output_dir, f"{letter_name}_visual_grid.png")
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"   Saved Grid:  {filename}")

# ==========================================
# 4. הגדרת הניסויים (The Experiment Logic)
# ==========================================

def analyze_letter_A(output_root, steps, snapshots):
    letter = "A"
    out_dir = os.path.join(output_root, letter)
    ensure_folder_exists(out_dir)
    print(f"--- Analyzing Letter A ---")
    
    defaults = {'base_width_factor': 1.0, 'top_width': 0, 'crossbar_h_shift': 0}
    
    # הגדרת הטווחים לכל פרמטר
    range_width = (1.0, 2.5)
    range_top = (0, 120)
    range_bar = (0, 50)
    
    results = {}
    
    # 1. Singles
    results['Leg Spread'] = run_multi_param_experiment(CanonicalLetters.draw_A, defaults, {'base_width_factor': range_width}, steps, snapshots)
    results['Flat Top'] = run_multi_param_experiment(CanonicalLetters.draw_A, defaults, {'top_width': range_top}, steps, snapshots)
    results['Bar Shift'] = run_multi_param_experiment(CanonicalLetters.draw_A, defaults, {'crossbar_h_shift': range_bar}, steps, snapshots)
    
    # 2. Pairs (Combinations of 2)
    results['Legs + Top'] = run_multi_param_experiment(CanonicalLetters.draw_A, defaults, 
                                                       {'base_width_factor': range_width, 'top_width': range_top}, steps, snapshots)
    results['Legs + Bar'] = run_multi_param_experiment(CanonicalLetters.draw_A, defaults, 
                                                       {'base_width_factor': range_width, 'crossbar_h_shift': range_bar}, steps, snapshots)
    results['Top + Bar']  = run_multi_param_experiment(CanonicalLetters.draw_A, defaults, 
                                                       {'top_width': range_top, 'crossbar_h_shift': range_bar}, steps, snapshots)
    
    # 3. All Combined
    results['ALL COMBINED'] = run_multi_param_experiment(CanonicalLetters.draw_A, defaults, 
                                                         {'base_width_factor': range_width, 'top_width': range_top, 'crossbar_h_shift': range_bar}, steps, snapshots)
    
    save_graph(results, letter, out_dir)
    save_grid(results, letter, out_dir, snapshots)

def analyze_letter_B(output_root, steps, snapshots):
    letter = "B"
    out_dir = os.path.join(output_root, letter)
    ensure_folder_exists(out_dir)
    print(f"--- Analyzing Letter B ---")
    
    defaults = {'width_factor': 1.0, 'waist_y_shift': 0, 'rotation_deg': 0}
    
    range_width = (1.0, 0.4)
    range_waist = (0, 50)
    range_rot = (0, -15)
    
    results = {}
    
    # Singles
    results['Squeeze'] = run_multi_param_experiment(CanonicalLetters.draw_B, defaults, {'width_factor': range_width}, steps, snapshots)
    results['Waist Up'] = run_multi_param_experiment(CanonicalLetters.draw_B, defaults, {'waist_y_shift': range_waist}, steps, snapshots)
    results['Tilt'] = run_multi_param_experiment(CanonicalLetters.draw_B, defaults, {'rotation_deg': range_rot}, steps, snapshots)
    
    # Pairs
    results['Squeeze + Waist'] = run_multi_param_experiment(CanonicalLetters.draw_B, defaults, 
                                                            {'width_factor': range_width, 'waist_y_shift': range_waist}, steps, snapshots)
    results['Squeeze + Tilt'] = run_multi_param_experiment(CanonicalLetters.draw_B, defaults, 
                                                           {'width_factor': range_width, 'rotation_deg': range_rot}, steps, snapshots)
    results['Waist + Tilt'] = run_multi_param_experiment(CanonicalLetters.draw_B, defaults, 
                                                         {'waist_y_shift': range_waist, 'rotation_deg': range_rot}, steps, snapshots)
    
    # All
    results['ALL COMBINED'] = run_multi_param_experiment(CanonicalLetters.draw_B, defaults, 
                                                         {'width_factor': range_width, 'waist_y_shift': range_waist, 'rotation_deg': range_rot}, steps, snapshots)
    
    save_graph(results, letter, out_dir)
    save_grid(results, letter, out_dir, snapshots)

def analyze_letter_C(output_root, steps, snapshots):
    letter = "C"
    out_dir = os.path.join(output_root, letter)
    ensure_folder_exists(out_dir)
    print(f"--- Analyzing Letter C ---")
    
    # התחלה מ-40 (C יפה)
    defaults = {'cut_top': 40, 'cut_bottom': 40, 'elongation_factor': 1.0, 'rotation_deg': 0}
    
    # הגדרת הטווחים
    # עבור סגירה, אנחנו צריכים להזיז את שני ה-cutים ביחד
    range_cut = (40, -90) 
    range_elong = (1.0, 1.6)
    range_rot = (0, 30)
    
    # Helper dicts for "Closing" (affects 2 params strictly speaking but counts as 1 logical deformation)
    closing_params = {'cut_top': range_cut, 'cut_bottom': range_cut}
    
    results = {}
    
    # Singles
    results['Closing'] = run_multi_param_experiment(CanonicalLetters.draw_C, defaults, closing_params, steps, snapshots)
    results['Squash'] = run_multi_param_experiment(CanonicalLetters.draw_C, defaults, {'elongation_factor': range_elong}, steps, snapshots)
    results['Rotate'] = run_multi_param_experiment(CanonicalLetters.draw_C, defaults, {'rotation_deg': range_rot}, steps, snapshots)
    
    # Pairs
    # שילוב סגירה + מעיכה
    pair1 = closing_params.copy(); pair1['elongation_factor'] = range_elong
    results['Closing + Squash'] = run_multi_param_experiment(CanonicalLetters.draw_C, defaults, pair1, steps, snapshots)
    
    # שילוב סגירה + סיבוב
    pair2 = closing_params.copy(); pair2['rotation_deg'] = range_rot
    results['Closing + Rotate'] = run_multi_param_experiment(CanonicalLetters.draw_C, defaults, pair2, steps, snapshots)
    
    # שילוב מעיכה + סיבוב
    results['Squash + Rotate'] = run_multi_param_experiment(CanonicalLetters.draw_C, defaults, 
                                                            {'elongation_factor': range_elong, 'rotation_deg': range_rot}, steps, snapshots)
    
    # All
    all_combined = closing_params.copy()
    all_combined['elongation_factor'] = range_elong
    all_combined['rotation_deg'] = range_rot
    results['ALL COMBINED'] = run_multi_param_experiment(CanonicalLetters.draw_C, defaults, all_combined, steps, snapshots)
    
    save_graph(results, letter, out_dir)
    save_grid(results, letter, out_dir, snapshots)

if __name__ == "__main__":
    OUTPUT_ROOT = "outputs"
    STEPS = 300
    SNAPSHOTS = 20
    
    print("🚀 Starting Comprehensive Analysis (Singles, Pairs, Combined)...")
    analyze_letter_A(OUTPUT_ROOT, STEPS, SNAPSHOTS)
    analyze_letter_B(OUTPUT_ROOT, STEPS, SNAPSHOTS)
    analyze_letter_C(OUTPUT_ROOT, STEPS, SNAPSHOTS)
    print("\n✅ Analysis Complete. Check the 'outputs' folder.")