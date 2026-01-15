"""
Generate release dates JSON from Fandom Wiki SkinData.
This script downloads and parses the Fandom Wiki data, then saves it as a JSON file.
"""
import json
import re
import os

# Output path
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web", "public", "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "release_dates.json")

# The Fandom Wiki Lua data (will be loaded from a local cache or downloaded)
# Due to Cloudflare blocking requests, this needs to be fetched manually or cached

def parse_fandom_lua(lua_data):
    """Parse Fandom Wiki Lua table to extract release dates."""
    release_dates = {}
    
    # Find all champion positions for context
    champion_positions = []
    champ_pattern = re.compile(r'\["([A-Za-z\']+)"\]\s*=\s*\{\s*\["id"\]\s*=\s*\d+')
    for m in champ_pattern.finditer(lua_data):
        champion_positions.append((m.start(), m.group(1)))
    champion_positions.sort(key=lambda x: x[0])
    
    # Find all release dates and look back for skin names
    release_pattern = re.compile(r'\["release"\]\s*=\s*"(\d{4}-\d{2}-\d{2})"')
    skin_pattern = re.compile(r'\["([^"]+)"\]\s*=\s*\{')
    
    known_fields = {
        'id', 'skins', 'availability', 'looteligible', 'cost', 'release', 
        'set', 'neweffects', 'newanimations', 'newrecall', 'chromas',
        'voiceactor', 'splashartist', 'lore', 'filter', 'variant',
        'newvoice', 'newquotes', 'transforming', 'forms', 'distribution',
        'vu', 'retired', 'formatname', 'earlysale', 'removed'
    }
    
    for release_match in release_pattern.finditer(lua_data):
        release_date = release_match.group(1)
        release_pos = release_match.start()
        
        # Find the closest champion before this position
        current_champion = None
        for pos, champ_name in champion_positions:
            if pos < release_pos:
                current_champion = champ_name
            else:
                break
        
        if not current_champion:
            continue
        
        # Find the skin name by looking backwards
        search_start = max(0, release_pos - 2000)
        chunk = lua_data[search_start:release_pos]
        
        # Find all skin-like patterns in this chunk and take the last one
        skin_matches = list(skin_pattern.finditer(chunk))
        if skin_matches:
            skin_name = skin_matches[-1].group(1)
            # Skip if it matches a known field name
            if skin_name.lower() not in known_fields:
                key = f"{current_champion}:{skin_name}"
                release_dates[key] = release_date
    
    return release_dates

if __name__ == "__main__":
    # Try to load from cache file first
    # We look for a few variations
    potential_files = [
        "fandom_skindata.lua",
        "fandom_skindata_raw.lua", 
        "fandom_skindata_cache.txt"
    ]
    
    lua_data = None
    loaded_file = None
    
    for fname in potential_files:
        fpath = os.path.join(os.path.dirname(__file__), fname)
        if os.path.exists(fpath):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "return {" in content:
                        lua_data = content
                        loaded_file = fpath
                        break
            except Exception as e:
                print(f"Error reading {fname}: {e}")

    if not lua_data:
        print("\n" + "="*60)
        print("🛑 MISSING DATA FILE")
        print("To fetch the release dates, please do the following:")
        print("1. Open this URL in your browser:")
        print("   https://leagueoflegends.fandom.com/wiki/Module:SkinData/data?action=raw")
        print("2. Select All (Ctrl+A) and Copy (Ctrl+C)")
        print(f"3. Create a file named '{potential_files[0]}' in this folder:")
        print(f"   {os.path.dirname(__file__)}")
        print("4. Paste the content and save.")
        print("="*60 + "\n")
        exit(1)
    
    print(f"Loading data from: {loaded_file}")
    
    # Parse the data
    release_dates = parse_fandom_lua(lua_data)
    print(f"Parsed {len(release_dates)} release dates")
    
    # Save to JSON
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(release_dates, f, indent=2, ensure_ascii=False)
    
    print(f"Saved to: {OUTPUT_FILE}")
    
    # Print some samples
    print("\nSample entries:")
    for i, (key, date) in enumerate(release_dates.items()):
        if i >= 10:
            break
        print(f"  {key}: {date}")
