"""
Organize Project Structure
Moves files to proper locations and creates symlinks for web app
"""
import os
import shutil
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Define structure
STRUCTURE = {
    'data': [
        ('LOL_EXPORT_SKINS/skins_all.csv', 'data/skins_all.csv'),
        ('LOL_EXPORT_SKINS/skins_all.json', 'data/skins_all.json'),
        ('LOL_EXPORT_SKINS/meta.json', 'data/meta.json'),
    ],
    'assets/splash': [
        ('LOL_SKIN_ASSETS/was_images', 'assets/splash'),
    ],
    'assets/meta': [
        ('LOL_SKIN_ASSETS/meta_json', 'assets/meta'),
    ],
    'scripts': [
        ('export_lol_skins.py', 'scripts/export_skins.py'),
        ('download_skin_assets.py', 'scripts/download_assets.py'),
        ('find_wad_files.py', 'scripts/find_wad_files.py'),
        ('generate_curated_skin_list.py', 'scripts/generate_lists.py'),
    ],
    'docs': [
        ('README.md', 'docs/README.md'),
        ('EXTRACT_GAME_FILES_GUIDE.md', 'docs/EXTRACT_GAME_FILES.md'),
        ('LOL_SKINS_COMPLETE_LIST.md', 'docs/SKINS_LIST.md'),
        ('LOL_SKINS_COMPLETE_LIST.txt', 'docs/SKINS_LIST.txt'),
        ('wad_files_list.txt', 'docs/WAD_FILES.txt'),
    ],
}

def copy_or_move(src, dst, move=False):
    """Copy or move file/directory"""
    src_path = BASE_DIR / src
    dst_path = BASE_DIR / dst
    
    if not src_path.exists():
        print(f"⚠️  Source not found: {src}")
        return False
    
    # Create parent directory
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        if src_path.is_dir():
            if dst_path.exists():
                print(f"✓ Already exists: {dst}")
                return True
            shutil.copytree(src_path, dst_path)
            print(f"✓ Copied directory: {src} → {dst}")
        else:
            shutil.copy2(src_path, dst_path)
            print(f"✓ Copied file: {src} → {dst}")
        return True
    except Exception as e:
        print(f"❌ Error copying {src}: {e}")
        return False

def main():
    print("=" * 80)
    print("ORGANIZING PROJECT STRUCTURE")
    print("=" * 80)
    print()
    
    # Copy files to new structure
    for category, files in STRUCTURE.items():
        print(f"\n📂 {category.upper()}")
        print("-" * 80)
        for src, dst in files:
            copy_or_move(src, dst)
    
    print("\n" + "=" * 80)
    print("✅ PROJECT ORGANIZED!")
    print("=" * 80)
    print()
    print("📁 New structure:")
    print("   data/          - CSV and JSON data files")
    print("   assets/        - Splash arts and metadata")
    print("   web/           - Web application (index.html)")
    print("   scripts/       - Python utility scripts")
    print("   docs/          - Documentation")
    print()
    print("🚀 To run the web app:")
    print("   1. Open: web/index.html in your browser")
    print("   2. Or run: python -m http.server 8000")
    print("   3. Then visit: http://localhost:8000/web/")
    print()

if __name__ == "__main__":
    main()
