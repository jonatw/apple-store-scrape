import os from 'os'
import { defineConfig, devices } from '@playwright/test'

// Local development test configuration
export default defineConfig({
  testDir: './e2e',
  timeout: 10000,
  retries: 1,
  // Use all CPU cores locally for maximum parallelism; use 2 workers in CI for stable runs
  workers: process.env.CI ? 2 : os.cpus().length,
  use: {
    headless: process.env.CI ? true : false, // Headless in CI, headed locally
    baseURL: 'http://localhost:4173/apple-store-scrape',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'npm run preview',
    port: 4173,
    reuseExistingServer: true,
  },
})