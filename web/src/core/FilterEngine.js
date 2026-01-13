
export class FilterEngine {
    constructor(skinData) {
        // Pre-compute search strings for performance (Phase 3 Optimization)
        this.allSkins = skinData.map(skin => ({
            ...skin,
            _searchStr: `${skin.champion} ${skin.skin_name}`.toLowerCase()
        }));
    }

    applyFilters(searchQuery, currentChampion, currentFilter, currentSort, favoritesSet) {
        let filteredSkins = this.allSkins.filter((skin) => {
            // Search filter (Optimized)
            if (searchQuery && !skin._searchStr.includes(searchQuery)) {
                return false;
            }

            // Champion filter
            if (currentChampion && skin.champion !== currentChampion) {
                return false;
            }

            // Type filter
            if (currentFilter === "chromas" && !skin.isChroma) return false;
            if (currentFilter === "prestige" && !skin.isPrestige) return false;
            if (currentFilter === "esports" && !skin.isEsports) return false;
            if (currentFilter === "favorites" && !favoritesSet.has(skin.skin_id)) return false;

            return true;
        });

        // SORTING
        if (currentSort !== "default") {
            filteredSkins.sort((a, b) => {
                switch (currentSort) {
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

        return filteredSkins;
    }
}
