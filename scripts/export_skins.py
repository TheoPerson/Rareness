import requests
import json
import csv
import os
from datetime import datetime

# Dossier de sortie
BASE_DIR = "LOL_EXPORT_SKINS"
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
print("💰 Récupération des données Meraki Analytics (Prix & Dates)...")
try:
    meraki_data = get_json("https://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/skins.json")
    # Indexer par ID pour recherche rapide
    meraki_index = {str(skin["id"]): skin for skin in meraki_data.values()}
    print(f"   ✅ {len(meraki_index)} skins trouvés chez Meraki")
except Exception as e:
    print(f"   ⚠️ Erreur Meraki: {e}")
    meraki_index = {}

skins = []

for champ_name, champ_data in champions.items():
    print(f"➡️  {champ_name}")
    champ_json = get_json(
        f"https://ddragon.leagueoflegends.com/cdn/{PATCH}/data/en_US/champion/{champ_name}.json"
    )["data"][champ_name]

    for skin in champ_json["skins"]:
        skin_id = str(skin["id"])
        meraki_info = meraki_index.get(skin_id, {})
        
        # Extraire prix et date
        price = 0
        currency = "RP"
        release_date = ""
        
        if meraki_info:
            price = meraki_info.get("cost", 0)
            if price == "special": 
                price = 0 # Handle special cases if needed
            
            # Meraki returns release date usually, but sometimes it's missing
            release_date = meraki_info.get("release", "")

        skins.append({
            "champion": champ_name,
            "champion_id": champ_data["key"],
            "skin_id": skin["id"],
            "skin_num": skin["num"],
            "skin_name": skin["name"],
            "chromas": skin["chromas"],
            "price": price,
            "release_date": release_date,
            "patch": PATCH
        })

# JSON
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
