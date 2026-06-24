import os
import zipfile

def create_runnable_zip(base_dir, zip_path):
    skip_dirs = {
        'node_modules', 'venv', '.venv', 'env', '.git', '__pycache__', 
        'datasets', 'runs', 'runs (2)', 'video', 'zipfilesidd', 'eval', 'test_images'
    }
    skip_exts = {'.zip', '.tar.gz', '.mp4'}
    
    print(f"Creating runnable zip at {zip_path}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            if 'frontend\\public\\metrics' in root or 'frontend/public/metrics' in root:
                continue
                
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                
                if ext in skip_exts:
                    continue
                    
                file_path = os.path.join(root, file)
                
                # Skip the heavy user-uploaded images from previous testing
                if 'backend\\static\\uploads' in file_path or 'backend/static/uploads' in file_path:
                    continue
                
                if os.path.getsize(file_path) > 50 * 1024 * 1024:
                    continue
                    
                arcname = os.path.relpath(file_path, base_dir)
                zipf.write(file_path, arcname)
                
        # ensure empty uploads directory exists in zip
        zipf.writestr('backend/static/uploads/', '')
        
    print("Runnable zip created successfully.")

if __name__ == "__main__":
    base = "E:/flipkarttrafficapp"
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    zip_dest = os.path.join(desktop, "MargRakshak_Submission.zip")
    
    create_runnable_zip(base, zip_dest)
