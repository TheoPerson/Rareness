<div align="center">
  <img src="public/assets/logo.png" alt="Rareness Logo" width="120" />
</div>

# 🎮 League of Legends Skin Collection - Web App

A beautiful, modern web application to browse and explore all League of Legends skins.

## ✨ Features

- 🔍 **Instant Search** - Find any champion or skin
- 🎨 **Smart Filters** - Filter by chromas, prestige, esports skins
- 📱 **Fully Responsive** - Works on desktop, tablet, and mobile
- 🌙 **Dark Theme** - Easy on the eyes with glassmorphism effects
- ⚡ **Lightning Fast** - Smooth animations and instant filtering
- 🖼️ **Full-Size Previews** - Click any skin to view details

## 🚀 Quick Start

### Option 1: Direct File Open

1. Navigate to the `web/` folder
2. Double-click `index.html`
3. Your browser will open the app!

### Option 2: Local Server (Recommended)

```bash
# From the project root directory
python -m http.server 8000

# Then visit:
http://localhost:8000/web/
```

### Option 3: Using Node.js

```bash
npx serve web -p 8000
```

## 📁 Project Structure

```
LOL-SKIN-COLLECTION/
├── web/
│   ├── index.html      # Main application
│   ├── styles.css      # Modern 2026 styling
│   └── app.js          # Application logic
│
├── data/
│   ├── skins_all.csv   # Skin database (2,041 skins)
│   └── skins_all.json  # JSON format
│
├── assets/
│   ├── splash/         # 2,038 splash art images
│   └── meta/           # Champion metadata
│
├── scripts/            # Python utilities
└── docs/               # Documentation
```

## 🎨 Design Features

### Modern 2026 UI/UX

- **Minimalist Design** - Clean, distraction-free interface
- **Glassmorphism** - Frosted glass effects and blur
- **Smooth Animations** - 60fps transitions
- **Responsive Grid** - Adapts to any screen size
- **Accessible** - Keyboard shortcuts and screen reader support

### Color Palette

- **Primary Gold**: `#C89B3C` - League of Legends signature color
- **Dark Background**: `#0A0E27` - Deep, rich dark theme
- **Accent Blue**: `#0AC8B9` - Modern tech accent
- **Text**: `#F0E6D2` - High contrast, easy to read

## ⌨️ Keyboard Shortcuts

- `/` - Focus search bar
- `Esc` - Close modal
- `Arrow Keys` - Navigate (when implemented)

## 🔧 Customization

### Change Data Source

Edit `app.js` line 21:

```javascript
const response = await fetch("../data/skins_all.csv");
```

### Modify Image Paths

Edit `app.js` line 42:

```javascript
skin.imagePath = `../assets/splash/${skin.champion}_${skin.skin_num}_...`;
```

### Adjust Colors

Edit `styles.css` `:root` variables:

```css
:root {
  --primary: #c89b3c;
  --bg-primary: #0a0e27;
  /* ... more variables */
}
```

## 📊 Statistics

- **Total Skins**: 2,041
- **Total Champions**: 172
- **Splash Arts**: 2,038 images
- **Data Size**: ~3 GB
- **Patch Version**: 16.1.1

## 🌐 Deploy Online

### GitHub Pages

1. Push to GitHub repository
2. Enable GitHub Pages in Settings
3. Select `main` branch and `/web` folder
4. Your site will be live at `https://username.github.io/repo-name/`

### Netlify

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd web
netlify deploy --prod
```

### Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd web
vercel --prod
```

## 🔒 Local vs Online

### Current Setup (Local)

- ✅ Works offline
- ✅ Fast loading
- ✅ No hosting costs
- ❌ Only accessible on your computer

### For Online Deployment

1. Upload `assets/splash/` to CDN (Cloudflare R2, AWS S3)
2. Update image paths in `app.js`
3. Deploy `web/` folder to hosting service
4. Optional: Add backend API for dynamic data

## 🛠️ Tech Stack

- **HTML5** - Semantic markup
- **CSS3** - Modern features (Grid, Flexbox, Custom Properties)
- **Vanilla JavaScript** - No frameworks, pure performance
- **CSV Parsing** - Client-side data processing

## 📱 Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## 🐛 Troubleshooting

### Images Not Loading

- Check that `assets/splash/` contains the images
- Verify file paths in `app.js`
- Use browser DevTools to check network requests

### Data Not Loading

- Ensure `data/skins_all.csv` exists
- Check browser console for errors
- Try running with a local server (CORS issues)

### Slow Performance

- Reduce image quality
- Implement lazy loading (already included)
- Enable browser caching

## 📄 License

All League of Legends assets are property of Riot Games, Inc.
This project is for personal use only.

## 🤝 Contributing

Want to improve the app?

1. Add new filters (by year, by skin line)
2. Implement favorites system
3. Add comparison view
4. Create dark/light theme toggle

---

**Made with ❤️ for League of Legends fans**
