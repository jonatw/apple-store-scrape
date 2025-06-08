import { defineConfig, devices } from '@playwright/test'

// Production test configuration
export default defineConfig({
  testDir: './e2e',
  timeout: 30000, // Longer timeout for production
  retries: 3,
  workers: 2, // Stable worker count for production
  use: {
    headless: true,
    baseURL: 'https://jonatw.github.io/apple-store-scrape',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],
  // No webServer for production - testing deployed site
})