import matplotlib.pyplot as plt
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim

from src.letter_model import LetterSkeleton
from src.base_letters import CanonicalLetters
from src.param_config import PARAM_CONFIG, get_limits

# =========================
# Configuration
# =========================

DRAW_FUNCS = {
    'A': CanonicalLetters.draw_A,
    'B': CanonicalLetters.draw_B,
    'C': CanonicalLetters.draw_C,
    'F': CanonicalLetters.draw_F,
    'X': CanonicalLetters.draw_X,
    'W': CanonicalLetters.draw_W,
}

OUTPUT_DIR = "results/custom_sequences"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# Utilities
# =========================

def calculate_distance(img1, img2):
    d_range = img1.max() - img1.min()
    if d_range == 0:
        d_range = 1
    sim = ssim(img1, img2, data_range=d_range)
    return max(0.0, 1.0 - sim)

def get_base_image(letter):
    model = LetterSkeleton(size=(200, 200))
    params = {k: v['default'] for k, v in PARAM_CONFIG[letter].items()}
    DRAW_FUNCS[letter](model, **params)
    return model.apply_morphology(thickness=params['thickness'])

# =========================
# Main Logic
# =========================

def run_sequence():
    print("\n--- Custom Deformation Generator ---")
    print(f"Available letters: {list(DRAW_FUNCS.keys())}")

    letter = input("Choose letter: ").upper().strip()
    if letter not in DRAW_FUNCS:
        print("❌ Invalid letter")
        return

    print(f"\nAvailable parameters for {letter}:")
    for k, v in PARAM_CONFIG[letter].items():
        print(f" - {k}: [{v['min']} → {v['max']}] (default={v['default']})")

    param = input("\nWhich parameter to vary? ").strip()
    if param not in PARAM_CONFIG[letter]:
        print("❌ Invalid parameter")
        return

    limits = get_limits(letter, param)

    try:
        start = float(input(f"Start value (≥ {limits['min']}): "))
        end = float(input(f"End value (≤ {limits['max']}): "))
        steps = int(input("Number of steps: "))
    except ValueError:
        print("❌ Invalid input")
        return

    # Clamp values
    start = max(limits['min'], min(limits['max'], start))
    end = max(limits['min'], min(limits['max'], end))

    print(f"\nGenerating {steps} variations for {letter}.{param}...")

    model = LetterSkeleton(size=(200, 200))
    base_img = get_base_image(letter)

    values = np.linspace(start, end, steps)
    images, scores = [], []

    for val in values:
        model.clear()
        params = {k: v['default'] for k, v in PARAM_CONFIG[letter].items()}

        # Preserve type
        if isinstance(params[param], int):
            params[param] = int(round(val))
        else:
            params[param] = float(val)

        DRAW_FUNCS[letter](model, **params)
        img = model.apply_morphology(thickness=params['thickness'])

        images.append(img)
        scores.append(calculate_distance(base_img, img))

    # =========================
    # Visualization
    # =========================

    fig = plt.figure(figsize=(16, 8))
    fig.suptitle(
        f"{letter} – Varying '{param}'",
        fontsize=18,
        fontweight='bold'
    )

    for i, (img, score) in enumerate(zip(images, scores)):
        ax = fig.add_subplot(2, steps, i + 1)
        ax.imshow(img, cmap='gray')
        ax.set_title(f"{values[i]:.2f}\nD={score:.2f}", fontsize=9)
        ax.axis('off')

    ax_plot = fig.add_subplot(2, 1, 2)
    ax_plot.plot(values, scores, marker='o')
    ax_plot.set_xlabel(param)
    ax_plot.set_ylabel("Distance from base")
    ax_plot.grid(alpha=0.3)

    filename = f"{letter}_{param}_sequence.png"
    path = os.path.join(OUTPUT_DIR, filename)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.show()

    print(f"\n✅ Saved to: {path}")

# =========================

if __name__ == "__main__":
    run_sequence()
