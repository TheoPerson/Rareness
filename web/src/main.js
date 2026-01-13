
import './styles/main.css';
import { SkinCollection } from './core/SkinCollection.js';
import { injectSpeedInsights } from '@vercel/speed-insights';

// Initialize Vercel Speed Insights
injectSpeedInsights();

document.addEventListener("DOMContentLoaded", () => {
  new SkinCollection();
});
