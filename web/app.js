// ===================================
// League of Legends Skin Collection
// Modern 2026 Web Application - SPA Version
// ===================================

class SkinCollection {
  constructor() {
    this.allSkins = [];
    this.filteredSkins = [];
    this.currentFilter = "all";
    this.currentChampion = "";
    this.searchQuery = "";
    this.currentSort = "default";
    this.isBrowseLoaded = false;
    
    // Favorites
    this.favorites = new Set(JSON.parse(localStorage.getItem('skinFavorites') || '[]'));

    this.init();
  }

  async init() {
    await this.loadData();
    this.setupEventListeners();
    this.updateStats(); // Initial stats for Hero/Footer
  }

  async loadData() {
    try {
      // Load CSV data
      const response = await fetch("../data/skins_all.csv");
      const csvText = await response.text();
      this.allSkins = this.parseCSV(csvText);
      this.filteredSkins = [...this.allSkins];

      // Populate champion filter
      this.populateChampionFilter();
      
      console.log(`Loaded ${this.allSkins.length} skins.`);
    } catch (error) {
      console.error("Error loading data:", error);
      alert("Failed to load skin data. Please check file paths.");
    }
  }

  parseCSV(csv) {
    const lines = csv.trim().split("\n");
    // Normalize headers: remove quotes, trim
    const headers = lines[0].split(",").map(h => h.trim().replace(/^"|"$/g, ''));

    return lines.slice(1).map((line) => {
      // Handle simple CSV splitting (assuming no commas in values based on python script)
      const values = line.split(",");
      const skin = {};

      headers.forEach((header, index) => {
        skin[header] = values[index]?.trim() || "";
      });

      // Add computed properties
      skin.isChroma = (skin.chromas === "True");
      skin.isPrestige = (skin.skin_name || "").toLowerCase().includes("prestige");
      skin.isEsports = this.isEsportsSkin(skin.skin_name);
      
      // Robust Price Parsing
      let priceVal = skin.price || "0";
      skin.price = parseInt(priceVal.toString().replace(/[^0-9]/g, '')) || 0;
      
      skin.imagePath = `../assets/splash/${skin.champion}_${
        skin.skin_num
      }_${this.sanitizeFilename(skin.skin_name)}.jpg`;

      // Handle default skin name
      if(skin.skin_name === "default") {
          skin.skin_name = "Original " + skin.champion;
      }

      return skin;
    });
  }

