# 🎮 League of Legends - Complete Skin Collection Project

## 🎉 PROJECT COMPLETE!

A professional, modern web application to browse and explore **2,041 League of Legends skins** with beautiful UI, instant search, and smart filtering.

---

## ✅ What's Been Built

### 1. **Modern Web Application**

- 📱 Fully responsive design (desktop, tablet, mobile)
- 🌙 Dark theme with glassmorphism effects
- ⚡ Lightning-fast search and filtering
- 🎨 2026 modern UI/UX standards
- 🖼️ Full-size image previews in modal

### 2. **Complete Data Collection**

- ✅ 2,041 skins cataloged
- ✅ 172 champions
- ✅ 2,038 splash art images downloaded
- ✅ Champion metadata (JSON)
- ✅ CSV and JSON formats

### 3. **Professional Project Structure**

```
LOL-SKIN-COLLECTION/
├── 📂 web/              # Web application (READY TO USE!)
│   ├── index.html       # Main app
│   ├── styles.css       # Modern styling
│   ├── app.js           # Application logic
│   └── README.md        # Web app docs
│
├── 📂 data/             # Data files
│   ├── skins_all.csv    # 2,041 skins
│   ├── skins_all.json   # JSON format
│   └── meta.json        # Metadata
│
├── 📂 assets/           # Media assets
│   ├── splash/          # 2,038 splash arts (~3GB)
│   └── meta/            # Champion metadata
│
├── 📂 scripts/          # Utility scripts
│   ├── export_skins.py
│   ├── download_assets.py
│   ├── find_wad_files.py
│   └── generate_lists.py
│
├── 📂 docs/             # Documentation
│   ├── README.md
│   ├── EXTRACT_GAME_FILES.md
│   └── SKINS_LIST.md
│
└── launch_webapp.py     # Quick launcher
```

---

## 🚀 How to Use

### **Option 1: Quick Launch (Recommended)**

```bash
python launch_webapp.py
```

✅ Server starts automatically  
✅ Browser opens to http://localhost:8000/web/  
✅ Ready to browse!

### **Option 2: Direct File Open**

1. Navigate to `web/` folder
2. Double-click `index.html`
3. App opens in your default browser

### **Option 3: Manual Server**

```bash
python -m http.server 8000
# Visit: http://localhost:8000/web/
```

---

## 🎨 Features

### Search & Filter

- 🔍 **Instant Search** - Type to find any champion or skin
- 🎨 **Chroma Filter** - Show only skins with chromas
- ⭐ **Prestige Filter** - Filter prestige editions
- 🏆 **Esports Filter** - T1, DRX, SKT, and more
- 👤 **Champion Filter** - Dropdown to select specific champion

### User Experience

- ⚡ **Fast Loading** - Optimized performance
- 📱 **Responsive** - Works on all devices
- 🎯 **Click to Enlarge** - Full-size splash art previews
- ⌨️ **Keyboard Shortcuts** - `/` for search, `Esc` to close
- 🎭 **Smooth Animations** - 60fps transitions

### Design

