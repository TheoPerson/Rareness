import { BadgeFactory } from '../core/BadgeFactory.js';

export class SkinCard {
    constructor(favoritesSet) {
        this.favorites = favoritesSet;
        // Pre-bind for performance if reusing listeners, though individual card listeners are easier for now.
    }

    createCardElement(skin, clickCallback, toggleFavoriteCallback) {
        // Main Container Construction (Optimized)

        // Favorite Button
        const isFav = this.favorites.has(skin.skin_id);
        
        // Re-do Card Container
        const cardDiv = document.createElement('div');
        cardDiv.className = 'skin-card';
        cardDiv.dataset.skinId = skin.skin_id; // For delegation
        cardDiv.setAttribute('tabindex', '0');
        cardDiv.setAttribute('role', 'button');
        cardDiv.setAttribute('aria-label', `View details for ${skin.skin_name}`);
        
        // Favorite Button
        const favBtnEl = document.createElement('button');
        favBtnEl.className = `skin-card-favorite ${isFav ? 'active' : ''}`;
        favBtnEl.dataset.skinId = skin.skin_id; // For delegation
        favBtnEl.title = isFav ? "Remove from Favorites" : "Add to Favorites";
        favBtnEl.setAttribute('aria-label', isFav ? "Remove from Favorites" : "Add to Favorites");
        favBtnEl.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true" style="pointer-events: none;">
                <path d="M10 3.5L12 8L17 8.5L13.5 12L14.5 17L10 14.5L5.5 17L6.5 12L3 8.5L8 8L10 3.5Z" stroke="currentColor" stroke-width="2" fill="${isFav ? 'currentColor' : 'none'}"/>
            </svg>
        `;

        // Image Wrapper
        const imgWrapper = document.createElement('div');
        imgWrapper.className = 'skin-card-image-wrapper';
        
        const img = document.createElement('img');
        img.className = 'skin-card-image';
        img.src = skin.imagePath;
        img.alt = ""; // Decorative if main label describes it, or use skin name? Using empty as card label covers it.
        img.loading = "lazy";
        imgWrapper.appendChild(img);

        // Badges
        const badges = BadgeFactory.getBadges(skin);
        if (badges.length > 0) {
            const badgeContainer = document.createElement('div');
            badgeContainer.className = 'skin-card-badges';
            badges.forEach(b => {
                badgeContainer.appendChild(BadgeFactory.createBadgeElement(b));
            });
            imgWrapper.appendChild(badgeContainer);
        }

        // Info
        const info = document.createElement('div');
        info.className = 'skin-card-info';
        
        const title = document.createElement('div');
        title.className = 'skin-card-title';
        title.textContent = skin.skin_name;
        
        const champion = document.createElement('div');
        champion.className = 'skin-card-champion';
        champion.textContent = skin.champion;
        
        info.appendChild(title);
        info.appendChild(champion);

        if (skin.price) {
            const price = document.createElement('div');
            price.className = 'skin-card-price';
            price.textContent = `${skin.price} RP`;
            info.appendChild(price);
        }

        // Assemble
        cardDiv.appendChild(favBtnEl);
        cardDiv.appendChild(imgWrapper);
        cardDiv.appendChild(info);

        // Optimized: No per-card listeners. Hover effect handled by CSS transform.
        // Parallax removed for performance on 2000+ items.
        
        return cardDiv;
    }
}
