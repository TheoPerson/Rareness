"""
🎮 LEAGUE OF LEGENDS SKIN COLLECTION - ENHANCED LAUNCHER
Modern 2026 Edition with Performance Monitoring
"""
import http.server
import socketserver
import webbrowser
import os
import sys
import time
import psutil
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

PORT = 8000
DIRECTORY = Path(__file__).parent

# Console colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║                                                                      ║")
    print("║   🎮  LEAGUE OF LEGENDS SKIN COLLECTION                              ║")
    print("║       ─────────────────────────────────────                          ║")
    print("║       Modern 2026 Web Application                                    ║")
    print("║                                                                      ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")

def get_memory_bar(percent, width=20):
    """Create a visual memory bar."""
    filled = int(width * percent / 100)
    bar = "█" * filled + "░" * (width - filled)
    color = Colors.GREEN if percent < 50 else Colors.YELLOW if percent < 80 else Colors.RED
    return f"{color}[{bar}]{Colors.END}"

def count_assets():
    """Count assets in the project."""
    stats = {
        "splash_images": 0,
        "total_size_mb": 0,
        "csv_rows": 0,
        "champions": set()
    }
    
    splash_dir = DIRECTORY / "assets" / "splash"
    if splash_dir.exists():
        for f in splash_dir.glob("*.jpg"):
            stats["splash_images"] += 1
            stats["total_size_mb"] += f.stat().st_size / (1024 * 1024)
            # Extract champion name
            champ = f.name.split("_")[0]
            stats["champions"].add(champ)
    
    csv_path = DIRECTORY / "data" / "skins_all.csv"
    if csv_path.exists():
        with open(csv_path, 'r', encoding='utf-8') as f:
            stats["csv_rows"] = sum(1 for _ in f) - 1  # Subtract header
    
    return stats

def print_system_info():
    """Print system and project info."""
    print(f"\n{Colors.BOLD}📊 SYSTEM STATUS{Colors.END}")
    print("─" * 60)
    
    # Memory
    mem = psutil.virtual_memory()
    mem_bar = get_memory_bar(mem.percent)
    print(f"  💾 Memory: {mem_bar} {mem.percent:.1f}% ({mem.used // (1024**3)}/{mem.total // (1024**3)} GB)")
    
    # CPU
    cpu_percent = psutil.cpu_percent(interval=0.5)
    cpu_bar = get_memory_bar(cpu_percent)
    print(f"  ⚡ CPU:    {cpu_bar} {cpu_percent:.1f}%")
    
    print()

def print_project_stats():
    """Print project statistics."""
    print(f"{Colors.BOLD}📁 PROJECT ASSETS{Colors.END}")
    print("─" * 60)
    
    stats = count_assets()
    
    print(f"  🖼️  Splash Images: {Colors.GREEN}{stats['splash_images']:,}{Colors.END}")
    print(f"  👤 Champions:     {Colors.GREEN}{len(stats['champions'])}{Colors.END}")
    print(f"  📋 Skins in CSV:  {Colors.GREEN}{stats['csv_rows']:,}{Colors.END}")
    print(f"  📦 Assets Size:   {Colors.YELLOW}{stats['total_size_mb']:.1f} MB{Colors.END}")
    print()

def print_cdn_info():
    """Print CDN vs Local info."""
    print(f"{Colors.BOLD}🌐 IMAGE DELIVERY{Colors.END}")
    print("─" * 60)
    print(f"  📍 Mode: {Colors.CYAN}Local Assets{Colors.END} (fastest for LAN)")
    print(f"  💡 Tip:  Images loaded from ./assets/splash/")
    print(f"  🔄 To use CDN: Edit app.js imagePath to use ddragon URLs")
    print()

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)
    
    def log_message(self, format, *args):
        # Custom logging with colors
        status = args[1] if len(args) > 1 else ""
        path = args[0].split()[1] if args else ""
        
        if "200" in str(status):
            color = Colors.GREEN
            emoji = "✅"
        elif "304" in str(status):
            color = Colors.CYAN
            emoji = "📦"
        elif "404" in str(status):
            color = Colors.RED
            emoji = "❌"
        else:
            color = Colors.YELLOW
            emoji = "⚠️"
        
        # Shorten path for display
        if len(path) > 50:
            path = "..." + path[-47:]
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"  {emoji} [{timestamp}] {color}{path}{Colors.END}")
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def main():
    clear_screen()
    print_banner()
    print_system_info()
    print_project_stats()
    print_cdn_info()
    
    print(f"{Colors.BOLD}🚀 SERVER STATUS{Colors.END}")
    print("─" * 60)
    
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            url = f"http://localhost:{PORT}/web/"
            
            print(f"  ✅ Server: {Colors.GREEN}RUNNING{Colors.END}")
            print(f"  🌐 URL:    {Colors.CYAN}{url}{Colors.END}")
            print(f"  📡 Port:   {Colors.YELLOW}{PORT}{Colors.END}")
            print()
            print(f"{Colors.BOLD}📝 REQUEST LOG{Colors.END}")
            print("─" * 60)
            
            # Auto-open browser
            try:
                webbrowser.open(url)
                print(f"  🌍 Browser opened automatically")
            except:
                print(f"  ⚠️  Please open: {url}")
            
            print()
            print(f"  {Colors.YELLOW}Press Ctrl+C to stop the server{Colors.END}")
            print()
            
            httpd.serve_forever()
            
    except OSError as e:
        if "10048" in str(e) or "Address already in use" in str(e):
            print(f"  {Colors.RED}❌ ERROR: Port {PORT} is already in use!{Colors.END}")
            print(f"  💡 Try closing other servers or use a different port.")
        else:
            raise e
    except KeyboardInterrupt:
        print(f"\n\n  {Colors.YELLOW}🛑 Server stopped gracefully{Colors.END}")
        print("─" * 60)

if __name__ == "__main__":
    main()
