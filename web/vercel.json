import { defineConfig } from "vite";
import path from "path";

export default defineConfig({
  server: {
    open: true,
    fs: {
      // Allow serving files from one level up to access 'data' and 'assets'
      allow: [".."],
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    outDir: "dist",
    emptyOutDir: true,
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: [], // Optional: functional tests might need setup
  },
});
