# Rareness v0.3 - GitHub Release Guide

## 📦 Creating the Release

### Step 1: Build the .exe

**Si le build automatique échoue**, lance PowerShell **en Administrateur** :

```powershell
cd C:\Users\theop\Desktop\Rareness-1
npm run desktop:build
```

**Sortie attendue :**

- `packages/desktop/release/Rareness-0.3.0-Portable.exe` (~150MB)

---

### Step 2: Créer la GitHub Release

1. **Va sur GitHub** : `https://github.com/TON_USERNAME/Rareness/releases/new`

2. **Tag version** : `v0.3.0`

3. **Release title** : `Rareness v0.3 - Desktop App`

4. **Description** :

```markdown
# Rareness v0.3 - League of Legends Account Value Calculator

## 🎮 Features

- Calculate your League account value in RP, USD, EUR
- Connects to League Client (LCU API)
- View your most valuable skins
- Works on Windows 10/11

## 📥 Download & Install

1. Download `Rareness-0.3.0-Portable.exe` below
2. Run the .exe (no installation needed)
3. Make sure League Client is running and logged in
4. Click "Analyze My Account"

## ⚠️ Requirements

- Windows 10 or 11
- League of Legends installed and running
```

5. **Attach file** : Drag `Rareness-0.3.0-Portable.exe` dans l'upload zone

6. **Publish release** ✅

---

### Step 3: Distribution

**Ton .exe est maintenant téléchargeable par tous** :

```
https://github.com/TON_USERNAME/Rareness/releases/download/v0.3.0/Rareness-0.3.0-Portable.exe
```

**Portable = pas d'installation** :

- ✅ Double-click to run
- ✅ No admin rights needed
- ✅ No dependencies
- ✅ Works from any folder

**Les users juste téléchargent et lancent !** 🚀

---

## 🛡️ Windows Defender Warning

**Normal** : Windows peut afficher "Windows protected your PC".

**Solution** :

1. Click "More info"
2. Click "Run anyway"

**Pourquoi ?** Le .exe n'est pas signé (code signing costs $$$).

**Pour éviter ça (futur)** :

- Acheter un certificat code signing (~$200/an)
- Ou utiliser open-source signing services

---

## 📊 Test Before Release

**Avant de publish** :

1. Test le .exe sur ton PC
2. Test sur un autre PC Windows si possible
3. Vérifie que League Client est détecté
4. Vérifie que les valeurs s'affichent

---

**Ready to rock! 🎸**
