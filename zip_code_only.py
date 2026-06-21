import os
import zipfile

def create_code_only_zip(base_dir, zip_path):
    allowed_exts = {'.py', '.ts', '.tsx', '.js', '.jsx', '.html', '.css', '.json', '.md', '.yaml', '.yml'}
    skip_dirs = {'node_modules', 'venv', '.venv', 'env', '.git', '__pycache__'}
    
    print(f"Creating code-only zip at {zip_path}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in allowed_exts:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, base_dir)
                    zipf.write(file_path, arcname)
    print("Zip created successfully.")

if __name__ == "__main__":
    base = "E:/flipkarttrafficapp"
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    zip_dest = os.path.join(desktop, "MargRakshak_SourceCode.zip")
    
    create_code_only_zip(base, zip_dest)
