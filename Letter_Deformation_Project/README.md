# Parametric Letter Perception Analysis

## Overview
This project explores the boundaries of visual perception by generating parametric deformations of letters (A, B, C, F, X, W). It quantifies the "perceptual distance" between a canonical letter and its deformed variants using Structural Similarity Index (SSIM).

The goal is to understand how geometric changes (shearing, squashing, stretching, etc.) affect the recognizability and structural integrity of characters.

## Key Features

### 1. Parametric Letter Generation
Dynamic generation of letter skeletons using vector-based logic, converted to raster images.

#### Original Letters (A, B, C):
- **Letter A:** Supports shear (tilt), top-width modification, crossbar shifting, and base widening.
- **Letter B:** Supports vertical squashing, waist shifting, rotation, and width modification using complex Bézier-like curves.
- **Letter C:** Supports opening/closing (arc length), rotation, and aspect ratio changes.

#### New Letters (F, X, W):
- **Letter F:** Vertical spine with two horizontal bars
  - `bar_length`: Length multiplier for horizontal bars (0.5 to 1.5)
  - `middle_bar_shift`: Vertical shift of middle bar (-30 to 30)
  - `shear_x`: Horizontal tilt/italics (-30 to 30)
  - `spine_height`: Height multiplier for the vertical spine (0.6 to 1.2)

- **Letter X:** Two diagonal lines crossing
  - `cross_ratio`: Where lines cross vertically (0.3 to 0.7, 0.5 = center)
  - `spread_angle`: Angle spread of the diagonals (-20 to 20)
  - `rotation_deg`: Overall rotation (-30 to 30)
  - `asymmetry`: Makes one diagonal thicker/different (-20 to 20)

- **Letter W:** Four connected line segments forming a W shape
  - `peak_depth`: How deep the inner valleys go (0.3 to 0.9)
  - `width_factor`: Overall width multiplier (0.6 to 1.4)
  - `middle_height`: Height of the middle peak (0.3 to 0.8)
  - `shear_x`: Horizontal tilt (-25 to 25)

### 2. Distance Metrics
- Uses **SSIM (Structural Similarity Index)** to calculate a "Distance Score" (0.0 = Identical, 1.0 = Completely different).
- Compares deformed versions against a "Canonical" (perfect) reference.

### 3. Visualization Tools
- **Interactive Playground:** Real-time GUI to manipulate parameters and see the distance score instantly.
- **Sequence Analysis:** Generates step-by-step deformation sequences with corresponding distance graphs.
- **Heatmaps:** 2D analysis showing the interaction between two parameters simultaneously.
- **Evolution Matrices:** Full parameter combination matrices with distance scores.

## Project Structure
```
├── src/                          # Core logic
│   ├── letter_model.py          # Drawing engine (OpenCV)
│   ├── base_letters.py          # Letter definitions (A, B, C, F, X, W)
│   └── param_config.py          # Parameter configuration
├── output/                       # Generated images
├── results/                      # Analysis results
│   ├── heatmaps/
│   ├── distance_analysis/
│   └── report_examples/
├── interactive_game.py          # Main GUI application
├── run_full_analysis.py         # Automated distance analysis
├── generate_heatmap.py          # Interactive heatmap generator
├── generate_extra_heatmaps.py   # Automated heatmap generation
├── generate_full_matrix.py      # Full parameter matrix generation
├── generate_visual_tables.py    # Visual deformation tables
├── generate_report_examples.py  # Report figure generation
├── analyze_inter_letter.py      # Inter-letter comparison
└── main.py                      # Basic letter preview
```

## Installation
Python 3.8+ and the following libraries:
```bash
pip install numpy opencv-python matplotlib scikit-image seaborn
```

## Usage Examples

### Generate Base Letters
```bash
python main.py
```

### Interactive GUI
```bash
python interactive_game.py
```

### Run Full Analysis
```bash
python run_full_analysis.py
```

### Generate Heatmaps
```bash
python generate_extra_heatmaps.py
```

## Parameter Summary

| Letter | Parameters |
|--------|-----------|
| A | base_width_factor, top_width, crossbar_h_shift, shear_x, thickness |
| B | width_factor, waist_y_shift, rotation_deg, vertical_squash, thickness |
| C | cut_top, vertical_squash, rotation_deg, thickness |
| F | bar_length, middle_bar_shift, shear_x, spine_height, thickness |
| X | cross_ratio, spread_angle, rotation_deg, asymmetry, thickness |
| W | peak_depth, width_factor, middle_height, shear_x, thickness |

## Authors
Romi Gandler & Noya Michalovici

January 2026
