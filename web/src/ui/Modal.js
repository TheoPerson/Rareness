
import { BadgeFactory } from '../core/BadgeFactory.js';

export class Modal {
    constructor(favoritesSet, toggleFavoriteCallback) {
        this.favorites = favoritesSet;
        this.toggleFavoriteCallback = toggleFavoriteCallback;
        
        this.modal = document.getElementById("skinModal");
        this.adminModal = document.getElementById("adminModal");
        
        this.init();
    }

    init() {
        // Close Buttons
        const closeBtn = document.getElementById("closeModal");
        if (closeBtn) closeBtn.addEventListener("click", () => this.close());

        if (this.modal) {
            this.modal.addEventListener("click", (e) => {
                if (e.target.classList.contains("modal-overlay")) {
                    this.close();
                }
            });
        }
        
        // Favorite Button in Modal
        const modalFavBtn = document.getElementById("modalFavorite");
        if(modalFavBtn) {
            modalFavBtn.addEventListener("click", () => {
                const id = document.getElementById("modalSkinId").textContent;
                if(id && this.toggleFavoriteCallback) {
                    this.toggleFavoriteCallback(id);
                    // Update state immediately
                    if(this.favorites.has(id)) modalFavBtn.classList.add('active');
                    else modalFavBtn.classList.remove('active');
                }
            });
        }
        
        // Admin Modal
        const closeAdmin = document.getElementById("closeAdmin");
        if(closeAdmin) {
            closeAdmin.addEventListener("click", () => {
                if(this.adminModal) this.adminModal.style.display = "none";
            });
        }
        if(this.adminModal) {
            this.adminModal.addEventListener("click", (e) => {
                if(e.target === this.adminModal) this.adminModal.style.display = "none";
            });
        }
    }


    open(skin) {
        if (!this.modal) return;
        const sk = skin; // alias

        document.getElementById("modalImage").src = sk.imagePath;
        document.getElementById("modalTitle").textContent = sk.skin_name;
        document.getElementById("modalChampion").textContent = sk.champion;
        document.getElementById("modalSkinId").textContent = sk.skin_id;
        document.getElementById("modalSkinNum").textContent = sk.skin_num;

        // Price
        const priceRow = document.getElementById("modalPriceRow");
        if (priceRow) {
            if (sk.price > 0 && sk.price < 99999) {
                priceRow.style.display = "flex";
                document.getElementById("modalPrice").textContent = `${sk.price} RP`;
            } else {
                priceRow.style.display = "none";
            }
        }

        // Release Date
        this.updateReleaseDate(sk);

        // Badges
        const badgeContainer = document.getElementById("modalBadges");
        badgeContainer.innerHTML = "";
        const badges = BadgeFactory.getBadges(sk);
        badges.forEach(b => {
             badgeContainer.appendChild(BadgeFactory.createBadgeElement(b));
        });

        // YouTube Link
        this.updateYouTubeLink(sk);

        // Favorite State
        const favBtn = document.getElementById("modalFavorite");
        if (favBtn) {
            if (this.favorites.has(sk.skin_id)) {
                favBtn.classList.add('active');
                favBtn.setAttribute('aria-pressed', 'true');
            } else {
                favBtn.classList.remove('active');
                favBtn.setAttribute('aria-pressed', 'false');
            }
        }

        this.modal.classList.add("active");
        this.modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = "hidden";
        
        // Focus Management (Simple)
        const closeBtn = document.getElementById("closeModal");
        if(closeBtn) closeBtn.focus();
    }

    close() {
        if (this.modal) {
            this.modal.classList.remove("active");
            this.modal.setAttribute('aria-hidden', 'true');
        }
        if (this.adminModal) this.adminModal.style.display = 'none';
        document.body.style.overflow = "";
    }

    
    updateYouTubeLink(skin) {
         const ytLink = document.getElementById("modalYouTubeLink");
         if (!ytLink) return;
         
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

    async updateReleaseDate(skin) {
        const dateRow = document.getElementById("modalReleaseDateRow");
        if (!dateRow) return;

        document.getElementById("modalReleaseDate").textContent = "Loading date...";
        dateRow.style.display = "flex";

        try {
             // CORS might be an issue here if not proxied, but CDragon usually allows it.
             const res = await fetch(`https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/skins/${skin.skin_id}/${skin.skin_id}.json`);
             if(res.ok) {
                 const data = await res.json();
                 if(data.releaseDate) {
                     const d = new Date(data.releaseDate);
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
}
