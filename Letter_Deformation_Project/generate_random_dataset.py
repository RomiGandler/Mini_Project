import matplotlib.pyplot as plt
import os
import random
import numpy as np
import math
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters

def generate_random_dataset(output_dir, num_samples_per_letter=300):
    # שינוי: ברירת המחדל היא כעת 300 תמונות לכל אות
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    model = LetterSkeleton(size=(200, 200))
    
    print(f"Generating {num_samples_per_letter} samples per letter in '{output_dir}'...")

    # --- Generate A (אקסטרים: צרה מאוד ורחבה מאוד) ---
    a_samples = []
    for i in range(num_samples_per_letter):
        params = {
            'top_width': random.randint(0, 90),
            'crossbar_h_shift': random.randint(-40, 40),
            
            # שינוי משמעותי:
            # 0.4 = צר מאוד (כמו יתד)
            # 1.95 = רחב מאוד (כמעט 200 פיקסלים, מקסימום רוחב)
            'base_width_factor': random.uniform(0.4, 1.95) 
        }
        CanonicalLetters.draw_A(model, **params)
        img = model.apply_morphology(thickness=6)
        
        filename = f"A_{i:03d}.png"
        plt.imsave(os.path.join(output_dir, filename), img, cmap='gray')
        a_samples.append(img)

    # --- Generate B (אקסטרים: מתוחה ופחוסה) ---
    b_samples = []
    for i in range(num_samples_per_letter):
        params = {
            'waist_y_shift': random.randint(-35, 35),
            
            # שינוי משמעותי:
            # 0.5 = B צרה מאוד ("מתוחה")
            # 2.1 = B שמנה ופחוסה מאוד
            'width_factor': random.uniform(0.5, 2.1),
            
            'rotation_deg': random.randint(-15, 15)
        }
        CanonicalLetters.draw_B(model, **params)
        img = model.apply_morphology(thickness=6)
        
        filename = f"B_{i:03d}.png"
        plt.imsave(os.path.join(output_dir, filename), img, cmap='gray')
        b_samples.append(img)

    # --- Generate C (נשאר עם התיקון הקודם והמוצלח) ---
    c_samples = []
    for i in range(num_samples_per_letter):
        params = {
            'rotation_deg': random.randint(-25, 25),
            'cut_top': random.randint(-40, 95),
            'cut_bottom': random.randint(-40, 60), # שומרים על ההגבלה כדי שלא תהיה "עצובה"
            'elongation_factor': random.uniform(0.8, 1.6) 
        }
        CanonicalLetters.draw_C(model, **params)
        img = model.apply_morphology(thickness=6)
        
        filename = f"C_{i:03d}.png"
        plt.imsave(os.path.join(output_dir, filename), img, cmap='gray')
        c_samples.append(img)

    print("Generation complete.")
    create_contact_sheet(a_samples, b_samples, c_samples, output_dir)

def create_contact_sheet(a_imgs, b_imgs, c_imgs, output_dir):
    """
    יוצר תצוגה מורחבת של דוגמאות.
    """
    # הגדלתי קצת את כמות התצוגה כדי שנראה יותר מהמגוון החדש
    samples_to_show = 80  
    cols = 16
    
    print(f"Creating preview grid with {samples_to_show} samples per letter...")

    all_samples = a_imgs[:samples_to_show] + b_imgs[:samples_to_show] + c_imgs[:samples_to_show]
    
    total_images = len(all_samples)
    if total_images == 0:
        return

    rows = math.ceil(total_images / cols)
    
    fig_height = rows * 1.5 
    fig, axes = plt.subplots(rows, cols, figsize=(22, fig_height)) # קצת יותר רחב
    plt.subplots_adjust(wspace=0.05, hspace=0.05, left=0.01, right=0.99, top=0.99, bottom=0.01)
    
    if isinstance(axes, np.ndarray):
        axes_flat = axes.flat
    else:
        axes_flat = [axes]

    for i, ax in enumerate(axes_flat):
        if i < total_images:
            ax.imshow(all_samples[i], cmap='gray')
            ax.axis('off')
        else:
            ax.axis('off')
        
    preview_path = os.path.join(output_dir, "_preview_grid_300.png")
    plt.savefig(preview_path, dpi=150)
    print(f"Preview saved to: {preview_path}")
    plt.close(fig)

if __name__ == "__main__":
    generate_random_dataset(output_dir='dataset_random_300')