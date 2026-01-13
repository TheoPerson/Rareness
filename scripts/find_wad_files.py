"""
League of Legends - Find and List .wad.client Files
Locates your LoL installation and lists all champion skin archives
"""
import os
import winreg
from pathlib import Path

def find_lol_installation():
    """Try to find League of Legends installation path from registry"""
    possible_paths = [
        r"C:\Riot Games\League of Legends",
        r"C:\Program Files\Riot Games\League of Legends",
        r"C:\Program Files (x86)\Riot Games\League of Legends",
        r"D:\Riot Games\League of Legends",
        r"E:\Riot Games\League of Legends",
    ]
    
    # Try registry first
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\League of Legends")
        install_location, _ = winreg.QueryValueEx(key, "InstallLocation")
        winreg.CloseKey(key)
        if os.path.exists(install_location):
            return install_location
    except:
        pass
    
    # Try common paths
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def get_wad_files(lol_path):
    """Get all .wad.client files from Champions folder"""
    champions_path = os.path.join(lol_path, "Game", "DATA", "FINAL", "Champions")
    
    if not os.path.exists(champions_path):
        return None, champions_path
    
    wad_files = list(Path(champions_path).glob("*.wad.client"))
    return wad_files, champions_path

def main():
    print("=" * 80)
    print("LEAGUE OF LEGENDS - .wad.client FILE FINDER")
    print("=" * 80)
    print()
    
    # Find LoL installation
    print("🔍 Searching for League of Legends installation...")
    lol_path = find_lol_installation()
    
    if not lol_path:
        print("❌ Could not find League of Legends installation!")
        print("\nPlease manually specify your installation path:")
        print("Example: C:\\Riot Games\\League of Legends")
        manual_path = input("\nEnter path (or press Enter to skip): ").strip()
        
        if manual_path and os.path.exists(manual_path):
            lol_path = manual_path
        else:
            print("\n❌ Invalid path. Exiting.")
            return
    
    print(f"✅ Found League of Legends at: {lol_path}\n")
    
    # Get .wad.client files
    print("📦 Searching for .wad.client files...")
    wad_files, champions_path = get_wad_files(lol_path)
    
    if wad_files is None:
        print(f"❌ Champions folder not found at: {champions_path}")
        print("\nExpected structure:")
        print("  League of Legends/")
        print("    └── Game/")
        print("        └── DATA/")
        print("            └── FINAL/")
        print("                └── Champions/  ← Should be here")
        return
    
    if not wad_files:
        print(f"❌ No .wad.client files found in: {champions_path}")
        return
    
    print(f"✅ Found {len(wad_files)} champion .wad.client files!\n")
    
    # Display files with sizes
    print("=" * 80)
    print(f"{'CHAMPION':<25} {'FILE SIZE':<15} {'FULL PATH'}")
    print("=" * 80)
    
    total_size = 0
    for wad in sorted(wad_files):
        champion_name = wad.stem  # Remove .wad.client
        size_bytes = wad.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        total_size += size_bytes
        
        print(f"{champion_name:<25} {size_mb:>10.2f} MB   {wad}")
    
    print("=" * 80)
    print(f"Total champions: {len(wad_files)}")
    print(f"Total size: {total_size / (1024**3):.2f} GB")
    print("=" * 80)
    print()
    
    # Save list to file
    output_file = "wad_files_list.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("League of Legends .wad.client Files\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Installation Path: {lol_path}\n")
        f.write(f"Champions Folder: {champions_path}\n")
        f.write(f"Total Files: {len(wad_files)}\n")
        f.write(f"Total Size: {total_size / (1024**3):.2f} GB\n\n")
        f.write("=" * 80 + "\n\n")
        
        for wad in sorted(wad_files):
            champion_name = wad.stem
            size_mb = wad.stat().st_size / (1024 * 1024)
            f.write(f"{champion_name:<25} {size_mb:>10.2f} MB   {wad}\n")
    
    print(f"📄 File list saved to: {output_file}\n")
    
    # Instructions
    print("=" * 80)
    print("🛠️  NEXT STEPS - HOW TO EXTRACT")
    print("=" * 80)
    print()
    print("1. Download Obsidian (WAD Editor):")
    print("   https://github.com/Crauzer/Obsidian/releases/latest")
    print()
    print("2. Download Hashtables (Required!):")
    print("   https://github.com/CommunityDragon/CDTB")
    print("   Files needed: hashes.game.txt, hashes.lcu.txt")
    print()
    print("3. In Obsidian:")
    print(f"   - Select League Folder: {lol_path}\\Game")
    print("   - Navigate to: DATA/FINAL/Champions/")
    print("   - Click on any .wad.client file to browse")
    print("   - Extract files you need")
    print()
    print("4. Skin files are located in:")
    print("   assets/characters/[champion]/skins/")
    print("   - base/ = default skin (skin 0)")
    print("   - skin01/ = first skin")
    print("   - skin02/ = second skin")
    print("   - etc.")
    print()
    print("=" * 80)
    print()
    
    # Ask if user wants to open the folder
    response = input("Would you like to open the Champions folder now? (y/n): ").strip().lower()
    if response == 'y':
        os.startfile(champions_path)
        print(f"\n✅ Opened: {champions_path}")

if __name__ == "__main__":
    main()
