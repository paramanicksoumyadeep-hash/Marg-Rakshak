import os
import re
import zipfile

def remove_formatting_and_emojis(file_path):
    # Regex to match lines like '# ----------' or '// ----------' or '{/* --------- */}'
    dash_pattern = re.compile(r'^\s*(#|//|/\*|<!--|\{/\*)\s*[-=]{3,}\s*(\*/|-->|\*/\})?\s*$')
    
    # Regex to strip emojis. A simple unicode block match for most emojis
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        new_lines = []
        changed = False
        for line in lines:
            # Check if it's a dash comment line
            if dash_pattern.match(line):
                changed = True
                continue # skip this line
                
            # Remove emojis
            new_line = emoji_pattern.sub('', line)
            if new_line != line:
                changed = True
            
            new_lines.append(new_line)
            
        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"Cleaned: {file_path}")
            
    except Exception as e:
        print(f"Skipping {file_path}: {e}")

def process_directory(base_dir):
    skip_dirs = {'node_modules', 'venv', '.venv', 'env', '.git', '__pycache__', 'datasets', 'runs', 'video'}
    allowed_exts = {'.py', '.ts', '.tsx', '.js', '.jsx', '.css', '.md'}
    
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in allowed_exts:
                remove_formatting_and_emojis(os.path.join(root, file))

def create_zip(base_dir, zip_path):
    # Zip the code
    skip_dirs = {'node_modules', 'venv', '.venv', 'env', '.git', '__pycache__', 'datasets', 'runs', 'runs (2)', 'video', 'zipfilesidd'}
    skip_exts = {'.pt', '.zip', '.tar.gz', '.mp4'}
    
    print(f"Creating zip at {zip_path}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in skip_exts:
                    continue
                    
                file_path = os.path.join(root, file)
                
                # Check size, skip anything over 10MB just to be safe
                if os.path.getsize(file_path) > 10 * 1024 * 1024:
                    continue
                    
                arcname = os.path.relpath(file_path, base_dir)
                zipf.write(file_path, arcname)
    print("Zip created successfully.")

if __name__ == "__main__":
    base = "E:/flipkarttrafficapp"
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    zip_dest = os.path.join(desktop, "MargRakshak_SourceCode.zip")
    
    process_directory(base)
    create_zip(base, zip_dest)
