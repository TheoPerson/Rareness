
export const BadgeType = {
    ULTIMATE: 'ultimate',
    LEGENDARY: 'legendary',
    EPIC: 'epic',
    MYTHIC: 'mythic',
    PRESTIGE: 'prestige',
    HEXTECH: 'hextech',
    CHROMA: 'chroma',
    COLLECTION: 'collection'
};

export class BadgeFactory {
    static getBadges(skin) {
        const badges = [];

        // 1. Rarity
        if (skin.price >= 3250) badges.push({ type: BadgeType.ULTIMATE, label: 'Ultimate' });
        else if (skin.price >= 1820) badges.push({ type: BadgeType.LEGENDARY, label: 'Legendary' });
        else if (skin.price >= 1350) badges.push({ type: BadgeType.EPIC, label: 'Epic' });
        else if (skin.isPrestige) badges.push({ type: BadgeType.MYTHIC, label: 'Mythic' });

        // 2. Type
        if (skin.isPrestige) badges.push({ type: BadgeType.PRESTIGE, label: 'Prestige' });
        if (skin.skin_name.includes("Hextech")) badges.push({ type: BadgeType.HEXTECH, label: 'Hextech' });
        if (skin.isChroma) badges.push({ type: BadgeType.CHROMA, label: 'Chromas' });

        // 3. Collections (Partial List)
        const collections = ["K/DA", "PROJECT", "Star Guardian", "Coven", "Spirit Blossom", "Blood Moon", "High Noon", "Pool Party", "Bewitching", "Snow Moon", "Arcana"];
        for (const col of collections) {
            if (skin.skin_name.includes(col)) {
                badges.push({ type: BadgeType.COLLECTION, label: col });
                break; // Often only one major collection per skin
            }
        }

        return badges;
    }

    static createBadgeElement(badge) {
        const span = document.createElement('span');
        span.className = `badge badge-${badge.type}`;
        span.textContent = badge.label;
        return span;
    }
}
