/**
 * Handles image loading with fallback for missing splash arts.
 * Uses ddragon CDN as reliable source.
 */
export class ImageCache {
  static FALLBACK_URL = 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Aatrox_0.jpg';

  /**
   * Gets the best available image URL for a skin.
   * Prioritizes CDN (ddragon) for reliability.
   * @param {Object} skin - Skin object with splashPath and imagePath
   * @returns {string} Image URL
   */
  static getImageUrl(skin) {
    // Prefer CDN (always available) over local paths
    return skin.splashPath || skin.imagePath || this.FALLBACK_URL;
  }

  /**
   * Handles image load errors by setting a fallback.
   * @param {HTMLImageElement} img - Image element that failed to load
   */
  static handleError(img) {
    if (!img.dataset.fallbackApplied) {
      img.dataset.fallbackApplied = 'true';
      img.src = this.FALLBACK_URL;
    }
  }
}
