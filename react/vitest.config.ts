import path from "node:path";
import { defineConfig } from "vitest/config";

export default defineConfig({
  resolve: { alias: { "@": path.resolve(__dirname, "./src") } },
  esbuild: { jsx: "automatic" },
  test: {
    // OSDK component subpaths import CSS modules; transform them rather than Node-loading CSS.
    server: { deps: { inline: ["@osdk/react-components"] } },
  },
});
