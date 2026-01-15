"""
Batch convert JPG splash arts to WEBP format
Reduces asset size by ~60% while maintaining quality

Usage:
    python convert_to_webp.py
    
Requirements:
    pip install Pillow tqdm
    
Output:
    - Creates web/public/assets_webp/ folder with converted images
    - Maintains directory structure
    - Provides size comparison statistics
"""
import os
from pathlib import Path
from PIL import Image
from tqdm import tqdm
import concurrent.futures
import json

# Configuration
INPUT_DIR = Path("../web/public/assets")
OUTPUT_DIR = Path("../web/public/assets_webp")
QUALITY = 85  # WEBP quality (85 = visually lossless, good balance)
MAX_WORKERS = 4  # Parallel conversion workers

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def convert_image(jpg_path):
    """
    Convert single JPG to WEBP with error handling
    
    Args:
        jpg_path: Path object to JPG file
        
    Returns:
        tuple: (status, original_size, new_size)
    """
    try:
        # Calculate relative path to maintain directory structure
        rel_path = jpg_path.relative_to(INPUT_DIR)
        webp_path = OUTPUT_DIR / rel_path.with_suffix('.webp')
        
        # Skip if already converted
        if webp_path.exists():
            original_size = jpg_path.stat().st_size
            new_size = webp_path.stat().st_size
            return ('skipped', original_size, new_size)
        
        # Create subdirectories if needed
        webp_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert JPG to WEBP
        original_size = jpg_path.stat().st_size
        with Image.open(jpg_path) as img:
            # Convert RGBA to RGB if needed (WEBP doesn't support transparency in all modes)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Save as WEBP with optimization
            img.save(webp_path, 'WEBP', quality=QUALITY, method=6)
        
        new_size = webp_path.stat().st_size
        return ('success', original_size, new_size)
        
    except Exception as e:
        return (f'failed: {str(e)}', 0, 0)

def main():
    print("🖼️  WEBP Batch Converter for LOL Skin Collection")
    print("=" * 70)
    
    # Find all JPG files recursively
    jpg_files = list(INPUT_DIR.rglob('*.jpg'))
    
    if not jpg_files:
        print(f"❌ No JPG files found in {INPUT_DIR}")
        print("   Make sure the assets folder exists and contains images.")
        return
    
    print(f"📁 Input:  {INPUT_DIR}")
    print(f"📁 Output: {OUTPUT_DIR}")
    print(f"🔧 Quality: {QUALITY} (visually lossless)")
    print(f"⚙️  Workers: {MAX_WORKERS} parallel threads")
    print(f"\n📊 Found {len(jpg_files)} JPG files\n")
    
    # Convert with parallel processing
    results = []
    total_original = 0
    total_new = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        with tqdm(total=len(jpg_files), desc="Converting", unit="img") as pbar:
            futures = {executor.submit(convert_image, jpg): jpg for jpg in jpg_files}
            
            for future in concurrent.futures.as_completed(futures):
                status, orig_size, new_size = future.result()
                results.append(status)
                total_original += orig_size
                total_new += new_size
                pbar.update(1)
    
    # Calculate statistics
    success_count = results.count('success')
    skipped_count = results.count('skipped')
    failed_count = len([r for r in results if r.startswith('failed')])
    
    # Size calculations
    original_mb = total_original / 1024 / 1024
    new_mb = total_new / 1024 / 1024
    saved_mb = original_mb - new_mb
    savings_pct = ((total_original - total_new) / total_original * 100) if total_original > 0 else 0
    
    # Print results
    print("\n" + "=" * 70)
    print("📊 CONVERSION SUMMARY")
    print("=" * 70)
    print(f"✅ Converted: {success_count}")
    print(f"⏭️  Skipped:   {skipped_count} (already existed)")
    print(f"❌ Failed:    {failed_count}")
    print("\n" + "=" * 70)
    print("💾 SIZE COMPARISON")
    print("=" * 70)
    print(f"Original (JPG):  {original_mb:,.1f} MB")
    print(f"Converted (WEBP): {new_mb:,.1f} MB")
    print(f"Space Saved:     {saved_mb:,.1f} MB ({savings_pct:.1f}%)")
    print("=" * 70)
    
    # Save summary report
    summary = {
        "conversion_date": Path(__file__).stat().st_mtime,
        "total_files": len(jpg_files),
        "converted": success_count,
        "skipped": skipped_count,
        "failed": failed_count,
        "original_size_mb": round(original_mb, 2),
        "new_size_mb": round(new_mb, 2),
        "savings_mb": round(saved_mb, 2),
        "savings_percent": round(savings_pct, 2),
        "quality_setting": QUALITY
    }
    
    summary_path = OUTPUT_DIR / "conversion_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📄 Summary saved to: {summary_path}")
    
    # Next steps
    print("\n" + "=" * 70)
    print("🚀 NEXT STEPS")
    print("=" * 70)
    print("1. Review converted images in assets_webp/ folder")
    print("2. Update SkinCard.js to use .webp extension")
    print("3. Test images display correctly in browser")
    print("4. After verification, delete old assets/ folder")
    print("5. Rename assets_webp/ to assets/")
    print("=" * 70 + "\n")
    
    if failed_count > 0:
        print("⚠️  Some conversions failed. Check error messages above.")
        failed_items = [r for r in results if r.startswith('failed')]
        print(f"   Failed conversions: {failed_items[:5]}")  # Show first 5

if __name__ == "__main__":
    main()
