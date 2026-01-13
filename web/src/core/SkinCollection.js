
import { DataManager } from './DataManager.js';
import { FilterEngine } from './FilterEngine.js';
import { SkinCard } from '../ui/SkinCard.js';
import { Modal } from '../ui/Modal.js';

export class SkinCollection {
  constructor() {
    this.dataManager = new DataManager();
    this.filterEngine = null;
    this.skinCardV = null; 
    this.modal = null;

    // State
    this.allSkins = [];
    this.filteredSkins = [];
    this.currentFilter = "all";
    this.currentChampion = "";
    this.searchQuery = "";
    this.currentSort = "default";
    this.isBrowseLoaded = false;
    
    this.favorites = new Set(JSON.parse(localStorage.getItem('skinFavorites') || '[]'));

    // Initialize Helpers
    this.skinCardV = new SkinCard(this.favorites);
    this.modal = new Modal(this.favorites, (id) => this.toggleFavorite(id));

    this.initialize();
  }

  async initialize() {
    try {
        this.allSkins = await this.dataManager.loadData();
        this.filterEngine = new FilterEngine(this.allSkins);
        this.filteredSkins = [...this.allSkins];
        this.populateChampionFilter(); // Keep this call
        this.setupEventListeners();
        this.setupEventDelegation();
        this.updateStats(); 
    } catch (e) {
        console.error("Initialization failed", e);
        // Show user friendly error
        const grid = document.getElementById("skinsGrid");
        if(grid) grid.innerHTML = `<div class="error-message">Failed to load skins. Please ensure the data server is running.</div>`;
    }
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
    // Theme Toggle
    const themeToggle = document.getElementById("themeToggle");
    if(themeToggle) {
        themeToggle.addEventListener("click", () => {
            const isDark = document.body.dataset.theme === 'dark'; // Assuming default calls for light/dark
            // Actually, CSS variables are set on :root. We might need a class.
            // Let's toggle class 'light-mode' on body if default is dark, or vice versa.
            document.body.classList.toggle("light-theme");
            const isLight = document.body.classList.contains("light-theme");
            
            // Icon swap
             themeToggle.querySelector('.sun-icon').style.display = isLight ? 'none' : 'block';
             themeToggle.querySelector('.moon-icon').style.display = isLight ? 'block' : 'none';
        });
    }

    // SPA NAVIGATION
    const homeBtn = document.getElementById("homeBtn");
    if(homeBtn) homeBtn.addEventListener("click", () => this.showSection("heroSection"));
    
    const browseBtn = document.getElementById("browseBtn");
    if(browseBtn) browseBtn.addEventListener("click", () => this.loadAndShowBrowse());
    
    const heroBrowseBtn = document.getElementById("heroBrowseBtn");
    if(heroBrowseBtn) heroBrowseBtn.addEventListener("click", () => this.loadAndShowBrowse());
    
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
             // Force show section FIRST
             this.showSection("browseSection");
             
             // Then apply logic
             if(!this.isBrowseLoaded) this.isBrowseLoaded = true;
             
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

    // Keyboard shortcuts
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
          this.modal.close();
      }
    });

    // ADMIN DASHBOARD LOGIC (Simplified)
    const adminTrigger = document.getElementById("adminTrigger");
    const adminModal = document.getElementById("adminModal");
    
    if(adminTrigger && adminModal) {
        adminTrigger.addEventListener("click", () => {
            adminModal.style.display = "flex";
            this.updateAdminStats();
        });
    }

    // Close Admin
    const closeAdmin = document.getElementById("closeAdmin");
    if(closeAdmin) {
        closeAdmin.addEventListener("click", () => {
             adminModal.style.display = "none";
        });
    }
  }

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
      
      // Update Grid Card if exists (This is now handled by event delegation for immediate feedback)
      // const card = document.querySelector(`.skin-card[data-skin-id="${skinId}"]`);
      // if(card) {
      //     const favBtn = card.querySelector('.skin-card-favorite');
      //     if(favBtn) {
      //         if(this.favorites.has(skinId)) favBtn.classList.add('active');
      //         else favBtn.classList.remove('active');
      //     }
      // }
      this.updateStats();
  }

  applyFilters() {
    if(!this.filterEngine) return;
    
    this.filteredSkins = this.filterEngine.applyFilters(
        this.searchQuery,
        this.currentChampion,
        this.currentFilter,
        this.currentSort,
        this.favorites
    );

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

    // Optimized rendering with Infinite Scroll
    grid.innerHTML = "";
    this.currentRenderCount = 0;
    this.CHUNK_SIZE = 50;
    
    // Create Sentinel for Infinite Scroll
    this.observerSentinel = document.createElement('div');
    this.observerSentinel.className = 'scroll-sentinel';
    this.observerSentinel.style.height = '20px';
    this.observerSentinel.style.width = '100%';
    
    // Initial Render
    this.renderNextChunk();
    
    // Setup Intersection Observer
    if (this.scrollObserver) this.scrollObserver.disconnect();
    
    this.scrollObserver = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) {
            this.renderNextChunk();
        }
    }, { rootMargin: '200px' });
    
    grid.appendChild(this.observerSentinel);
    this.scrollObserver.observe(this.observerSentinel);
  }

  renderNextChunk() {
      const grid = document.getElementById("skinsGrid");
      // If we have rendered all, disconnect
      if (this.currentRenderCount >= this.filteredSkins.length) {
          if (this.scrollObserver) this.scrollObserver.disconnect();
          if (this.observerSentinel) this.observerSentinel.style.display = 'none';
          return;
      }

      const nextSkins = this.filteredSkins.slice(this.currentRenderCount, this.currentRenderCount + this.CHUNK_SIZE);
      const fragment = document.createDocumentFragment();

      nextSkins.forEach((skin) => {
          const card = this.skinCardV.createCardElement(skin); // Delegation handles events now
          fragment.appendChild(card);
      });

      // Insert before sentinel
      if (this.observerSentinel && this.observerSentinel.parentNode === grid) {
          grid.insertBefore(fragment, this.observerSentinel);
      } else {
          grid.appendChild(fragment);
      }
      
      this.currentRenderCount += nextSkins.length;
  }

  setupEventDelegation() {
    const grid = document.getElementById("skinsGrid");
    if(!grid) return;

    grid.addEventListener("click", (e) => {
        // 1. Handle Favorite Click
        const favBtn = e.target.closest('.skin-card-favorite');
        if (favBtn) {
            e.stopPropagation(); // Prevent card modal
            const skinId = favBtn.dataset.skinId;
            if(skinId) {
                this.toggleFavorite(skinId);
                // Immediate Visual Feedback
                favBtn.classList.toggle('active');
                const svg = favBtn.querySelector('svg path');
                if(svg) {
                    if(favBtn.classList.contains('active')) {
                        svg.setAttribute('fill', 'currentColor');
                        favBtn.setAttribute('aria-label', "Remove from Favorites");
                        favBtn.title = "Remove from Favorites";
                    } else {
                        svg.setAttribute('fill', 'none');
                        favBtn.setAttribute('aria-label', "Add to Favorites");
                        favBtn.title = "Add to Favorites";
                    }
                }
            }
            return;
        }

        // 2. Handle Card Click (Modal)
        const card = e.target.closest('.skin-card');
        if (card) {
            const skinId = card.dataset.skinId;
            if(skinId) {
                 const skin = this.getSkinById(skinId);
                 if(skin && this.modal) this.modal.open(skin);
            }
        }
    });

    // Keyboard Accessibility for Delegation
    grid.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
            const favBtn = e.target.closest('.skin-card-favorite');
            if (favBtn) {
                e.preventDefault();
                e.stopPropagation();
                favBtn.click(); // Reuse click logic
                return;
            }
            
            const card = e.target.closest('.skin-card');
            if (card && document.activeElement === card) {
                e.preventDefault();
                 const skinId = card.dataset.skinId;
                 if(skinId) {
                      const skin = this.getSkinById(skinId);
                      if(skin && this.modal) this.modal.open(skin);
                 }
            }
        }
    });
  }

  getSkinById(id) {
      return this.allSkins.find(s => s.skin_id == id);
  }

  updateStats() {
    try {
        const totalSkins = this.allSkins.length;
        const totalChampions = new Set(this.allSkins.map((skin) => skin.champion)).size;
        const totalFavs = this.favorites.size;
        const totalChromas = this.allSkins.filter(s => s.isChroma).length;
        const realSkins = totalSkins - totalChromas;

        // Header Stats
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

        // HERO STAT CARDS
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
            } else if (card) {
                // Fallback if no skin found (e.g. data load issue)
                const value = card.querySelector('.stat-value');
                if(value) value.textContent = "N/A";
            }
        };

        if(pricedSkins.length > 0) {
            // Most Expensive
            const mostExpensive = pricedSkins.reduce((a, b) => (a.price || 0) > (b.price || 0) ? a : b);
            updateStatCard("statMostExpensive", mostExpensive, `${mostExpensive.price} RP`);
            
            // Cheapest
            const cheapest = pricedSkins.reduce((a, b) => (a.price || 99999) < (b.price || 99999) ? a : b);
            updateStatCard("statCheapest", cheapest, `${cheapest.price} RP`);
        } else {
            updateStatCard("statMostExpensive", null, "N/A");
            updateStatCard("statCheapest", null, "N/A");
        }
        
        // Latest Release
        const datedSkins = this.allSkins.filter(s => s.release_date);
        if(datedSkins.length > 0) {
            const newest = datedSkins.reduce((a, b) => (a.release_date || '') > (b.release_date || '') ? a : b);
            updateStatCard("statLatest", newest, newest.release_date);
        } else {
             updateStatCard("statLatest", null, "N/A");
        }
    } catch (e) {
        console.warn("Stats update warning:", e);
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
}
