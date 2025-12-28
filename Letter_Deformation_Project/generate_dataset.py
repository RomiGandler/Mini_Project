import matplotlib.pyplot as plt
import os
from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters

def generate_full_dataset(model, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Generating Letter A...")
    # --- A Variations ---
    # Shift Crossbar
    for val in [-40, -20, 0, 20, 40]:
        CanonicalLetters.draw_A(model, crossbar_h_shift=val)
        save_image(model, output_dir, f"A_shift_{val}")

    # Round Top
    for width in [0, 30, 60, 80]:
        CanonicalLetters.draw_A(model, top_width=width)
        save_image(model, output_dir, f"A_round_{width}")

    # Wide/Narrow Legs
    for factor in [0.7, 1.0, 1.3, 1.5]:
        CanonicalLetters.draw_A(model, base_width_factor=factor)
        save_image(model, output_dir, f"A_width_{factor:.1f}")


    print("Generating Letter B...")
    # --- B Variations ---
    # Waist Shift (הזזת המותניים למעלה/למטה)
    for shift in [-30, -15, 0, 15, 30]:
        CanonicalLetters.draw_B(model, waist_y_shift=shift)
        save_image(model, output_dir, f"B_waist_{shift}")
        
    # Width (רזה/שמן)
    for width in [0.7, 1.0, 1.3, 1.6]:
        CanonicalLetters.draw_B(model, width_factor=width)
        save_image(model, output_dir, f"B_width_{width:.1f}")


    print("Generating Letter C...")
    # --- C Variations ---
    # Opening Gap (פתוח/סגור)
    # שלילי = סגור יותר (כמעט O), חיובי = פתוח יותר
    for gap in [-30, -15, 0, 15, 35]: 
        CanonicalLetters.draw_C(model, gap_angle_deg=gap)
        save_image(model, output_dir, f"C_gap_{gap}")

    # Elongation (רחב/צר)
    for elong in [0.7, 0.9, 1.0, 1.2]:
        CanonicalLetters.draw_C(model, elongation_factor=elong)
        save_image(model, output_dir, f"C_elong_{elong:.1f}")

    print(f"Done! Images saved in '{output_dir}'")

def save_image(model, output_dir, filename):
    img = model.apply_morphology(thickness=6)
    full_path = os.path.join(output_dir, f"{filename}.png")
    plt.imsave(full_path, img, cmap='gray')

if __name__ == "__main__":
    model = LetterSkeleton(size=(200, 200))
    generate_full_dataset(model, output_dir='dataset_full')