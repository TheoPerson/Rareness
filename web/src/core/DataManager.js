/**
 * Handles data fetching, parsing, and normalization for Skin data.
 */
export class DataManager {
  constructor() {
    this.allSkins = [];
  }

  /**
   * Loads pre-computed skin data from JSON with timeout protection.
   * @returns {Promise<Array>} Array of skin objects
   */
  async loadData() {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);

    try {
      const response = await fetch("/data/skins_all.json", {
        signal: controller.signal
      });
      clearTimeout(timeout);

      if (!response.ok) {
        throw new Error(`Failed to fetch data: ${response.status} ${response.statusText}`);
      }

      this.allSkins = await response.json();
      console.log(`[DataManager] Loaded ${this.allSkins.length} skins.`);
      return this.allSkins;
    } catch (error) {
      clearTimeout(timeout);
      if (error.name === 'AbortError') {
        throw new Error('Data loading timed out. Please refresh the page.');
      }
      console.error("[DataManager] Error loading data:", error);
      throw error;
    }
  }
}