- 🌙 **Dark Theme** - Easy on the eyes
- ✨ **Glassmorphism** - Modern frosted glass effects
- 🎨 **League Colors** - Signature gold (#C89B3C)
- 📐 **Minimalist** - Clean, distraction-free interface

---

## 📊 Statistics

| Metric                 | Count        |
| ---------------------- | ------------ |
| **Total Skins**        | 2,041        |
| **Champions**          | 172          |
| **Splash Arts**        | 2,038 images |
| **Skins with Chromas** | ~1,200+      |
| **Prestige Skins**     | ~100         |
| **Esports Skins**      | ~150         |
| **Data Size**          | ~3 GB        |
| **Patch Version**      | 16.1.1       |

---

## 🌐 Deploy Online (Future)

### GitHub Pages

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/lol-skins.git
git push -u origin main

# Enable GitHub Pages in repo settings
# Select: main branch, /web folder
```

### Netlify (One Command)

```bash
cd web
netlify deploy --prod
```

### Vercel

```bash
cd web
vercel --prod
```

---

## 🛠️ Technical Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: CSS Grid, Flexbox, Custom Properties
- **Data**: CSV parsing, client-side filtering
- **Server**: Python HTTP server (development)
- **Assets**: 2,038 splash art images (JPG)

### Why No Framework?

- ⚡ **Faster** - No build step, instant loading
- 🎯 **Simpler** - Easy to understand and modify
- 📦 **Smaller** - No dependencies, pure web standards
- 🚀 **Future-proof** - Works forever, no updates needed

---

## 📁 File Locations

### Data Files

- **CSV**: `data/skins_all.csv`
- **JSON**: `data/skins_all.json`
- **Metadata**: `data/meta.json`

### Images

- **Splash Arts**: `assets/splash/`
  - Format: `{Champion}_{SkinNum}_{SkinName}.jpg`
  - Example: `Ahri_15_K-DA_Ahri.jpg`

### Champion Metadata

- **Location**: `assets/meta/`
  - Format: `{Champion}.json`
  - Example: `Ahri.json`

---

## 🔧 Customization

### Change Colors

Edit `web/styles.css`:

```css
:root {
  --primary: #c89b3c; /* Gold */
  --bg-primary: #0a0e27; /* Dark blue */
  --accent-blue: #0ac8b9; /* Teal */
}
```

### Add New Filters

Edit `web/app.js` in the `applyFilters()` method:

```javascript
if (this.currentFilter === "mythic") {
  return skin.skin_name.includes("Mythic");
}
```

### Modify Grid Layout

Edit `web/styles.css`:

```css
.skins-grid {
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  /* Change 280px to adjust card size */
}
```

---

## ⚠️ Notes

### Image Paths

- Images must be in `assets/splash/` folder
- Filenames must match the pattern in `app.js`
- If images don't load, check browser console for 404 errors

### CORS Issues

- Use a local server (not direct file:// protocol)
- `launch_webapp.py` handles this automatically
- Or use: `python -m http.server 8000`

### Performance

- 2,041 skins load instantly (CSV parsing)
- Images lazy-load as you scroll
- Filtering is client-side (no server needed)

---

## 🎯 Next Steps (Optional Enhancements)

### Features to Add

- [ ] Favorites system (localStorage)
- [ ] Dark/Light theme toggle
- [ ] Skin comparison view
- [ ] Filter by year/patch
- [ ] Filter by skin line (PROJECT, K/DA, etc.)
- [ ] Sort options (alphabetical, newest, etc.)
- [ ] Grid/List view toggle
- [ ] Export filtered results

### Technical Improvements

- [ ] Add service worker (offline support)
- [ ] Implement virtual scrolling (better performance)
- [ ] Add image optimization
- [ ] Create backend API
- [ ] Add database (SQLite/PostgreSQL)
- [ ] User accounts and preferences

---

## 📄 License

All League of Legends assets are property of **Riot Games, Inc.**

This project is for **personal use only**. Do not redistribute Riot's assets commercially.

---

## 🤝 Support

### Troubleshooting

1. **Images not loading?**

   - Check `assets/splash/` folder exists
   - Verify file paths in browser DevTools
   - Use local server (not direct file open)

2. **Data not loading?**

   - Ensure `data/skins_all.csv` exists
   - Check browser console for errors
   - Try refreshing the page

3. **Slow performance?**
   - Clear browser cache
   - Close other tabs
   - Check image file sizes

### Getting Help

- Check `web/README.md` for detailed docs
- Review `docs/` folder for guides
- Inspect browser console for errors

---

## 🎉 Enjoy!

You now have a **complete, professional, modern web application** to browse all League of Legends skins!

**Features:**
✅ Beautiful 2026 UI  
✅ Instant search & filtering  
✅ 2,041 skins cataloged  
✅ 2,038 splash arts  
✅ Fully responsive  
✅ Ready to deploy online

**Made with ❤️ for League of Legends fans**

---

_Last Updated: January 13, 2026_  
_Patch Version: 16.1.1_  
_Total Skins: 2,041_
