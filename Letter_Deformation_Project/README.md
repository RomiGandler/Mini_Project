# Parametric Letter Perception Analysis

## Overview
This project explores the boundaries of visual perception by generating parametric deformations of letters (A, B, C). It quantifies the "perceptual distance" between a canonical letter and its deformed variants using Structural Similarity Index (SSIM).

The goal is to understand how geometric changes (shearing, squashing, stretching, etc.) affect the recognizability and structural integrity of characters.

## Key Features

### 1. Parametric Letter Generation
Dynamic generation of letter skeletons using vector-based logic, converted to raster images.
- **Letter A:** Supports shear (tilt), top-width modification, crossbar shifting, and base widening.
- **Letter B:** Supports vertical squashing, waist shifting, rotation, and width modification using complex Bézier-like curves.
- **Letter C:** Supports opening/closing (arc length), rotation, and aspect ratio changes.

### 2. Distance Metrics
- Uses **SSIM (Structural Similarity Index)** to calculate a "Distance Score" (0.0 = Identical, 1.0 = Completely different).
- Compares deformed versions against a "Canonical" (perfect) reference.

### 3. Visualization Tools
- **Interactive Playground:** Real-time GUI to manipulate parameters and see the distance score instantly.
- **Sequence Analysis:** Generates step-by-step deformation sequences with corresponding distance graphs.
- **Heatmaps:** 2D analysis showing the interaction between two parameters simultaneously.

## Project Structure
- `src/`: Core logic (Letter models, drawing engines, configuration).
- `results/`: Output directory for generated graphs and heatmaps.
- `interactive_game.py`: The main GUI application.
- `generate_*.py`: Scripts for generating static analysis reports.

## Installation
Python 3.8+ and the following libraries:
bash
pip install numpy opencv-python matplotlib scikit-image seaborn