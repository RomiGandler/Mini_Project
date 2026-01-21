"""
Main runner for Letter Deformation Project
Runs all analyses and saves outputs under results/
"""

import os
import subprocess
import sys

# ----------------------------------
# Helper: run a python script safely
# ----------------------------------
def run_script(script_name):
    print(f"\n🚀 Running {script_name} ...")
    try:
        subprocess.run(
            [sys.executable, script_name],
            check=True
        )
        print(f"✅ Finished {script_name}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error while running {script_name}")
        print(e)
        sys.exit(1)

# ----------------------------------
# Main
# ----------------------------------
def main():

    print("\n==============================")
    print(" Letter Deformation Project ")
    print("==============================\n")

    # Ensure results directory exists
    os.makedirs("results", exist_ok=True)

    # ----------------------------------
    # 1. Base letters visualization
    # ----------------------------------
    run_script("main.py")  # canonical letters overview (A,B,C,F,X,W)

    # ----------------------------------
    # 2. Visual deformation tables
    # ----------------------------------
    run_script("generate_visual_tables.py")

    # ----------------------------------
    # 3. Heatmaps (parameter interactions)
    # ----------------------------------
    run_script("generate_heatmap.py")
    run_script("generate_extra_heatmaps.py")

    # ----------------------------------
    # 4. Full deformation matrices
    # ----------------------------------
    run_script("generate_full_matrix.py")

    # ----------------------------------
    # 5. Inter-letter & distance analysis
    # ----------------------------------
    run_script("analyze_inter_letter.py")

    # ----------------------------------
    # 6. Report example figures
    # ----------------------------------
    run_script("generate_report_examples.py")

    print("\n🎉 ALL ANALYSES COMPLETED SUCCESSFULLY!")
    print("📁 Check the 'results/' directory.\n")

# ----------------------------------
if __name__ == "__main__":
    main()
