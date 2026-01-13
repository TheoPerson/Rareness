# League of Legends - Extract .wad.client Skin Files

## 🎯 What You're Looking For

You want the actual game files:

- **`.wad.client`** files - Game asset packages containing 3D models, textures, animations
- **`.skn`** files - Skin mesh/model files
- **`.dds`** files - Texture files
- **`.bin`** files - Binary data files
- **`.skl`** files - Skeleton/rigging files

These are NOT the web splash arts - these are the actual in-game 3D assets!

---

## 📍 Where Are These Files Located?

### Default League of Legends Installation Path:

```
C:\Riot Games\League of Legends\Game\DATA\FINAL\Champions\
```

Each champion has their own `.wad.client` file:

```
C:\Riot Games\League of Legends\Game\DATA\FINAL\Champions\Ahri.wad.client
C:\Riot Games\League of Legends\Game\DATA\FINAL\Champions\Yasuo.wad.client
C:\Riot Games\League of Legends\Game\DATA\FINAL\Champions\Jinx.wad.client
... etc
```

---

## 🛠️ Tools Needed to Extract

### 1. **Obsidian** (Recommended - Official WAD Editor)

- **GitHub:** https://github.com/Crauzer/Obsidian
- **Download:** https://github.com/Crauzer/Obsidian/releases/latest
- **Features:**
  - Modern UI
  - Extract individual files or entire archives
  - Browse WAD contents
  - No command line needed

### 2. **LtMAO Toolbox** (Alternative)

- **GitHub:** https://github.com/LeagueToolkit/LeagueToolkit
- Command-line tool for batch extraction

### 3. **Ritoddity** (Alternative)

- Older tool but still works
- Simple extraction interface

---

## 📋 Step-by-Step Extraction Guide

### Using Obsidian (Easiest Method)

#### Step 1: Download Obsidian

1. Go to https://github.com/Crauzer/Obsidian/releases/latest
2. Download `Obsidian.zip`
3. Extract to a folder (e.g., `C:\Tools\Obsidian\`)

#### Step 2: Download Hashtables (Required!)

1. Go to https://github.com/CommunityDragon/CDTB/tree/master/cdragontoolbox
2. Download these files:
   - `hashes.game.txt`
   - `hashes.lcu.txt`
3. Place them in: `C:\Tools\Obsidian\wad_hashtables\`

#### Step 3: Run Obsidian

1. Launch `Obsidian.exe`
2. Click **"Select League Folder"**
3. Navigate to: `C:\Riot Games\League of Legends\Game`
4. Click **"Restart"** when prompted

#### Step 4: Extract Skin Files

1. In Obsidian, navigate to: `DATA/FINAL/Champions/`
2. Click on a champion's `.wad.client` file (e.g., `Ahri.wad.client`)
3. You'll see folders like:
   - `assets/characters/ahri/skins/`
   - Each skin has folders: `base/`, `skin01/`, `skin02/`, etc.
4. Right-click on a file → **"Extract"** or **"Extract All"**

---

## 📁 File Structure Inside .wad.client

```
Ahri.wad.client
│
└── assets/characters/ahri/
    ├── skins/
    │   ├── base/           ← Default skin (skin 0)
    │   │   ├── ahri.skn    ← 3D model
    │   │   ├── ahri.dds    ← Texture
    │   │   ├── ahri.bin    ← Metadata
    │   │   └── animations/
    │   │
    │   ├── skin01/         ← Dynasty Ahri
    │   ├── skin02/         ← Midnight Ahri
    │   ├── skin03/         ← Foxfire Ahri
    │   └── ... (more skins)
    │
    └── animations/
```

---

## 🐍 Python Script to List All .wad.client Files

```python
import os
from pathlib import Path

# League of Legends installation path
LOL_PATH = r"C:\Riot Games\League of Legends\Game\DATA\FINAL\Champions"

# Check if path exists
if not os.path.exists(LOL_PATH):
    print(f"❌ League of Legends not found at: {LOL_PATH}")
    print("Please update LOL_PATH to your installation directory")
    exit()

# Find all .wad.client files
wad_files = list(Path(LOL_PATH).glob("*.wad.client"))

print(f"📦 Found {len(wad_files)} champion .wad.client files:\n")

for wad in sorted(wad_files):
    size_mb = wad.stat().st_size / (1024 * 1024)
    print(f"  {wad.name:<30} ({size_mb:.2f} MB)")

print(f"\n✅ Total champions: {len(wad_files)}")
print(f"📍 Location: {LOL_PATH}")
```

---

## 🔧 Batch Extraction Script

Save this as `extract_all_skins.py`:

```python
import os
import subprocess
from pathlib import Path

# Configuration
LOL_PATH = r"C:\Riot Games\League of Legends\Game\DATA\FINAL\Champions"
OUTPUT_PATH = r"C:\Users\theop\Desktop\Bureau\LOL SKINS\EXTRACTED_GAME_FILES"
OBSIDIAN_PATH = r"C:\Tools\Obsidian\Obsidian.exe"

# Create output directory
os.makedirs(OUTPUT_PATH, exist_ok=True)

# Get all .wad.client files
wad_files = list(Path(LOL_PATH).glob("*.wad.client"))

print(f"📦 Found {len(wad_files)} .wad.client files")
print(f"📂 Output: {OUTPUT_PATH}\n")

for wad in wad_files:
    champion_name = wad.stem  # Remove .wad.client extension
    output_dir = os.path.join(OUTPUT_PATH, champion_name)

    print(f"Extracting: {champion_name}...")

    # Command to extract using Obsidian CLI (if available)
    # Note: Obsidian may not have CLI - use GUI instead
    # This is a placeholder for manual extraction

print("\n✅ Please use Obsidian GUI to extract files manually")
print("   Navigate to each champion's .wad.client and extract")
```

---

## 📊 What's Inside Each Skin Folder?

| File Type     | Extension | Description                           |
| ------------- | --------- | ------------------------------------- |
| **Mesh**      | `.skn`    | 3D model geometry                     |
| **Skeleton**  | `.skl`    | Bone structure for animations         |
| **Texture**   | `.dds`    | Skin textures (diffuse, normal, etc.) |
| **Material**  | `.bin`    | Material properties                   |
| **Animation** | `.anm`    | Animation data                        |
| **Particles** | `.bin`    | VFX particle effects                  |

---

## ⚠️ Important Notes

1. **File Size**: Each champion's `.wad.client` can be 50-500 MB
2. **Total Size**: Extracting all champions = 20-50 GB
3. **Riot's Policy**: Extracting for personal use is generally tolerated, but:
   - Don't redistribute Riot's assets
   - Don't use for commercial purposes
   - Custom skins are "use at your own risk"

---

## 🔗 Useful Resources

- **Obsidian GitHub:** https://github.com/Crauzer/Obsidian
- **League Toolkit:** https://github.com/LeagueToolkit/LeagueToolkit
- **Community Dragon:** https://communitydragon.org/
- **Runeforge (Modding Guide):** https://runeforge.dev/

---

## 🎯 Next Steps

1. **Install Obsidian** from GitHub
2. **Download hashtables** (required for proper file names)
3. **Open your League installation** in Obsidian
4. **Navigate to Champions folder**
5. **Extract the .wad.client files** you need

Would you like me to create a script that:

- Locates your League installation automatically?
- Lists all available .wad.client files?
- Provides extraction commands?
