
import './styles/main.css';
import { SkinCollection } from './core/SkinCollection.js';
import { injectSpeedInsights } from '@vercel/speed-insights';

// Initialize Vercel Speed Insights for performance monitoring
injectSpeedInsights();

document.addEventListener("DOMContentLoaded", () => {
  new SkinCollection();
});
