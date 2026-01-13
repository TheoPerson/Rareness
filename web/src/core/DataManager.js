/**
 * Handles data fetching, parsing, and normalization for Skin data.
 */
export class DataManager {
  constructor() {
    this.allSkins = [];
  }

  /**
   * Loads and parses skin data from CSV.
   * @returns {Promise<Array>} Array of skin objects
   */
  /**
   * Loads pre-computed skin data from JSON.
   * @returns {Promise<Array>} Array of skin objects
   */
  async loadData() {
    try {
      const response = await fetch("/data/skins_all.json");
      if (!response.ok) {
        throw new Error(`Failed to fetch data: ${response.status} ${response.statusText}`);
      }
      this.allSkins = await response.json();
      console.log(`[DataManager] Loaded ${this.allSkins.length} skins from JSON.`);
      return this.allSkins;
    } catch (error) {
      console.error("[DataManager] Error loading data:", error);
      throw error;
    }
  }
}
