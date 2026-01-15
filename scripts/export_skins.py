import requests
import json
import csv
import os
from datetime import datetime
from pathlib import Path

# Configuration
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(os.path.dirname(SCRIPTS_DIR), "web", "public", "data")
ASSETS_DIR = os.path.join(os.path.dirname(SCRIPTS_DIR), "web", "public", "assets", "splash")
RELEASE_DATES_FILE = os.path.join(SCRIPTS_DIR, "release_dates_final.json")
SPECIAL_PRICES_FILE = os.path.join(SCRIPTS_DIR, "special_skin_prices.json")

os.makedirs(BASE_DIR, exist_ok=True)

# Get latest patch
print("🔍 Fetching latest patch version...")
try:
    PATCH = requests.get("https://ddragon.leagueoflegends.com/api/versions.json", timeout=10).json()[0]
    print(f"✅ Using patch: {PATCH}")
except Exception as e:
    PATCH = "16.1.1"
    print(f"⚠️  Using fallback patch: {PATCH}")

# Load release dates
print(f"📅 Loading release dates...")
release_dates_map = {}
if os.path.exists(RELEASE_DATES_FILE):
    with open(RELEASE_DATES_FILE, "r", encoding="utf-8") as f:
        release_dates_map = json.load(f)
    print(f"✅ Loaded {len(release_dates_map)} release dates")
else:
    print(f"⚠️  No release dates file found")

# Load special skin prices (Mythic, Prestige, Victorious, etc.)
print(f"💎 Loading special skin prices...")
special_prices = {}
if os.path.exists(SPECIAL_PRICES_FILE):
    with open(SPECIAL_PRICES_FILE, "r", encoding="utf-8") as f:
        special_list = json.load(f)
        # Convert to lookup dict
        for entry in special_list:
            key = f"{entry['champion']}:{entry['skin']}"
            special_prices[key] = {"price": entry["price_rp"], "status": entry["status"]}
    print(f"✅ Loaded {len(special_prices)} special skin prices")
else:
    print(f"⚠️  No special prices file found")

# Fetch champion list
print("📥 Fetching champion list...")
champions_url = f"https://ddragon.leagueoflegends.com/cdn/{PATCH}/data/en_US/champion.json"
champions = requests.get(champions_url, timeout=15).json()["data"]
print(f"✅ Found {len(champions)} champions")

# Fetch Meraki Analytics Data for Prices and Dates
print("💰 Fetching Meraki Analytics data (Prices & Dates)...")
try:
    meraki_url = "https://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions.json"
    meraki_data = requests.get(meraki_url, timeout=20).json()
    print(f"✅ Meraki data loaded")
except Exception as e:
    print(f"⚠️  Meraki Analytics not available: {e}")
    meraki_data = {}

# Process all champions and skins
skins = []
validation_warnings = []

