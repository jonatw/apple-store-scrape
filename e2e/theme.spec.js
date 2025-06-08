import { test, expect } from '@playwright/test'
import { setupMockDataRoutes, waitForDataLoad } from './test-helpers.js'

test.describe('Apple Store Price Comparison - Theme Tests', () => {
  test.beforeEach(async ({ page }) => {
    await setupMockDataRoutes(page)
  })

  test('should respect system dark mode preference', async ({ page }) => {
    // Set system to prefer dark mode
    await page.emulateMedia({ colorScheme: 'dark' })
    
    await page.goto('/')
    await waitForDataLoad(page)
    
    // Should automatically use dark theme
    await expect(page.locator('html')).toHaveAttribute('data-bs-theme', 'dark')
    
    // Theme icon should be moon (dark mode)
    await expect(page.locator('#theme-toggle i')).toHaveClass(/fa-moon/)
  })

  test('should respect system light mode preference', async ({ page }) => {
    // Set system to prefer light mode
    await page.emulateMedia({ colorScheme: 'light' })
    
    await page.goto('/')
    await waitForDataLoad(page)
    
    // Should automatically use light theme
    await expect(page.locator('html')).toHaveAttribute('data-bs-theme', 'light')
    
    // Theme icon should be sun (light mode)
    await expect(page.locator('#theme-toggle i')).toHaveClass(/fa-sun/)
  })

  test('should override system preference when user manually sets theme', async ({ page }) => {
    // Set system to prefer dark mode
    await page.emulateMedia({ colorScheme: 'dark' })
    
    await page.goto('/')
    await waitForDataLoad(page)
    
    // Should start with dark theme
    await expect(page.locator('html')).toHaveAttribute('data-bs-theme', 'dark')
    
    // User clicks to switch to light theme
    await page.click('#theme-toggle')
    await page.waitForTimeout(500)
    
    // Should switch to light theme despite system preference
    await expect(page.locator('html')).toHaveAttribute('data-bs-theme', 'light')
    
    // Reload page
    await page.reload()
    await waitForDataLoad(page)
    
    // Should remember user preference (light) instead of system preference (dark)
    await expect(page.locator('html')).toHaveAttribute('data-bs-theme', 'light')
  })

  test('should respond to system theme changes when no manual preference is set', async ({ page }) => {
    // Start with light mode
    await page.emulateMedia({ colorScheme: 'light' })
    
    await page.goto('/')
    await waitForDataLoad(page)
    
    // Should start with light theme
    await expect(page.locator('html')).toHaveAttribute('data-bs-theme', 'light')
    
    // Change system preference to dark
    await page.emulateMedia({ colorScheme: 'dark' })
    await page.waitForTimeout(500)
    
    // Should automatically switch to dark theme
    await expect(page.locator('html')).toHaveAttribute('data-bs-theme', 'dark')
  })

  test('should not respond to system theme changes when user has manual preference', async ({ page }) => {
    // Start with dark mode
    await page.emulateMedia({ colorScheme: 'dark' })
    
    await page.goto('/')
    await waitForDataLoad(page)
    
    // User manually switches to light theme
    await page.click('#theme-toggle')
    await page.waitForTimeout(500)
    
    // Should be light theme
    await expect(page.locator('html')).toHaveAttribute('data-bs-theme', 'light')
    
    // Change system preference back to light (which is same as current)
    await page.emulateMedia({ colorScheme: 'light' })
    await page.waitForTimeout(500)
    
    // Then change system to dark
    await page.emulateMedia({ colorScheme: 'dark' })
    await page.waitForTimeout(500)
    
    // Should stay light because user has manual preference
    await expect(page.locator('html')).toHaveAttribute('data-bs-theme', 'light')
  })

  test('should clear manual preference and follow system when localStorage is cleared', async ({ page }) => {
    // Set system to dark mode
    await page.emulateMedia({ colorScheme: 'dark' })
    
    await page.goto('/')
    await waitForDataLoad(page)
    
    // User manually switches to light theme
    await page.click('#theme-toggle')
    await page.waitForTimeout(500)
    
    // Clear localStorage to simulate clearing preferences
    await page.evaluate(() => localStorage.clear())
    
    // Reload page
    await page.reload()
    await waitForDataLoad(page)
    
    // Should follow system preference (dark) again
    await expect(page.locator('html')).toHaveAttribute('data-bs-theme', 'dark')
  })

  test('should maintain theme consistency across page navigation', async ({ page }) => {
    // Set system to prefer dark mode
    await page.emulateMedia({ colorScheme: 'dark' })
    
    await page.goto('/')
    await waitForDataLoad(page)
    
    // Should start with dark theme
    await expect(page.locator('html')).toHaveAttribute('data-bs-theme', 'dark')
    
    // Switch between product categories
    await page.click('[data-product="ipad"]')
    await waitForDataLoad(page)
    
    // Theme should remain dark
    await expect(page.locator('html')).toHaveAttribute('data-bs-theme', 'dark')
    
    // Switch to another category
    await page.click('[data-product="mac"]')
    await waitForDataLoad(page)
    
    // Theme should still remain dark
    await expect(page.locator('html')).toHaveAttribute('data-bs-theme', 'dark')
  })
})