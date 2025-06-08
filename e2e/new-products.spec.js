import { test, expect } from '@playwright/test'
import { setupMockDataRoutes, waitForDataLoad, switchToProduct, createMockProductData } from './test-helpers.js'

test.describe('Apple Store Price Comparison - New Products Tests', () => {
  test.beforeEach(async ({ page }) => {
    await setupMockDataRoutes(page)
  })

  test('should load and display Apple Watch data correctly', async ({ page }) => {
    await page.goto('/')
    await switchToProduct(page, 'watch')

    // Verify Watch data structure
    const mockData = createMockProductData('watch')
    
    // Check product count matches
    const displayedCount = await page.locator('#total-products').textContent()
    expect(parseInt(displayedCount)).toBe(mockData.products.length)
    
    // Verify table has the expected columns
    await expect(page.locator('#products-table thead')).toContainText('Product Name')
    await expect(page.locator('#products-table thead')).toContainText('US Price (USD)')
    await expect(page.locator('#products-table thead')).toContainText('Taiwan Price (TWD)')
    
    // Check for Watch-specific products
    await expect(page.locator('#products-table')).toContainText('Apple Watch')
    await expect(page.locator('#products-table')).toContainText('Series 10')
    await expect(page.locator('#products-table')).toContainText('Ultra 2')
    await expect(page.locator('#products-table')).toContainText('SE')
    
    // Check page title
    await expect(page.locator('#page-title')).toContainText('Apple WATCH Price Comparison')
  })

  test('should load and display AirPods data correctly', async ({ page }) => {
    await page.goto('/')
    await switchToProduct(page, 'airpods')

    // Verify AirPods data structure
    const mockData = createMockProductData('airpods')
    
    // Check product count matches
    const displayedCount = await page.locator('#total-products').textContent()
    expect(parseInt(displayedCount)).toBe(mockData.products.length)
    
    // Verify table has the expected columns
    await expect(page.locator('#products-table thead')).toContainText('Product Name')
    await expect(page.locator('#products-table thead')).toContainText('US Price (USD)')
    await expect(page.locator('#products-table thead')).toContainText('Taiwan Price (TWD)')
    
    // Check for AirPods-specific products
    await expect(page.locator('#products-table')).toContainText('AirPods')
    await expect(page.locator('#products-table')).toContainText('Pro')
    await expect(page.locator('#products-table')).toContainText('Max')
    
    // Check page title
    await expect(page.locator('#page-title')).toContainText('Apple AIRPODS Price Comparison')
  })

  test('should load and display Apple TV/Home data correctly', async ({ page }) => {
    await page.goto('/')
    await switchToProduct(page, 'tvhome')

    // Verify TV/Home data structure
    const mockData = createMockProductData('tvhome')
    
    // Check product count matches
    const displayedCount = await page.locator('#total-products').textContent()
    expect(parseInt(displayedCount)).toBe(mockData.products.length)
    
    // Verify table has the expected columns
    await expect(page.locator('#products-table thead')).toContainText('Product Name')
    await expect(page.locator('#products-table thead')).toContainText('US Price (USD)')
    await expect(page.locator('#products-table thead')).toContainText('Taiwan Price (TWD)')
    
    // Check for TV/Home-specific products
    await expect(page.locator('#products-table')).toContainText('Apple TV')
    await expect(page.locator('#products-table')).toContainText('HomePod')
    
    // Check page title
    await expect(page.locator('#page-title')).toContainText('Apple TVHOME Price Comparison')
  })

  test('should switch between all product categories', async ({ page }) => {
    await page.goto('/')
    await waitForDataLoad(page)

    // Test switching to Watch
    await switchToProduct(page, 'watch')
    await expect(page.locator('#page-title')).toContainText('Apple WATCH Price Comparison')
    await expect(page.locator('[data-product="watch"]')).toHaveClass(/active/)
    await expect(page.locator('#products-table')).toContainText('Apple Watch')

    // Test switching to AirPods
    await switchToProduct(page, 'airpods')
    await expect(page.locator('#page-title')).toContainText('Apple AIRPODS Price Comparison')
    await expect(page.locator('[data-product="airpods"]')).toHaveClass(/active/)
    await expect(page.locator('#products-table')).toContainText('AirPods')

    // Test switching to TV/Home
    await switchToProduct(page, 'tvhome')
    await expect(page.locator('#page-title')).toContainText('Apple TVHOME Price Comparison')
    await expect(page.locator('[data-product="tvhome"]')).toHaveClass(/active/)
    await expect(page.locator('#products-table')).toContainText('Apple TV')

    // Switch back to iPhone
    await switchToProduct(page, 'iphone')
    await expect(page.locator('#page-title')).toContainText('Apple IPHONE Price Comparison')
    await expect(page.locator('[data-product="iphone"]')).toHaveClass(/active/)
    await expect(page.locator('#products-table')).toContainText('iPhone')
  })

  test('should display navigation for all product categories', async ({ page }) => {
    await page.goto('/')
    
    // Should have all navigation tabs visible
    await expect(page.locator('[data-product="iphone"]')).toBeVisible()
    await expect(page.locator('[data-product="ipad"]')).toBeVisible()
    await expect(page.locator('[data-product="mac"]')).toBeVisible()
    await expect(page.locator('[data-product="watch"]')).toBeVisible()
    await expect(page.locator('[data-product="airpods"]')).toBeVisible()
    await expect(page.locator('[data-product="tvhome"]')).toBeVisible()

    // Should display correct text
    await expect(page.locator('[data-product="watch"]')).toContainText('Watch')
    await expect(page.locator('[data-product="airpods"]')).toContainText('AirPods')
    await expect(page.locator('[data-product="tvhome"]')).toContainText('TV & Home')
  })

  test('should filter products correctly in new categories', async ({ page }) => {
    await page.goto('/')
    await switchToProduct(page, 'watch')
    await waitForDataLoad(page)

    // Get initial row count
    const initialRowCount = await page.locator('#products-table tbody tr').count()
    expect(initialRowCount).toBeGreaterThan(0)

    // Search for "Ultra"
    await page.fill('#searchInput', 'Ultra')
    await page.waitForTimeout(500)

    // Should filter to Ultra products only
    const visibleProducts = await page.locator('#products-table tbody tr').all()
    for (const row of visibleProducts) {
      const productName = await row.locator('td:first-child').textContent()
      expect(productName?.toLowerCase()).toContain('ultra')
    }

    // Clear search
    await page.fill('#searchInput', '')
    await page.waitForTimeout(500)

    // Should return to original count
    const clearedRowCount = await page.locator('#products-table tbody tr').count()
    expect(clearedRowCount).toBe(initialRowCount)
  })

  test('should handle responsive design with new product categories', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 })
    
    await page.goto('/')
    await waitForDataLoad(page)

    // Should still display all navigation tabs
    await expect(page.locator('[data-product="watch"]')).toBeVisible()
    await expect(page.locator('[data-product="airpods"]')).toBeVisible()
    await expect(page.locator('[data-product="tvhome"]')).toBeVisible()

    // Should be able to switch products on mobile
    await switchToProduct(page, 'watch')
    await expect(page.locator('#page-title')).toContainText('Apple WATCH Price Comparison')
    
    await switchToProduct(page, 'airpods')
    await expect(page.locator('#page-title')).toContainText('Apple AIRPODS Price Comparison')
  })

  test('should maintain data consistency across all product categories', async ({ page }) => {
    await page.goto('/')
    await waitForDataLoad(page)

    // Test switching through all categories and back
    const categories = ['ipad', 'mac', 'watch', 'airpods', 'tvhome', 'iphone']
    
    for (const category of categories) {
      await switchToProduct(page, category)
      
      // Each category should have products
      const productCount = await page.locator('#total-products').textContent()
      expect(parseInt(productCount)).toBeGreaterThan(0)
      
      // Table should have data
      const tableRows = await page.locator('#products-table tbody tr').count()
      expect(tableRows).toBeGreaterThan(0)
      
      // Should have proper title
      const title = await page.locator('#page-title').textContent()
      expect(title).toContain(category.toUpperCase())
    }
  })
})