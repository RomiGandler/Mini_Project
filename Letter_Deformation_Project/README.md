 `README.md` with this:

---

# 👁️ Parametric Letter Perception Analysis

## 📖 Overview

This project explores the boundaries of visual perception by generating parametric deformations of letters (**A, B, C, F, X, W**). It quantifies the "perceptual distance" between a canonical letter and its deformed variants using the **Structural Similarity Index (SSIM)**.

The goal is to understand how geometric changes (shearing, squashing, stretching, etc.) affect the recognizability and structural integrity of characters.

---

## 🚀 Key Features

### 1. Parametric Letter Generation

Dynamic generation of letter skeletons using vector-based logic (OpenCV).

#### 🔹 Original Letters (A, B, C)

* **Letter A:** Supports shear (tilt), top-width modification, crossbar shifting, and base widening.
* **Letter B:** Supports vertical squashing, waist shifting, rotation, and width modification using complex Bézier-like curves.
* **Letter C:** Supports opening/closing (arc length), rotation, and aspect ratio changes.

#### 🔹 Complex Letters (F, X, W)

* **Letter F:** Vertical spine with two horizontal bars.
* `bar_length`: Length multiplier for horizontal bars (0.5 to 1.5).
* `middle_bar_shift`: Vertical shift of middle bar (-30 to 30).
* `shear_x`: Horizontal tilt/italics (-30 to 30).
* `spine_height`: Height multiplier for the vertical spine (0.6 to 1.2).


* **Letter X:** Two diagonal lines crossing.
* `cross_ratio`: Where lines cross vertically (0.3 to 0.7).
* `spread_angle`: Angle spread of the diagonals (-20 to 20).
* `rotation_deg`: Overall rotation (-30 to 30).
* `asymmetry`: Makes one diagonal thicker/different.


* **Letter W:** Four connected line segments forming a W shape.
* `peak_depth`: How deep the inner valleys go (0.3 to 0.9).
* `width_factor`: Overall width multiplier (0.6 to 1.4).
* `middle_height`: Height of the middle peak (0.3 to 0.8).
* `shear_x`: Horizontal tilt (-25 to 25).



### 2. Distance Metrics

* Uses **SSIM (Structural Similarity Index)** to calculate a "Distance Score" (0.0 = Identical, 1.0 = Completely different).
* Compares deformed versions against a "Canonical" (perfect) reference.

### 3. Analysis Tools

* **Interactive Playground:** Real-time GUI to manipulate parameters and see the distance score instantly.
* **1D Parameter Analysis:** Graphs showing how a single parameter affects the score over a range.
* **2D Heatmaps:** Visualization of how *two* parameters interact (e.g., Does shearing 'A' matter less if it's very wide?).
* **Inter-Letter Similarity:** Compares the base structure of all letters against each other.

---

## 📂 Project Structure

```text
├── main.py                     # 🚀 ENTRY POINT: Main Menu CLI
├── param_config.json           # ⚙️ CONFIG: Central parameter limits
├── requirements.txt            # Dependencies
├── src/                        # 🧠 Core Logic
│   ├── letter_model.py         # Drawing engine
│   └── base_letters.py         # Letter definitions
├── Run_Project/                # 🛠️ Execution Scripts
│   ├── analyze_parameter.py    # 1D Graph generation
│   ├── analyze_heatmap.py      # 2D Heatmap generation
│   ├── inter_letter_analysis.py# Similarity Matrix
│   ├── generate_dataset.py     # ML Dataset generator
│   └── interactive_game.py     # GUI Tool
└── analysis/                   # 📊 OUTPUTS (Generated automatically)
    ├── heatmaps/
    ├── parameter_plots/
    └── inter_letter/

```

---

## 🛠️ Installation

1. **Clone or download the project.**
2. **Install dependencies** using the provided file:

```bash
pip install -r requirements.txt

```

*(Requires Python 3.8+)*

---

## 💻 Usage

The project is controlled via a single unified menu.

### 1. Run the Main Menu

```bash
python main.py

```

### 2. Select an Option

From the menu, you can choose:

* **1:** **Interactive Game** – Opens a window with sliders to play with letters manually.
* **2:** **Generate Dataset** – Creates thousands of images for Machine Learning.
* **3:** **Parameter Analysis** – Generates 1D graphs (Distance vs. Parameter).
* **4:** **Heatmap Analysis** – Generates 2D interaction maps.
* **5:** **Inter-Letter Matrix** – Checks similarity between base letters.
* **A:** **RUN ALL (Batch Mode)** – Automatically runs all analyses and saves reports to the `analysis/` folder.

---

## 📊 Parameter Summary Table

| Letter | Adjustable Parameters |
| --- | --- |
| **A** | `base_width_factor`, `top_width`, `crossbar_h_shift`, `shear_x`, `thickness` |
| **B** | `width_factor`, `waist_y_shift`, `rotation_deg`, `vertical_squash`, `thickness` |
| **C** | `cut_top`, `vertical_squash`, `rotation_deg`, `thickness` |
| **F** | `bar_length`, `middle_bar_shift`, `shear_x`, `spine_height`, `thickness` |
| **X** | `cross_ratio`, `spread_angle`, `rotation_deg`, `asymmetry`, `thickness` |
| **W** | `peak_depth`, `width_factor`, `middle_height`, `shear_x`, `thickness` |

---

## 👥 Authors

**Romi Gandler & Noya Michalovici**
*January 2026*