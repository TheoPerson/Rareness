"""
League of Legends Skin Asset Downloader
Downloads WAS (Web Asset Sprite) images and META (JSON metadata) for all skins
Enhanced with retry logic and better error handling
"""
import csv
import os
import json
import requests
from pathlib import Path
from tqdm import tqdm
import time

# Configuration
CSV_PATH = "LOL_EXPORT_SKINS/skins_all.csv"
OUTPUT_DIR = "LOL_SKIN_ASSETS"
WAS_DIR = os.path.join(OUTPUT_DIR, "was_images")
META_DIR = os.path.join(OUTPUT_DIR, "meta_json")

# Create output directories
os.makedirs(WAS_DIR, exist_ok=True)
os.makedirs(META_DIR, exist_ok=True)

# Create session with retry logic
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=3)
session.mount('http://', adapter)
session.mount('https://', adapter)

def download_with_retry(url, filepath, max_retries=3, timeout=15):
    """Download file with retry logic"""
    for attempt in range(max_retries):
        try:
            resp = session.get(url, timeout=timeout, stream=True)
            if resp.status_code == 200:
                with open(filepath, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return True
            elif resp.status_code == 404:
                return False  # File doesn't exist, don't retry
            else:
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                return False
        except (requests.RequestException, KeyboardInterrupt) as e:
            if isinstance(e, KeyboardInterrupt):
                raise
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return False
    return False

# Get latest patch version
print("🔎 Fetching latest patch version...")
try:
    versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    latest_patch = session.get(versions_url, timeout=10).json()[0]
    print(f"📦 Using patch: {latest_patch}")
except Exception as e:
    print(f"⚠️  Could not fetch latest patch, using default: 16.1.1")
    latest_patch = "16.1.1"

# Read skins from CSV
print(f"📖 Reading skins from {CSV_PATH}...")
skins = []
with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    skins = list(reader)

print(f"✅ Found {len(skins)} skins to download\n")

# Track stats
downloaded_champions = set()
failed_downloads = []
success_count = 0
skip_count = 0

# Download WAS images (skin splash arts)
print("🖼️  Downloading WAS (Splash Art) images...")
print("   This may take 10-20 minutes depending on your connection...")
print("   Press Ctrl+C to stop (progress is saved)\n")

try:
    for skin in tqdm(skins, desc="WAS Images", unit="skin"):
        champion = skin["champion"]
        skin_num = skin["skin_num"]
        skin_name = skin["skin_name"]
        
        # Build WAS URL - using full splash art
        was_url = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion}_{skin_num}.jpg"
        
        # Create safe filename
        safe_name = skin_name.replace("/", "-").replace(":", "").replace(" ", "_").replace("'", "")
        filename = f"{champion}_{skin_num}_{safe_name}.jpg"
        filepath = os.path.join(WAS_DIR, filename)
        
        # Skip if already downloaded
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            skip_count += 1
            continue
        
        # Download with retry
        if download_with_retry(was_url, filepath):
            success_count += 1
        else:
            failed_downloads.append({
                "type": "WAS",
                "skin_id": skin["skin_id"],
                "champion": champion,
                "skin_name": skin_name,
                "url": was_url
            })
            # Remove failed file if it exists
            if os.path.exists(filepath):
                os.remove(filepath)

except KeyboardInterrupt:
    print("\n\n⚠️  Download interrupted by user. Progress has been saved.")
    print(f"   Downloaded: {success_count} | Skipped: {skip_count}")
    print("   Run the script again to resume.\n")

print(f"\n✅ WAS images: {success_count} downloaded, {skip_count} already existed")
print(f"   Location: {WAS_DIR}\n")

# Download META JSON files (one per champion)
print("📄 Downloading META (JSON metadata) files...")
meta_success = 0
meta_skip = 0

try:
    unique_champions = sorted(set(skin["champion"] for skin in skins))
    
    for champion in tqdm(unique_champions, desc="META JSON", unit="champion"):
        filepath = os.path.join(META_DIR, f"{champion}.json")
        
        # Skip if already downloaded
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            meta_skip += 1
            continue
        
        # Build META URL
        meta_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_patch}/data/en_US/champion/{champion}.json"
        
        # Download with retry
        try:
            resp = session.get(meta_url, timeout=15)
            if resp.status_code == 200:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(resp.json(), f, indent=2, ensure_ascii=False)
                meta_success += 1
            else:
                failed_downloads.append({
                    "type": "META",
                    "champion": champion,
                    "url": meta_url,
                    "status": resp.status_code
                })
        except Exception as e:
            failed_downloads.append({
                "type": "META",
                "champion": champion,
                "url": meta_url,
                "error": str(e)
            })

except KeyboardInterrupt:
    print("\n\n⚠️  Download interrupted by user. Progress has been saved.")

print(f"\n✅ META JSON: {meta_success} downloaded, {meta_skip} already existed")
print(f"   Location: {META_DIR}\n")

# Save failed downloads log
if failed_downloads:
    failed_log = os.path.join(OUTPUT_DIR, "failed_downloads.json")
    with open(failed_log, "w", encoding="utf-8") as f:
        json.dump(failed_downloads, f, indent=2)
    print(f"⚠️  {len(failed_downloads)} downloads failed. See: {failed_log}\n")

# Generate summary report
summary = {
    "download_date": time.strftime("%Y-%m-%d %H:%M:%S"),
    "patch": latest_patch,
    "total_skins": len(skins),
    "was_downloaded": success_count,
    "was_skipped": skip_count,
    "meta_downloaded": meta_success,
    "meta_skipped": meta_skip,
    "failed": len(failed_downloads)
}

summary_path = os.path.join(OUTPUT_DIR, "download_summary.json")
with open(summary_path, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

# Print final summary
print(f"{'='*70}")
print(f"📊 DOWNLOAD SUMMARY")
print(f"{'='*70}")
print(f"Total skins:        {len(skins)}")
print(f"WAS downloaded:     {success_count}")
print(f"WAS skipped:        {skip_count}")
print(f"META downloaded:    {meta_success}")
print(f"META skipped:       {meta_skip}")
print(f"Failed:             {len(failed_downloads)}")
print(f"{'='*70}")
print(f"\n📁 Output directory: {os.path.abspath(OUTPUT_DIR)}")
print(f"📄 Summary saved to: {summary_path}\n")
