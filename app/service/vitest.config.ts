import { defineConfig } from "vitest/config";

// Each test opens a whole in-process Postgres; starting one takes a few seconds.
export default defineConfig({ test: { testTimeout: 60_000, hookTimeout: 60_000 } });
