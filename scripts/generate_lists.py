"""
Generate a curated, human-readable list of ALL League of Legends skins
Organized by champion with skin names and chroma information
"""
import csv
import os
from collections import defaultdict

# Configuration
CSV_PATH = "LOL_EXPORT_SKINS/skins_all.csv"
OUTPUT_MD = "LOL_SKINS_COMPLETE_LIST.md"
OUTPUT_TXT = "LOL_SKINS_COMPLETE_LIST.txt"

# Read skins from CSV
print(f"📖 Reading skins from {CSV_PATH}...")
skins_by_champion = defaultdict(list)

with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        champion = row["champion"]
        skin_name = row["skin_name"]
        chromas = row["chromas"]
        skin_num = row["skin_num"]
        
        skins_by_champion[champion].append({
            "name": skin_name,
            "chromas": chromas == "True",
            "num": int(skin_num)
        })

# Sort champions alphabetically
sorted_champions = sorted(skins_by_champion.keys())

# Generate Markdown version
print(f"📝 Generating {OUTPUT_MD}...")
with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.write("# League of Legends - Complete Skin List (2026)\n\n")
    f.write(f"**Total Champions:** {len(sorted_champions)}  \n")
    f.write(f"**Total Skins:** {sum(len(skins) for skins in skins_by_champion.values())}  \n\n")
    f.write("---\n\n")
    
    for champion in sorted_champions:
        skins = skins_by_champion[champion]
        f.write(f"## {champion}\n\n")
        f.write(f"**Total skins:** {len(skins)}\n\n")
        
        for skin in skins:
            chroma_indicator = "🎨" if skin["chromas"] else "  "
            f.write(f"{chroma_indicator} **{skin['name']}**")
            if skin["chromas"]:
                f.write(" *(has chromas)*")
            f.write("\n")
        
        f.write("\n")
    
    f.write("---\n\n")
    f.write("### Legend\n\n")
    f.write("- 🎨 = Skin has chromas available\n")
    f.write("- **default** = Base skin (no special cosmetic)\n")

# Generate plain text version
print(f"📝 Generating {OUTPUT_TXT}...")
with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
    f.write("=" * 80 + "\n")
    f.write("LEAGUE OF LEGENDS - COMPLETE SKIN LIST (2026)\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Total Champions: {len(sorted_champions)}\n")
    f.write(f"Total Skins: {sum(len(skins) for skins in skins_by_champion.values())}\n\n")
    f.write("=" * 80 + "\n\n")
    
    for champion in sorted_champions:
        skins = skins_by_champion[champion]
        f.write(f"{champion.upper()}\n")
        f.write("-" * len(champion) + "\n")
        f.write(f"Total skins: {len(skins)}\n\n")
        
        for skin in skins:
            chroma_text = " [CHROMAS]" if skin["chromas"] else ""
            f.write(f"  • {skin['name']}{chroma_text}\n")
        
        f.write("\n")

print(f"\n✅ Generated curated skin lists:")
print(f"   📄 {OUTPUT_MD} (Markdown format)")
print(f"   📄 {OUTPUT_TXT} (Plain text format)")

# Print summary statistics
total_skins = sum(len(skins) for skins in skins_by_champion.values())
skins_with_chromas = sum(
    sum(1 for skin in skins if skin["chromas"])
    for skins in skins_by_champion.values()
)

print(f"\n{'='*60}")
print(f"📊 STATISTICS")
print(f"{'='*60}")
print(f"Total Champions: {len(sorted_champions)}")
print(f"Total Skins: {total_skins}")
print(f"Skins with Chromas: {skins_with_chromas}")
print(f"Skins without Chromas: {total_skins - skins_with_chromas}")
print(f"{'='*60}\n")
