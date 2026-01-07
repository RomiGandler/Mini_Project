# Project Tracking & Documentation

## 📂 File Dictionary
*A guide to the codebase structure.*

### Core Modules (`src/`)
| File | Purpose |
|------|---------|
| **`letter_model.py`** | The "Engine". Responsible for creating the blank canvas, drawing lines and curves, and handling the low-level OpenCV drawing commands. It is polymorphic (can handle points or ellipse parameters). |
| **`base_letters.py`** | The "Blueprint". Contains the logic for drawing specific letters (A, B, C). It calculates geometry, applies trigonometry for rotation/shear, and sends drawing commands to the model. |
| **`param_config.py`** | The "Rulebook". A Single Source of Truth that defines the minimum, maximum, and default values for every parameter to prevent crashes and extreme distortions. |

### Executable Scripts
| File | Purpose |
|------|---------|
| **`interactive_game.py`** | A GUI tool (using Matplotlib sliders) allowing manual play with parameters to "feel" the changes in real-time. |
| **`generate_custom_sequence.py`** | Generates a specific visual sequence (e.g., "Tilt A from -30° to 30°"). Outputs an image with 6 snapshots and a distance graph. |
| **`run_full_analysis.py`** | An automation script that runs a predefined set of analyses on all letters and saves the results in bulk. |
| **`generate_heatmap.py`** | Advanced analysis tool. Creates a 2D color map to visualize how *two* parameters interact and affect the letter's score simultaneously. |

---

## 🚀 Development Milestones
*A log of the steps taken to build the project.*

### Phase 1: Infrastructure
- [x] **Basic Skeleton:** Created `LetterSkeleton` class to handle canvas creation and basic line drawing.
- [x] **Distance Metric:** Integrated `SSIM` from scikit-image to measure visual difference between images.

### Phase 2: Letter Definitions
- [x] **Letter A:** Implemented logic for Shearing, Crossbar shift, and variable width.
- [x] **Letter B:** Implemented logic using dual loops. **Challenge:** Initially crashed due to complex curve parameters. **Fix:** Updated `letter_model` to handle ellipse arguments (`center`, `axes`).
- [x] **Letter C:** Implemented logic using arc drawing. Added "Cut Top" parameter to control the opening size.

### Phase 3: Robustness & Safety
- [x] **Geometric Constraints:** Added "Clamping" logic (in `base_letters`) to prevent letter parts from flying off the canvas during extreme deformations (e.g., keeping A's legs inside the frame).
- [x] **Central Configuration:** Created `param_config.py` to centralize all parameter limits. This ensures the Game, the Analysis tools, and the Heatmaps all respect the same physical limits.

### Phase 4: Advanced Visualization
- [x] **Interactive Tool:** Built a slider-based GUI.
- [x] **Heatmaps:** Implemented 2D matrix visualization (using Seaborn) to detect correlations between parameters.
- [x] **Heatmap Analysis Done:** Successfully generated interaction heatmap for Letter A (Shear vs Width).

---

## 📝 Next Steps / To-Do
- [ ] Analyze results to find "Perceptual Breakpoints" (points where the score drops drastically for other letters).
- [ ] Generate documentation for final submission.

---

## 🧠 Key Research Findings
*Insights derived from the generated data and graphs.*

### Analysis of Letter A: Shear vs. Width Interaction
Based on the heatmap `heatmap_A_shear_x_base_width_factor.png`:

1.  **The "Sweet Spot" (Optimal Zone):** The lowest distance scores (~0.10 - 0.12, indicated in deep blue) occur when both parameters are near their defaults (Shear near 0, Width factor between 0.9 and 1.1).
2.  **Width is Dominant Over Shear:**
    * Extreme broadening of the letter (Base Width Factor > 1.5, bottom rows) results in the highest distance scores (deep red, ~0.29 - 0.31) regardless of the shear value.
    * Extreme shearing (-40 or +40) also increases the distance, but less drastically (orange zones, scores ~0.23 - 0.25) as long as the width remains reasonable.
3.  **Conclusion:** The perceptual structure of letter 'A' is more sensitive to extreme changes in its aspect ratio (becoming too wide or too narrow) than it is to being tilted (sheared).