  sanitizeFilename(name) {
    if(!name) return "";
    return name.replace(/[/:]/g, "-").replace(/'/g, "").replace(/ /g, "_");
  }

  isEsportsSkin(skinName) {
    if(!skinName) return false;
    const esportsTeams = [
      "T1", "DRX", "SKT", "SSG", "FPX", "iG", "DWG", "EDG", "Fnatic", "TPA",
    ];
    return esportsTeams.some((team) => skinName.includes(team));
  }

  populateChampionFilter() {
    const champions = [
      ...new Set(this.allSkins.map((skin) => skin.champion)),
    ].sort();
    const select = document.getElementById("championFilter");
    if(!select) return;

    champions.forEach((champion) => {
      const option = document.createElement("option");
      option.value = champion;
      option.textContent = champion;
      select.appendChild(option);
    });
  }

  setupEventListeners() {
    // SPA NAVIGATION
    document.getElementById("homeBtn").addEventListener("click", () => this.showSection("heroSection"));
    document.getElementById("browseBtn").addEventListener("click", () => this.loadAndShowBrowse());
    document.getElementById("heroBrowseBtn").addEventListener("click", () => this.loadAndShowBrowse());
    
    // Search
    const searchInput = document.getElementById("searchInput");
    const clearSearch = document.getElementById("clearSearch");

    searchInput.addEventListener("input", (e) => {
      this.searchQuery = e.target.value.toLowerCase();
      clearSearch.style.display = this.searchQuery ? "block" : "none";
      this.applyFilters();
    });

    clearSearch.addEventListener("click", () => {
      searchInput.value = "";
      this.searchQuery = "";
      clearSearch.style.display = "none";
      this.applyFilters();
    });

    // Filter chips
    document.querySelectorAll(".filter-chip").forEach((chip) => {
      chip.addEventListener("click", (e) => {
        const targetBtn = e.target.closest('.filter-chip');
        if(!targetBtn) return;

        document.querySelectorAll(".filter-chip").forEach((c) => c.classList.remove("active"));
        targetBtn.classList.add("active");
        
        this.currentFilter = targetBtn.dataset.filter;
        this.applyFilters();
      });
    });

    // Favorites Header Button -> Opens Browse filtered by Favorites
    const favBtn = document.getElementById("favoritesBtn");
    if(favBtn) {
        favBtn.addEventListener("click", () => {
             this.loadAndShowBrowse(); // Ensure loaded
             
             // Activate Favorites Filter Programmatically
             document.querySelectorAll(".filter-chip").forEach((c) => c.classList.remove("active"));
             const favChip = document.querySelector('.filter-chip[data-filter="favorites"]');
             if(favChip) favChip.classList.add("active");

             this.currentFilter = "favorites";
             this.applyFilters();
        });
    }

    // Champion filter
    document.getElementById("championFilter").addEventListener("change", (e) => {
        this.currentChampion = e.target.value;
        this.applyFilters();
    });
    
    // Sorting
    const sortControl = document.getElementById("sortControl");
    if(sortControl) {
        sortControl.addEventListener("change", (e) => {
            this.currentSort = e.target.value;
            this.applyFilters();
        });
    }

    // Modal Interactions
    const modal = document.getElementById("skinModal");
    const closeBtn = document.getElementById("closeModal");
    if(closeBtn) closeBtn.addEventListener("click", () => this.closeModal());
    if(modal) modal.addEventListener("click", (e) => {
      if (e.target.classList.contains("modal-overlay")) {
        this.closeModal();
      }
    });

    // Modal Favorite Toggle
    const modalFavBtn = document.getElementById("modalFavorite");
    if(modalFavBtn) {
        modalFavBtn.addEventListener("click", () => {
            const id = document.getElementById("modalSkinId").textContent;
            if(id) {
                this.toggleFavorite(id);
                // Update modal button state
                if(this.favorites.has(id)) modalFavBtn.classList.add('active');
                else modalFavBtn.classList.remove('active');
                
                if(this.currentFilter === 'favorites') this.applyFilters();
                this.updateStats();
            }
        });
    }

    // Keyboard shortcuts
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
          this.closeModal();
          document.getElementById('adminModal').style.display = 'none';
      }
    });

    // ADMIN DASHBOARD LOGIC
    const adminTrigger = document.getElementById("adminTrigger");
    const adminModal = document.getElementById("adminModal");
    const closeAdmin = document.getElementById("closeAdmin");
    
    if(adminTrigger && adminModal) {
        adminTrigger.addEventListener("click", () => {
            adminModal.style.display = "flex";
            this.updateAdminStats();
        });
        
        closeAdmin.addEventListener("click", () => {
             adminModal.style.display = "none";
        });
        
        adminModal.addEventListener("click", (e) => {
            if(e.target === adminModal) adminModal.style.display = "none";
        });
    }
  }

  updateAdminStats() {
      // Memory
      if(performance && performance.memory) {
          const used = Math.round(performance.memory.usedJSHeapSize / 1024 / 1024);
          const total = Math.round(performance.memory.jsHeapSizeLimit / 1024 / 1024);
          document.getElementById('admin_memory').textContent = `${used} / ${total} MB`;
      } else {
          document.getElementById('admin_memory').textContent = "Restricted";
      }
      
      // DOM
      document.getElementById('admin_dom').textContent = document.getElementsByTagName('*').length;
      
      // Assets (Images)
      document.getElementById('admin_assets').textContent = document.images.length;
      
      // Time to Interactive (Mock/Approx)
      const tti = Math.round(performance.now());
      document.getElementById('admin_tti').textContent = `${tti}ms`;
  }

  // SPA Logic
  showSection(sectionId) {
      // Hide all main sections
      document.getElementById("heroSection").style.display = "none";
      document.getElementById("browseSection").style.display = "none";
      
      // Update Nav Buttons
      document.querySelectorAll(".nav-btn").forEach(btn => btn.classList.remove("active"));
      
      if(sectionId === "heroSection") {
          document.getElementById("heroSection").style.display = "block";
          document.getElementById("homeBtn").classList.add("active");
      } else if (sectionId === "browseSection") {
          document.getElementById("browseSection").style.display = "block";
          document.getElementById("browseBtn").classList.add("active");
      }
      
      window.scrollTo(0, 0);
  }

  loadAndShowBrowse() {
      // Only render filters/grid if not done yet
      if(!this.isBrowseLoaded) {
          this.applyFilters();
          this.isBrowseLoaded = true;
      }
      this.showSection("browseSection");
  }

  toggleFavorite(skinId) {
      if (this.favorites.has(skinId)) {
          this.favorites.delete(skinId);
      } else {
          this.favorites.add(skinId);
      }
      localStorage.setItem('skinFavorites', JSON.stringify([...this.favorites]));
      
      // Update Grid Card if exists
      const card = document.querySelector(`.skin-card[data-skin-id="${skinId}"]`);
      if(card) {
          const favBtn = card.querySelector('.skin-card-favorite');
          if(favBtn) {
              if(this.favorites.has(skinId)) favBtn.classList.add('active');
              else favBtn.classList.remove('active');
          }
      }
      this.updateStats();
  }

  applyFilters() {
    this.filteredSkins = this.allSkins.filter((skin) => {
      // Search filter
      if (this.searchQuery) {
        const searchMatch =
          skin.champion.toLowerCase().includes(this.searchQuery) ||
          skin.skin_name.toLowerCase().includes(this.searchQuery);
        if (!searchMatch) return false;
      }

      // Champion filter
      if (this.currentChampion && skin.champion !== this.currentChampion) {
        return false;
      }

      // Type filter
      if (this.currentFilter === "chromas" && !skin.isChroma) return false;
      if (this.currentFilter === "prestige" && !skin.isPrestige) return false;
      if (this.currentFilter === "esports" && !skin.isEsports) return false;
      if (this.currentFilter === "favorites" && !this.favorites.has(skin.skin_id)) return false;

      return true;
    });
    
    // SORTING
    if (this.currentSort !== "default") {
        this.filteredSkins.sort((a, b) => {
            switch(this.currentSort) {
                case "date-newest":
                    return (b.release_date || '').localeCompare(a.release_date || '');
                case "date-oldest":
                    return (a.release_date || '').localeCompare(b.release_date || '');
                case "price-high":
                    return (b.price || 0) - (a.price || 0);
                case "price-low":
                    return (a.price || 0) - (b.price || 0);
                case "name-az":
                    return a.skin_name.localeCompare(b.skin_name);
                default:
                    return 0;
            }
        });
    }

    this.renderSkins();
  }

  renderSkins() {
    const grid = document.getElementById("skinsGrid");
    const loadingState = document.getElementById("loadingState");
    const emptyState = document.getElementById("emptyState");

    if(loadingState) loadingState.style.display = "none";

    if (this.filteredSkins.length === 0) {
      grid.innerHTML = "";
      if(emptyState) emptyState.style.display = "flex";
      return;
    }

    if(emptyState) emptyState.style.display = "none";

    // Optimized rendering
    grid.innerHTML = this.filteredSkins
      .map((skin) => this.createSkinCard(skin))
      .join("");

    // Add interactions
    grid.querySelectorAll(".skin-card").forEach((card, index) => {
        // Open Modal
        card.addEventListener("click", (e) => {
            if(!e.target.closest('.skin-card-favorite')) { 
                this.openModal(this.filteredSkins[index]);
            }
        });
        
        // Favorite Toggle
        const favBtn = card.querySelector('.skin-card-favorite');
        if(favBtn) {
            favBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggleFavorite(this.filteredSkins[index].skin_id);
            });
            
            // Mouse Enter (Pre-load image for parallax if needed)
        }
        
        // Parallax Effect
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = ((y - centerY) / centerY) * -10; 
            const rotateY = ((x - centerX) / centerX) * 10;
            
            const wrapper = card.querySelector('.skin-card-image-wrapper');
            if(wrapper) {
                const img = wrapper.querySelector('img');
                if(img) {
                    img.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.1) translateZ(10px)`;
                }
            }
        });
        
        card.addEventListener('mouseleave', () => {
            const wrapper = card.querySelector('.skin-card-image-wrapper');
            if(wrapper) {
                const img = wrapper.querySelector('img');
                if(img) img.style.transform = '';
            }
        });
    });
  }

  // Helper to generate badges
  getSkinBadges(skin) {
    const badges = [];
    
    // 1. Rarity Tags
    if (skin.price >= 3250) badges.push('<span class="badge badge-ultimate">Ultimate</span>');
    else if (skin.price >= 1820) badges.push('<span class="badge badge-legendary">Legendary</span>');
    else if (skin.price >= 1350) badges.push('<span class="badge badge-epic">Epic</span>');
    else if (skin.isPrestige) badges.push('<span class="badge badge-mythic">Mythic</span>'); // Fallback if no price but is prestige
    
    // 2. Type Tags
    if (skin.isPrestige) badges.push('<span class="badge badge-prestige">Prestige</span>');
    if (skin.skin_name.includes("Hextech")) badges.push('<span class="badge badge-hextech">Hextech</span>');
    
    // CORRECTED LOGIC: "chromas" column = True means skin HAS chromas available
    if (skin.isChroma) badges.push('<span class="badge badge-chroma">Chromas Available</span>');
    
    // 3. Collection Tags (Simple extraction)
    const collections = ["K/DA", "PROJECT", "Star Guardian", "Coven", "Spirit Blossom", "Blood Moon", "High Noon", "Pool Party", "Bewitching", "Snow Moon", "Arcana"];
    collections.forEach(col => {
        if(skin.skin_name.includes(col)) {
             badges.push(`<span class="badge badge-collection">${col}</span>`);
        }
    });

    return badges;
  }

  createSkinCard(skin) {
    const isFav = this.favorites.has(skin.skin_id);
    const badges = this.getSkinBadges(skin);

    return `
            <div class="skin-card" data-skin-id="${skin.skin_id}">
                <button class="skin-card-favorite ${isFav ? 'active' : ''}" title="Favorite">
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                        <path d="M10 3.5L12 8L17 8.5L13.5 12L14.5 17L10 14.5L5.5 17L6.5 12L3 8.5L8 8L10 3.5Z" stroke="currentColor" stroke-width="2" fill="${isFav ? 'currentColor' : 'none'}"/>
                    </svg>
                </button>
                <div class="skin-card-image-wrapper">
                    <img class="skin-card-image" src="${skin.imagePath}" alt="${skin.skin_name}" loading="lazy">
                    ${
                        badges.length
                        ? `<div class="skin-card-badges">${badges.join("")}</div>`
                        : ""
                    }
                </div>
                <div class="skin-card-info">
                    <div class="skin-card-title">${skin.skin_name}</div>
                    <div class="skin-card-champion">${skin.champion}</div>
                    ${skin.price ? `<div class="skin-card-price">${skin.price} RP</div>` : ''}
                </div>
            </div>
        `;
  }

  async openModal(skin) {
    const modal = document.getElementById("skinModal");

    document.getElementById("modalImage").src = skin.imagePath;
    document.getElementById("modalTitle").textContent = skin.skin_name;
    document.getElementById("modalChampion").textContent = skin.champion;
    document.getElementById("modalSkinId").textContent = skin.skin_id;
    document.getElementById("modalSkinNum").textContent = skin.skin_num;
    
    // Price
    const priceRow = document.getElementById("modalPriceRow");
    if (priceRow) {
        if (skin.price > 0 && skin.price < 99999) {
            priceRow.style.display = "flex";
            document.getElementById("modalPrice").textContent = `${skin.price} RP`;
        } else {
            priceRow.style.display = "none";
        }
    }

    // Release Date - FETCH FROM CDRAGON if missing
    const dateRow = document.getElementById("modalReleaseDateRow");
    // Default: clear it or show "Loading..."
    if (dateRow) {
         document.getElementById("modalReleaseDate").textContent = "Loading date...";
         dateRow.style.display = "flex";
         
         try {
             // Fetch metadata
             const res = await fetch(`https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/skins/${skin.skin_id}/${skin.skin_id}.json`);
             if(res.ok) {
                 const data = await res.json();
                 if(data.releaseDate) {
                     // data.releaseDate is usually a timestamp or string? 
                     // Usually format "2020-07-22" or similar
                     const d = new Date(data.releaseDate);
                     // Format: January 12, 2021
                     const dateStr = d.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
                     document.getElementById("modalReleaseDate").textContent = dateStr;
                 } else {
                     document.getElementById("modalReleaseDate").textContent = "Unknown";
                 }
             } else {
                 throw new Error("API 404");
             }
         } catch(e) {
             console.log("Could not fetch date", e);
             document.getElementById("modalReleaseDate").textContent = "N/A";
         }
    }

    // Badges
    const badges = this.getSkinBadges(skin);
    document.getElementById("modalBadges").innerHTML = badges.join("");
    
    // YouTube Link Logic
    const ytLink = document.getElementById("modalYouTubeLink");
    if (ytLink) {
        ytLink.style.display = "inline-flex";
        let query = "";
        if (skin.skin_name.toLowerCase().includes("default") || skin.skin_name.toLowerCase().includes("original")) {
             query = `League of Legends ${skin.champion} Base Skin Spotlight`;
        } else {
             if (skin.skin_name.toLowerCase().includes(skin.champion.toLowerCase())) {
                 query = `League of Legends ${skin.skin_name} Skin Spotlight`;
             } else {
                 query = `League of Legends ${skin.skin_name} ${skin.champion} Skin Spotlight`;
             }
        }
        ytLink.href = `https://www.youtube.com/results?search_query=${encodeURIComponent(query)}`;
    }

    // Favorite Button State
    const favBtn = document.getElementById("modalFavorite");
    if (favBtn) {
        if(this.favorites.has(skin.skin_id)) {
            favBtn.classList.add('active');
        } else {
            favBtn.classList.remove('active');
        }
    }

    modal.classList.add("active");
    document.body.style.overflow = "hidden";
  }

  closeModal() {
    const modal = document.getElementById("skinModal");
    if(modal) modal.classList.remove("active");
    document.body.style.overflow = "";
  }

  updateStats() {
    const totalSkins = this.allSkins.length;
    const totalChampions = new Set(this.allSkins.map((skin) => skin.champion)).size;
    const totalFavs = this.favorites.size;
    const totalChromas = this.allSkins.filter(s => s.isChroma).length;
    const realSkins = totalSkins - totalChromas;

    // Header Stats (Simplified)
    const favCountEl = document.getElementById("favoritesCount");
    if(favCountEl) favCountEl.textContent = totalFavs;
    
    // HERO STATS
    const heroSkins = document.getElementById("heroTotalSkins");
    const heroChamps = document.getElementById("heroTotalChamps");
    
    if(heroSkins) heroSkins.textContent = realSkins.toLocaleString();
    if(heroChamps) heroChamps.textContent = totalChampions.toLocaleString();
    
    // FOOTER STATS
    const footerStats = document.getElementById("footerStats");
    if(footerStats) footerStats.textContent = `${realSkins.toLocaleString()} Skins • ${totalChampions} Champions • ${totalChromas} Chromas`;

    // HERO STAT CARDS ONLY
    const pricedSkins = this.allSkins.filter(s => s.price > 0 && s.price < 99999);
    
    const updateStatCard = (cardId, skin, priceText) => {
        const card = document.getElementById(cardId);
        if(card && skin) {
            // Set icon background
            const icon = card.querySelector('.stat-icon');
            if(icon && skin.imagePath) {
                icon.style.backgroundImage = `url('${skin.imagePath}')`;
            }
            
            // Set value text
            const value = card.querySelector('.stat-value');
            if(value) value.textContent = priceText || skin.skin_name;
        }
    };

    if(pricedSkins.length > 0) {
        // Most Expensive
        const mostExpensive = pricedSkins.reduce((a, b) => a.price > b.price ? a : b);
        updateStatCard("statMostExpensive", mostExpensive, `${mostExpensive.price} RP`);
        
        // Cheapest
        const cheapest = pricedSkins.reduce((a, b) => a.price < b.price ? a : b);
        updateStatCard("statCheapest", cheapest, `${cheapest.price} RP`);
    }
    
    // Latest Release
    const datedSkins = this.allSkins.filter(s => s.release_date);
    if(datedSkins.length > 0) {
        const newest = datedSkins.reduce((a, b) => (a.release_date || '') > (b.release_date || '') ? a : b);
        updateStatCard("statLatest", newest, newest.release_date);
    }
  }

  showError(message) {
      alert(message);
  }
}

// Initialize app when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  new SkinCollection();
});
