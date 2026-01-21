import os
import sys
import subprocess

# Terminal styling constants
class Style:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def clear_screen():
    """Clears the terminal screen based on OS."""
    os.system('cls' if os.name == 'nt' else 'clear')

def run_script(script_name, args=None):
    """
    Executes a script from the Run_Project directory.
    Passes optional arguments to the script.
    """
    script_path = os.path.join("Run_Project", script_name)
    cmd = [sys.executable, script_path]
    if args:
        cmd.extend(args)
    
    print(f"\n{Style.BLUE}🚀 Running: {script_name}...{Style.END}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print(f"{Style.FAIL}❌ Error running {script_name}{Style.END}")
    except KeyboardInterrupt:
        print(f"\n{Style.YELLOW}⚠️  Execution interrupted by user.{Style.END}")

def run_full_pipeline():
    """
    Automated pipeline: Runs all analytical scripts in batch mode
    and saves results to the central /analysis folder.
    """
    clear_screen()
    print(f"{Style.HEADER}{Style.BOLD}=== STARTING FULL ANALYSIS PIPELINE ==={Style.END}\n")
    
    # 1. Generate 1D Distance Graphs
    run_script("analyze_parameter.py", ["--batch"])
    
    # 2. Generate 2D Interaction Heatmaps
    run_script("analyze_heatmap.py", ["--batch"])
    
    # 3. Generate Inter-Letter Similarity Matrix
    run_script("inter_letter_analysis.py")
    
    print(f"\n{Style.GREEN}{Style.BOLD}✅ Pipeline Complete! Check the 'analysis/' folder.{Style.END}")
    input("\nPress Enter to return to menu...")

def main():
    """Main menu loop for project management."""
    # Ensure current working directory is the project root
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    while True:
        clear_screen()
        print(f"{Style.HEADER}{Style.BOLD}==========================================")
        print("   LETTER DEFORMATION PROJECT - MAIN MENU")
        print(f"=========================================={Style.END}")
        
        print(f"{Style.BOLD}Production & Tools:{Style.END}")
        print(f"  {Style.GREEN}1.{Style.END} Interactive Game (Manual UI Testing)")
        print(f"  {Style.GREEN}2.{Style.END} Generate Dataset (Images for ML Training)")
        
        print(f"\n{Style.BOLD}Analysis Tools (Individual):{Style.END}")
        print(f"  {Style.GREEN}3.{Style.END} Parameter Analysis (1D Distortion Graphs)")
        print(f"  {Style.GREEN}4.{Style.END} Heatmap Analysis (2D Parameter Interaction)")
        print(f"  {Style.GREEN}5.{Style.END} Inter-Letter Similarity Matrix")
        
        print(f"\n{Style.BOLD}Automation:{Style.END}")
        print(f"  {Style.YELLOW}A.{Style.END} {Style.BOLD}RUN ALL ANALYSIS (Batch Mode){Style.END}")
        
        print(f"\n{Style.FAIL}Q.{Style.END} Quit")
        print(f"{Style.HEADER}------------------------------------------{Style.END}")
        
        choice = input(f"{Style.BOLD}Select an option: {Style.END}").strip().upper()

        if choice == '1': run_script("interactive_game.py")
        elif choice == '2': run_script("generate_dataset.py")
        elif choice == '3': run_script("analyze_parameter.py")
        elif choice == '4': run_script("analyze_heatmap.py")
        elif choice == '5': run_script("inter_letter_analysis.py")
        elif choice == 'A': run_full_pipeline()
        elif choice == 'Q':
            print(f"\n{Style.BLUE}Goodbye! 👋{Style.END}")
            break
        else:
            input(f"\n{Style.FAIL}Invalid option. Press Enter to continue...{Style.END}")

if __name__ == "__main__":
    main()