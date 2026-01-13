import requests
import json
import csv
import os
from datetime import datetime

# Dossier de sortie
# Web App Data Directory
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web", "public", "data")
os.makedirs(BASE_DIR, exist_ok=True)

session = requests.Session()

def get_json(url):
    return session.get(url, timeout=10).json()

print("🔎 Récupération de la version LoL...")
PATCH = get_json(
    "https://ddragon.leagueoflegends.com/api/versions.json"
)[0]

print(f"📦 Patch utilisé : {PATCH}")

print("📜 Récupération de la liste des champions...")
champions = get_json(
    f"https://ddragon.leagueoflegends.com/cdn/{PATCH}/data/en_US/champion.json"
)["data"]

# Fetch Meraki Analytics Data for Prices and Dates
# Fetch Meraki Analytics Data for Prices and Dates
print("💰 Récupération des données Meraki Analytics (Prix & Dates)...")
meraki_index = {}

# 1. Fallback: Load from existing CSV first (if exists)
csv_path = os.path.join(BASE_DIR, "skins_all.csv")
if os.path.exists(csv_path):
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                s_id = row.get("skin_id")
                if s_id:
                    meraki_index[s_id] = {
                        "cost": row.get("price", 0),
                        "release": row.get("release_date", "")
                    }
        print(f"   📂 Chargé {len(meraki_index)} prix depuis le CSV local (fallback)")
    except Exception as e:
        print(f"   ⚠️ Impossible de lire le CSV local: {e}")

# 2. Try Online Fetch
try:
    meraki_data = get_json("https://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/skins.json")
    # Indexer par ID pour recherche rapide
    online_index = {str(skin["id"]): skin for skin in meraki_data.values()}
    if online_index:
        meraki_index = online_index # Overwrite with fresh data if successful
        print(f"   ✅ {len(meraki_index)} skins trouvés chez Meraki (Actualisé)")
except Exception as e:
    print(f"   ⚠️ Erreur Meraki (Utilisation du cache CSV si diponible): {e}")

# Helper Functions
def sanitize_filename(name):
    if not name: return ""
    return name.replace("/", "-").replace(":", "-").replace("'", "").replace(" ", "_")

def is_esports_skin(skin_name):
    if not skin_name: return False
    esports_teams = ["T1", "DRX", "SKT", "SSG", "FPX", "iG", "DWG", "EDG", "Fnatic", "TPA"]
    return any(team in skin_name for team in esports_teams)

# Processing
skins = []

for champ_name, champ_data in champions.items():
    print(f"➡️  {champ_name}")
    try:
        champ_json = get_json(
            f"https://ddragon.leagueoflegends.com/cdn/{PATCH}/data/en_US/champion/{champ_name}.json"
        )["data"][champ_name]
    except Exception as e:
        print(f"Failed to fetch {champ_name}: {e}")
        continue

    for skin in champ_json["skins"]:
        skin_id = str(skin["id"])
        meraki_info = meraki_index.get(skin_id, {})
        
        # Price Logic
        price = 0
        raw_price = meraki_info.get("cost", 0)
        if raw_price == "special": 
            price = 0
        else:
            try:
                price = int(raw_price)
            except:
                price = 0
        
        release_date = meraki_info.get("release", "")

        # Name Normalization
        original_name = skin["name"]
        display_name = original_name
        if display_name == "default":
            display_name = f"Original {champ_name}"

        # Computed Properties
        is_chroma = (skin.get("chromas") == True) # Python True boolean
        is_prestige = "prestige" in display_name.lower()
        is_esports = is_esports_skin(display_name)
        
        # Image Path
        # Format: /assets/splash/{Champion}_{SkinNum}_{SanitizedName}.jpg
        # Careful: DataManager used skin.skin_num which is an int, make sure to str it
        sanitized_name = sanitize_filename(original_name)
        image_path = f"/assets/splash/{champ_name}_{skin['num']}_{sanitized_name}.jpg"

        skins.append({
            "champion": champ_name,
            "champion_id": champ_data["key"],
            "skin_id": skin["id"],
            "skin_num": skin["num"],
            "skin_name": display_name,         # Normalized name
            "chromas": str(skin.get("chromas")), # Keep string for CSV compat if needed, but JSON prefers bool
            "isChroma": is_chroma,             # Pre-computed
            "isPrestige": is_prestige,         # Pre-computed
            "isEsports": is_esports,           # Pre-computed
            "price": price,
            "release_date": release_date,
            "imagePath": image_path,           # Pre-computed
            "patch": PATCH
        })

# JSON Export
with open(f"{BASE_DIR}/skins_all.json", "w", encoding="utf-8") as f:
    json.dump(skins, f, indent=2, ensure_ascii=False)

# CSV
with open(f"{BASE_DIR}/skins_all.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=skins[0].keys())
    writer.writeheader()
    writer.writerows(skins)

# Meta
meta = {
    "exported_at": datetime.utcnow().isoformat() + "Z",
    "patch": PATCH,
    "total_skins": len(skins)
}

with open(f"{BASE_DIR}/meta.json", "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2)

print(f"✅ EXPORT TERMINÉ : {len(skins)} skins")
