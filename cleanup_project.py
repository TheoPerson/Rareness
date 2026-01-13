"""
Clean up project and fix image paths
"""
import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent

print("=" * 80)
print("CLEANING UP PROJECT")
print("=" * 80)
print()

# 1. Move images from LOL_SKIN_ASSETS/was_images to assets/splash
print("📸 Moving splash art images...")
source_images = BASE_DIR / "LOL_SKIN_ASSETS" / "was_images"
dest_images = BASE_DIR / "assets" / "splash"

if source_images.exists():
    dest_images.parent.mkdir(parents=True, exist_ok=True)
    
    # Count files
    image_files = list(source_images.glob("*.jpg"))
    print(f"   Found {len(image_files)} images in LOL_SKIN_ASSETS/was_images/")
    
    # Copy if destination is empty
    if not dest_images.exists() or not list(dest_images.glob("*.jpg")):
        print(f"   Copying to assets/splash/...")
        shutil.copytree(source_images, dest_images, dirs_exist_ok=True)
        print(f"   ✅ Copied {len(image_files)} images")
    else:
        print(f"   ✅ Images already in assets/splash/")
else:
    print("   ⚠️  Source folder not found")

# 2. Move metadata
print("\n📄 Moving metadata...")
source_meta = BASE_DIR / "LOL_SKIN_ASSETS" / "meta_json"
dest_meta = BASE_DIR / "assets" / "meta"

if source_meta.exists():
    dest_meta.parent.mkdir(parents=True, exist_ok=True)
    
    meta_files = list(source_meta.glob("*.json"))
    print(f"   Found {len(meta_files)} metadata files")
    
    if not dest_meta.exists() or not list(dest_meta.glob("*.json")):
        shutil.copytree(source_meta, dest_meta, dirs_exist_ok=True)
        print(f"   ✅ Copied {len(meta_files)} files")
    else:
        print(f"   ✅ Metadata already in assets/meta/")

# 3. Remove duplicate folders
print("\n🗑️  Removing duplicate folders...")
to_remove = [
    "LOL_EXPORT_SKINS",  # Duplicated in data/
    "LOL_SKIN_ASSETS",   # Duplicated in assets/
]

for folder in to_remove:
    folder_path = BASE_DIR / folder
    if folder_path.exists():
        try:
            shutil.rmtree(folder_path)
            print(f"   ✅ Removed: {folder}")
        except Exception as e:
            print(f"   ⚠️  Could not remove {folder}: {e}")

# 4. Remove unnecessary files
print("\n🗑️  Removing unnecessary files...")
to_remove_files = [
    "LOL_SKINS_COMPLETE_LIST.md",  # Moved to docs/
    "LOL_SKINS_COMPLETE_LIST.txt", # Moved to docs/
    "wad_files_list.txt",          # Moved to docs/
    "EXTRACT_GAME_FILES_GUIDE.md", # Moved to docs/
    "PROJECT_STRUCTURE.md",        # Not needed
    "export_lol_skins.py",         # Moved to scripts/
    "download_skin_assets.py",     # Moved to scripts/
    "find_wad_files.py",           # Moved to scripts/
    "generate_curated_skin_list.py", # Moved to scripts/
]

for file in to_remove_files:
    file_path = BASE_DIR / file
    if file_path.exists():
        try:
            file_path.unlink()
            print(f"   ✅ Removed: {file}")
        except Exception as e:
            print(f"   ⚠️  Could not remove {file}: {e}")

print("\n" + "=" * 80)
print("✅ CLEANUP COMPLETE!")
print("=" * 80)
print()
print("📁 Final structure:")
print("   ├── web/           - Web application")
print("   ├── data/          - CSV/JSON data")
print("   ├── assets/        - Images & metadata")
print("   ├── scripts/       - Python tools")
print("   └── docs/          - Documentation")
print()
print("🖼️  Images are now in: assets/splash/")
print("📊 Data is in: data/skins_all.csv")
print()
