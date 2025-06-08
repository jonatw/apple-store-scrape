import { test, expect } from '@playwright/test'
import { setupMockDataRoutes, waitForDataLoad, switchToProduct, updateSettings, getProductCount, getVisibleRowCount } from './test-helpers.js'

test.describe('Apple Store Price Comparison - User Interaction Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Set up mock data routes for each test
    await setupMockDataRoutes(page)
  })

  test('should load page with iPhone data by default', async ({ page }) => {
    await page.goto('/')
    await waitForDataLoad(page)

    // Should display iPhone products by default
    await expect(page.locator('#page-title')).toContainText('Apple IPHONE Price Comparison')
    
    // Should have the correct number of products
    const productCount = await getProductCount(page)
    expect(productCount).toBeGreaterThan(0)
    
    // iPhone tab should be active
    await expect(page.locator('[data-product="iphone"]')).toHaveClass(/active/)
    
    // Table should contain iPhone products
    await expect(page.locator('#products-table')).toContainText('iPhone')
  })

  test('should switch between product categories', async ({ page }) => {
    await page.goto('/')
    await waitForDataLoad(page)

    // Test switching to iPad
    await switchToProduct(page, 'ipad')
    await expect(page.locator('#page-title')).toContainText('Apple IPAD Price Comparison')
    await expect(page.locator('[data-product="ipad"]')).toHaveClass(/active/)
    await expect(page.locator('#products-table')).toContainText('iPad')

    // Test switching to Mac
    await switchToProduct(page, 'mac')
    await expect(page.locator('#page-title')).toContainText('Apple MAC Price Comparison')
    await expect(page.locator('[data-product="mac"]')).toHaveClass(/active/)
    await expect(page.locator('#products-table')).toContainText('Mac')

    // Switch back to iPhone
    await switchToProduct(page, 'iphone')
    await expect(page.locator('#page-title')).toContainText('Apple IPHONE Price Comparison')
    await expect(page.locator('[data-product="iphone"]')).toHaveClass(/active/)
    await expect(page.locator('#products-table')).toContainText('iPhone')
  })

  test('should update exchange rate and recalculate prices', async ({ page }) => {
    await page.goto('/')
    await waitForDataLoad(page)

    // Get initial average difference
    const initialAvgDiff = await page.locator('#avg-diff').textContent()
    const initialAvgDiffWithFee = await page.locator('#avg-diff-with-fee').textContent()

    // Update exchange rate
    await updateSettings(page, { exchangeRate: 32.0 })

    // Wait for recalculation
    await page.waitForTimeout(1000)

    // Average differences should change
    const newAvgDiff = await page.locator('#avg-diff').textContent()
    const newAvgDiffWithFee = await page.locator('#avg-diff-with-fee').textContent()

    expect(newAvgDiff).not.toBe(initialAvgDiff)
    expect(newAvgDiffWithFee).not.toBe(initialAvgDiffWithFee)

    // Exchange rate input should show the new value
    const exchangeRateValue = await page.locator('#exchangeRate').inputValue()
    expect(exchangeRateValue).toBe('32')
  })

  test('should update foreign transaction fee and recalculate', async ({ page }) => {
    await page.goto('/')
    await waitForDataLoad(page)

    // Get initial fee-adjusted difference
    const initialAvgDiffWithFee = await page.locator('#avg-diff-with-fee').textContent()

    // Update foreign fee
    await updateSettings(page, { foreignFee: 2.5 })

    // Wait for recalculation
    await page.waitForTimeout(1000)

    // Fee-adjusted difference should change
    const newAvgDiffWithFee = await page.locator('#avg-diff-with-fee').textContent()
    expect(newAvgDiffWithFee).not.toBe(initialAvgDiffWithFee)

    // Foreign fee input should show the new value
    const foreignFeeValue = await page.locator('#foreignFee').inputValue()
    expect(foreignFeeValue).toBe('2.5')
  })

  test('should filter products by search term', async ({ page }) => {
    await page.goto('/')
    await waitForDataLoad(page)

    // Get initial row count
    const initialRowCount = await getVisibleRowCount(page)
    expect(initialRowCount).toBeGreaterThan(0)

    // Search for "Pro"
    await page.fill('#searchInput', 'Pro')
    await page.waitForTimeout(500)

    // Should have fewer or equal rows
    const filteredRowCount = await getVisibleRowCount(page)
    expect(filteredRowCount).toBeLessThanOrEqual(initialRowCount)

    // All visible products should contain "Pro"
    const visibleProducts = await page.locator('#products-table tbody tr').all()
    for (const row of visibleProducts) {
      const productName = await row.locator('td:first-child').textContent()
      expect(productName?.toLowerCase()).toContain('pro')
    }

    // Clear search
    await page.fill('#searchInput', '')
    await page.waitForTimeout(500)

    // Should return to original count
    const clearedRowCount = await getVisibleRowCount(page)
    expect(clearedRowCount).toBe(initialRowCount)
  })

  test('should reset settings to defaults', async ({ page }) => {
    await page.goto('/')
    await waitForDataLoad(page)

    // Change settings
    await updateSettings(page, { 
      exchangeRate: 32.0, 
      foreignFee: 2.5 
    })

    // Verify changes
    expect(await page.locator('#exchangeRate').inputValue()).toBe('32')
    expect(await page.locator('#foreignFee').inputValue()).toBe('2.5')

    // Reset settings
    await page.click('#resetSettings')
    await page.waitForTimeout(500)

    // Should reset to defaults or empty (will use metadata defaults)
    const exchangeRateValue = await page.locator('#exchangeRate').inputValue()
    const foreignFeeValue = await page.locator('#foreignFee').inputValue()
    
    // Should be either empty (using defaults) or reset values
    expect(exchangeRateValue === '' || parseFloat(exchangeRateValue) === 31.5).toBeTruthy()
    expect(foreignFeeValue === '' || parseFloat(foreignFeeValue) === 1.5).toBeTruthy()

    // Search should be cleared
    expect(await page.locator('#searchInput').inputValue()).toBe('')
  })

  test('should toggle dark/light theme', async ({ page }) => {
    await page.goto('/')
    
    // Wait for theme initialization
    await page.waitForTimeout(1000)
    
    // Get initial theme (should respect system preference)
    const initialTheme = await page.locator('html').getAttribute('data-bs-theme')
    
    // Click theme toggle
    await page.click('#theme-toggle')
    await page.waitForTimeout(500)

    // Should switch to opposite theme
    const newTheme = await page.locator('html').getAttribute('data-bs-theme')
    expect(newTheme).not.toBe(initialTheme)

    // Click again to switch back
    await page.click('#theme-toggle')
    await page.waitForTimeout(500)

    // Should switch back to original theme
    const finalTheme = await page.locator('html').getAttribute('data-bs-theme')
    expect(finalTheme).toBe(initialTheme)
  })

  test('should persist settings in localStorage', async ({ page }) => {
    await page.goto('/')
    await waitForDataLoad(page)

    // Change settings
    await updateSettings(page, { 
      exchangeRate: 33.0, 
      foreignFee: 2.0 
    })

    // Reload page
    await page.reload()
    await waitForDataLoad(page)

    // Settings should be preserved
    expect(await page.locator('#exchangeRate').inputValue()).toBe('33')
    expect(await page.locator('#foreignFee').inputValue()).toBe('2')
  })

  test('should display purchase recommendations correctly', async ({ page }) => {
    await page.goto('/')
    await waitForDataLoad(page)

    // Should have recommendation badges in the table
    const recommendationBadges = page.locator('#products-table .badge')
    const badgeCount = await recommendationBadges.count()
    expect(badgeCount).toBeGreaterThan(0)

    // Should have different types of recommendations
    const badgeTexts = await recommendationBadges.allTextContents()
    const uniqueBadges = [...new Set(badgeTexts)]
    
    // Should have at least some recommendation types
    expect(uniqueBadges.length).toBeGreaterThan(0)
  })

  test('should handle responsive design on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 })
    
    await page.goto('/')
    await waitForDataLoad(page)

    // Should still display content properly
    await expect(page.locator('#total-products')).toBeVisible()
    await expect(page.locator('#products-table')).toBeVisible()
    
    // Navigation should be accessible
    await expect(page.locator('[data-product="iphone"]')).toBeVisible()
    await expect(page.locator('[data-product="ipad"]')).toBeVisible()
    await expect(page.locator('[data-product="mac"]')).toBeVisible()

    // Should be able to switch products on mobile
    await switchToProduct(page, 'mac')
    await expect(page.locator('#page-title')).toContainText('Apple MAC Price Comparison')
  })

  test('should display footer information correctly', async ({ page }) => {
    await page.goto('/')
    await waitForDataLoad(page)

    // Should display last updated information
    await expect(page.locator('#lastUpdated')).not.toContainText('-')
    
    // Should display exchange rate information
    await expect(page.locator('#currentExchangeRate')).toContainText('USD')
    await expect(page.locator('#currentExchangeRate')).toContainText('TWD')
    
    // Should display exchange rate source
    await expect(page.locator('#exchangeRateSource')).not.toContainText('Loading')
  })
})