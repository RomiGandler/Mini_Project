import os
# List files in a directory
def list_files(startpath):
    print(f"\n📂 Project Structure: {os.path.abspath(startpath)}")
    print("="*60)

    # Directories to ignore
    ignored_dirs = {'__pycache__', '.git', '.idea', '.vscode'}
    
    for root, dirs, files in os.walk(startpath):
        # Filter out unnecessary directories
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        
        # Print folder name
        folder_name = os.path.basename(root)
        if folder_name == '': folder_name = '.'
        print(f"{indent}📁 {folder_name}/")

        # Print files in the folder
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if not f.endswith('.pyc') and f != '.DS_Store': # Filter out junk files
                print(f"{subindent}📄 {f}")

if __name__ == "__main__":
    list_files('.')
    print("="*60)