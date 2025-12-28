import os
import matplotlib.pyplot as plt
import numpy as np
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters
from skimage.metrics import structural_similarity as ssim

# ==========================================
# 1. פונקציות עזר ומדידה
# ==========================================

def get_similarity(img1, img2):
    return ssim(img1, img2, data_range=img1.max() - img1.min())

def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"📁 Created folder: {folder_path}")

# ==========================================
# 2. מנוע הניסויים (Generic Experiment Engine)
# ==========================================

def run_single_param_experiment(letter_func, base_defaults, param_name, start_val, end_val, steps, num_snapshots):
    """מריץ ניסוי על פרמטר בודד לכל אות שהיא"""
    model = LetterSkeleton(size=(200, 200))
    
    # יצירת מקור (Reference)
    letter_func(model, **base_defaults)
    ref_image = model.apply_morphology(thickness=6)
    
    scores = []
    t_values = []
    snapshots_data = []
    snapshot_indices = np.linspace(0, steps, num_snapshots, dtype=int)
    
    for i in range(steps + 1):
        t = i / steps
        current_val = start_val + (end_val - start_val) * t
        
        current_params = base_defaults.copy()
        
        # טיפול ב-int/float
        if 'factor' in param_name:
            current_params[param_name] = current_val
            label_val = f"{current_val:.2f}"
        else:
            val_val = int(current_val)
            current_params[param_name] = val_val
            label_val = f"{val_val}px"
        
        letter_func(model, **current_params)
        test_img = model.apply_morphology(thickness=6)
        
        score = get_similarity(ref_image, test_img)
        scores.append(score)
        t_values.append(t)
        
        if i in snapshot_indices:
            snapshots_data.append({
                'image': test_img,
                'score': score,
                'label': label_val
            })
            
    return t_values, scores, snapshots_data

# ==========================================
# 3. ניסויים משולבים (Specific Combined Logic)
# ==========================================

def run_combined_A(steps, num_snapshots):
    model = LetterSkeleton(size=(200, 200))
    base_defaults = {'base_width_factor': 1.0, 'top_width': 0, 'crossbar_h_shift': 0}
    
    CanonicalLetters.draw_A(model, **base_defaults)
    ref_image = model.apply_morphology(thickness=6)
    
    scores, t_vals, snaps = [], [], []
    indices = np.linspace(0, steps, num_snapshots, dtype=int)
    
    for i in range(steps + 1):
        t = i / steps
        params = {
            'base_width_factor': 1.0 + (1.5 * t),
            'top_width': int(0 + (120 * t)),
            'crossbar_h_shift': int(0 + (50 * t))
        }
        CanonicalLetters.draw_A(model, **params)
        img = model.apply_morphology(thickness=6)
        score = get_similarity(ref_image, img)
        
        scores.append(score); t_vals.append(t)
        if i in indices: snaps.append({'image': img, 'score': score, 'label': f"t={t:.2f}"})
        
    return t_vals, scores, snaps

def run_combined_B(steps, num_snapshots):
    model = LetterSkeleton(size=(200, 200))
    base_defaults = {'width_factor': 1.0, 'waist_y_shift': 0, 'rotation_deg': 0}
    
    CanonicalLetters.draw_B(model, **base_defaults)
    ref_image = model.apply_morphology(thickness=6)
    
    scores, t_vals, snaps = [], [], []
    indices = np.linspace(0, steps, num_snapshots, dtype=int)
    
    for i in range(steps + 1):
        t = i / steps
        params = {
            'width_factor': 1.0 + (-0.6 * t),   # מצר מ-1.0 ל-0.4
            'waist_y_shift': int(0 + (50 * t)), # מותן עולה
            'rotation_deg': int(0 + (-15 * t))  # הטיה
        }
        CanonicalLetters.draw_B(model, **params)
        img = model.apply_morphology(thickness=6)
        score = get_similarity(ref_image, img)
        
        scores.append(score); t_vals.append(t)
        if i in indices: snaps.append({'image': img, 'score': score, 'label': f"t={t:.2f}"})
        
    return t_vals, scores, snaps

def run_combined_C(steps, num_snapshots):
    model = LetterSkeleton(size=(200, 200))
    base_defaults = {'cut_top': 60, 'cut_bottom': 60, 'elongation_factor': 1.0, 'rotation_deg': 0}
    
    CanonicalLetters.draw_C(model, **base_defaults)
    ref_image = model.apply_morphology(thickness=6)
    
    scores, t_vals, snaps = [], [], []
    indices = np.linspace(0, steps, num_snapshots, dtype=int)
    
    for i in range(steps + 1):
        t = i / steps
        params = {
            'cut_top': int(60 + (-150 * t)),    # מ-60 (פתוח) ל--90 (סגור)
            'cut_bottom': int(60 + (-150 * t)), 
            'elongation_factor': 1.0 + (0.6 * t),
            'rotation_deg': int(0 + (30 * t))
        }
        CanonicalLetters.draw_C(model, **params)
        img = model.apply_morphology(thickness=6)
        score = get_similarity(ref_image, img)
        
        scores.append(score); t_vals.append(t)
        if i in indices: snaps.append({'image': img, 'score': score, 'label': f"t={t:.2f}"})
        
    return t_vals, scores, snaps

# ==========================================
# 4. פונקציות שמירה (Save Functions)
# ==========================================

