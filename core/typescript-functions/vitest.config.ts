import { defineConfig } from 'vitest/config';

// TAKE CARE WHEN MODIFYING THIS FILE. The configuration that is imported is required for vitest to work correctly
// out of the box. Ensure that any modifications you make do not conflict with the contents of the imported
// configuration. Also note that the imported configuration is likely to change across template versions.

const functionsVitestConfig = require('./build/configuration/vitest.config.functions.json');
// Keep parallel test load within CI capacity without relaxing assertions or timeouts.
export default defineConfig({
  ...functionsVitestConfig,
  test: { ...functionsVitestConfig.test, maxWorkers: 2 },
});
