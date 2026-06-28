import { defineConfig } from '@playwright/test';
export default defineConfig({ testDir: './tests/e2e', fullyParallel: true, reporter: 'line', use: { baseURL: 'file:///home/hermes/exercises-dataset' } });