def save_graph(results, letter_name, output_dir):
    plt.figure(figsize=(12, 8))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'] 
    
    for i, (label, (t, scores, _)) in enumerate(results.items()):
        linewidth = 4 if label == "COMBINED" else 2.5
        linestyle = '--' if label == "COMBINED" else '-'
        plt.plot(t, scores, label=label, linewidth=linewidth, linestyle=linestyle, color=colors[i])
    
    plt.title(f"Sensitivity Analysis: Letter '{letter_name}' (300 Steps)", fontsize=18)
    plt.xlabel("Deformation Intensity (t)", fontsize=14)
    plt.ylabel("Similarity Score (SSIM)", fontsize=14)
    plt.axhline(y=0.75, color='red', linestyle=':', alpha=0.8, label='Similarity Threshold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    
    filename = os.path.join(output_dir, f"{letter_name}_analysis_graph.png")
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"   Saved Graph: {filename}")

def save_grid(results, letter_name, output_dir, num_snapshots):
    rows = len(results)
    cols = num_snapshots
    
    fig, axes = plt.subplots(rows, cols, figsize=(40, 10))
    fig.suptitle(f"Letter '{letter_name}': Deformation Progression", fontsize=24, y=0.98)
    
    experiment_names = list(results.keys())
    
    for row_idx, name in enumerate(experiment_names):
        _, _, snapshots_list = results[name]
        
        axes[row_idx, 0].set_ylabel(name, fontsize=16, fontweight='bold', rotation=90, labelpad=60)
        
        for col_idx in range(cols):
            ax = axes[row_idx, col_idx]
            if col_idx < len(snapshots_list):
                data = snapshots_list[col_idx]
                ax.imshow(data['image'], cmap='gray')
                ax.set_title(f"{data['label']}\n{data['score']:.2f}", fontsize=9)
            
            ax.set_xticks([]); ax.set_yticks([])
            if col_idx > 0: ax.set_yticklabels([]); ax.set_ylabel("")

    plt.tight_layout()
    filename = os.path.join(output_dir, f"{letter_name}_visual_grid.png")
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"   Saved Grid:  {filename}")

# ==========================================
# 5. ניהול ראשי (Main Orchestrator)
# ==========================================

def analyze_A(output_root, steps, snapshots):
    letter = "A"
    out_dir = os.path.join(output_root, letter)
    ensure_folder_exists(out_dir)
    
    results = {}
    defaults = {'base_width_factor': 1.0, 'top_width': 0, 'crossbar_h_shift': 0}
    
    print(f"--- Analyzing Letter A ---")
    results['Leg Spread'] = run_single_param_experiment(CanonicalLetters.draw_A, defaults, 'base_width_factor', 1.0, 2.5, steps, snapshots)
    results['Flat Top'] = run_single_param_experiment(CanonicalLetters.draw_A, defaults, 'top_width', 0, 120, steps, snapshots)
    results['Bar Shift'] = run_single_param_experiment(CanonicalLetters.draw_A, defaults, 'crossbar_h_shift', 0, 50, steps, snapshots)
    results['COMBINED'] = run_combined_A(steps, snapshots)
    
    save_graph(results, letter, out_dir)
    save_grid(results, letter, out_dir, snapshots)

def analyze_B(output_root, steps, snapshots):
    letter = "B"
    out_dir = os.path.join(output_root, letter)
    ensure_folder_exists(out_dir)
    
    results = {}
    defaults = {'width_factor': 1.0, 'waist_y_shift': 0, 'rotation_deg': 0}
    
    print(f"--- Analyzing Letter B ---")
    results['Squeeze Width'] = run_single_param_experiment(CanonicalLetters.draw_B, defaults, 'width_factor', 1.0, 0.4, steps, snapshots)
    results['Waist Up'] = run_single_param_experiment(CanonicalLetters.draw_B, defaults, 'waist_y_shift', 0, 50, steps, snapshots)
    results['Tilt Left'] = run_single_param_experiment(CanonicalLetters.draw_B, defaults, 'rotation_deg', 0, -15, steps, snapshots)
    results['COMBINED'] = run_combined_B(steps, snapshots)
    
    save_graph(results, letter, out_dir)
    save_grid(results, letter, out_dir, snapshots)

def analyze_C(output_root, steps, snapshots):
    letter = "C"
    out_dir = os.path.join(output_root, letter)
    ensure_folder_exists(out_dir)
    
    results = {}
    defaults = {'cut_top': 60, 'cut_bottom': 60, 'elongation_factor': 1.0, 'rotation_deg': 0}
    
    print(f"--- Analyzing Letter C ---")
    results['Closing Up'] = run_single_param_experiment(CanonicalLetters.draw_C, defaults, 'cut_top', 60, -90, steps, snapshots)
    results['Squashing'] = run_single_param_experiment(CanonicalLetters.draw_C, defaults, 'elongation_factor', 1.0, 1.6, steps, snapshots)
    results['Rotating'] = run_single_param_experiment(CanonicalLetters.draw_C, defaults, 'rotation_deg', 0, 30, steps, snapshots)
    results['COMBINED'] = run_combined_C(steps, snapshots)
    
    save_graph(results, letter, out_dir)
    save_grid(results, letter, out_dir, snapshots)

if __name__ == "__main__":
    OUTPUT_ROOT = "outputs"
    STEPS = 300
    SNAPSHOTS = 20
    
    print("🚀 Starting Full Analysis...")
    analyze_A(OUTPUT_ROOT, STEPS, SNAPSHOTS)
    analyze_B(OUTPUT_ROOT, STEPS, SNAPSHOTS)
    analyze_C(OUTPUT_ROOT, STEPS, SNAPSHOTS)
    print("\n✅ All done! Check the 'outputs' folder.")