for champ_name, champ_data in champions.items():
    print(f"⚙️  {champ_name}")
    
    # Fetch detailed champion data
    champ_json_url = f"https://ddragon.leagueoflegends.com/cdn/{PATCH}/data/en_US/champion/{champ_name}.json"
    champ_json = requests.get(champ_json_url, timeout=10).json()["data"][champ_name]
    
    # Build Meraki index for fast lookup
    meraki_champ = meraki_data.get(champ_name, {})
    meraki_skins = meraki_champ.get("skins", [])
    meraki_index = {str(skin["id"]): skin for skin in meraki_skins}
    
    for skin in champ_json["skins"]:
        skin_id = str(skin["id"])
        skin_num = skin["num"]
        skin_name = skin["name"]
        
        # Skip default skins
        if skin_name == "default":
            continue
        
        # Get Meraki info
        meraki_info = meraki_index.get(skin_id, {})
        
        # === PRICE LOGIC ===
        # Priority: Special Prices DB > Meraki Analytics > Default
        price = None
        
        # 1. Check special prices database (Prestige, Victorious, Hextech, etc.)
        special_key = f"{champ_name}:{skin_name}"
        if special_key in special_prices:
            price_info = special_prices[special_key]
            price = price_info["price"] if price_info["price"] > 0 else None
        # 2. Check Meraki as fallback
        elif meraki_info:
            price = meraki_info.get("cost", 1350)
            if price == "special" or price == "Special":
                price = None
        # 3. Default
        else:
            price = 1350
        
        # Override for Prestige skins (if not in special DB)
        if "Prestige" in skin_name and price is None:
            price = None  # Keep as None (no RP price)
        
        # === RELEASE DATE LOGIC ===
        release_date = ""
        
        # Curated release dates take priority (more reliable)
        key1 = f"{champ_name}:{skin_name}"
        clean_name = skin_name.replace(champ_name, "").strip()
        key2 = f"{champ_name}:{clean_name}"
        
        if key1 in release_dates_map:
            release_date = release_dates_map[key1]
        elif key2 in release_dates_map:
            release_date = release_dates_map[key2]
        elif meraki_info and "release" in meraki_info:
            # Use Meraki as fallback, but validate it
            meraki_date = meraki_info["release"]
            # Filter out placeholder future dates (Meraki uses "2025-03-05" for unreleased skins)
            if meraki_date and meraki_date not in ["2025-03-05", "2026-01-01", "2099-12-31"]:
                release_date = meraki_date
        
        # === IMAGE PATH LOGIC ===
        # Use local assets if available, fallback to CDN
        safe_name = skin_name.replace("/", "-").replace(":", "").replace(" ", "_").replace("'", "")
        local_filename = f"{champ_name}_{skin_num}_{safe_name}.jpg"
        local_path = Path(ASSETS_DIR) / local_filename
        
        if local_path.exists():
            image_path = f"/assets/splash/{local_filename}"
        else:
            # Fallback to CDN
            image_path = f"https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{champ_name}_{skin_num}.jpg"
            validation_warnings.append(f"Missing local asset: {local_filename} (using CDN fallback)")
        
        # === BUILD SKIN ENTRY ===
        skin_entry = {
            "champion": champ_name,
            "champion_id": champ_data["key"],
            "skin_id": skin["id"],
            "skin_num": skin_num,
            "skin_name": skin_name,
            "chromas": skin.get("chromas", False),
            "price": price,
            "release_date": release_date,
            "imagePath": image_path,
            "splashPath": f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champ_name}_{skin_num}.jpg",
            "loadingPath": f"https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{champ_name}_{skin_num}.jpg",
            "isEsports": any(team in skin_name for team in ["T1", "DRX", "EDG", "DWG", "FPX", "IG", "SSG", "SKT T1", "TPA", "Fnatic"]),
            "isPrestige": "Prestige" in skin_name,
            "isChroma": False,  # Individual chromas not tracked
            "patch": PATCH
        }
        
        skins.append(skin_entry)

# === SAVE OUTPUT ===
print(f"\n💾 Saving data...")

# JSON
with open(f"{BASE_DIR}/skins_all.json", "w", encoding="utf-8") as f:
    json.dump(skins, f, indent=2, ensure_ascii=False)
print(f"✅ JSON: {BASE_DIR}/skins_all.json")

# CSV
if skins:
    with open(f"{BASE_DIR}/skins_all.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=skins[0].keys())
        writer.writeheader()
        writer.writerows(skins)
    print(f"✅ CSV: {BASE_DIR}/skins_all.csv")

# Meta
meta = {
    "exported_at": datetime.utcnow().isoformat() + "Z",
    "patch": PATCH,
    "total_skins": len(skins),
    "validation_warnings": len(validation_warnings)
}

with open(f"{BASE_DIR}/meta.json", "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2)
print(f"✅ Metadata: {BASE_DIR}/meta.json")

# Save validation warnings
if validation_warnings:
    with open(f"{BASE_DIR}/validation_warnings.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(validation_warnings))
    print(f"⚠️  {len(validation_warnings)} validation warnings saved")

print(f"\n{'='*70}")
print(f"✅ EXPORT COMPLETE: {len(skins)} skins exported")
print(f"   - With prices: {sum(1 for s in skins if s['price'] is not None)}")
print(f"   - With release dates: {sum(1 for s in skins if s['release_date'])}")
print(f"   - Using local assets: {sum(1 for s in skins if '/assets/' in s['imagePath'])}")
print(f"{'='*70}\n")
