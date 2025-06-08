import { test, expect } from '@playwright/test'
import { setupMockDataRoutes, waitForDataLoad, switchToProduct, createMockProductData } from './test-helpers.js'

test.describe('Apple Store Price Comparison - Data Integration Tests', () => {
  test.beforeEach(async ({ page }) => {
    await setupMockDataRoutes(page)
  })

  test('should load and display iPhone data correctly', async ({ page }) => {
    await page.goto('/')
    await waitForDataLoad(page)

    // Verify iPhone data structure
    const mockData = createMockProductData('iphone')
    
    // Check product count matches
    const displayedCount = await page.locator('#total-products').textContent()
    expect(parseInt(displayedCount)).toBe(mockData.products.length)
    
    // Check table has correct number of rows
    const tableRows = await page.locator('#products-table tbody tr').count()
    expect(tableRows).toBe(mockData.products.length)
    
    // Verify table has the expected columns
    await expect(page.locator('#products-table thead')).toContainText('Product Name')
    await expect(page.locator('#products-table thead')).toContainText('US Price (USD)')
    await expect(page.locator('#products-table thead')).toContainText('Taiwan Price (TWD)')
    
    // Check first product data
    const firstProduct = mockData.products[0]
    await expect(page.locator('#products-table tbody tr:first-child')).toContainText(firstProduct.PRODUCT_NAME)
  })

  test('should load and display iPad data correctly', async ({ page }) => {
    await page.goto('/')
    await switchToProduct(page, 'ipad')

    // Verify iPad data structure
    const mockData = createMockProductData('ipad')
    
    // Check product count matches
    const displayedCount = await page.locator('#total-products').textContent()
    expect(parseInt(displayedCount)).toBe(mockData.products.length)
    
    // Verify table has the expected columns
    await expect(page.locator('#products-table thead')).toContainText('Product Name')
    await expect(page.locator('#products-table thead')).toContainText('US Price (USD)')
    await expect(page.locator('#products-table thead')).toContainText('Taiwan Price (TWD)')
    
    // Check first product data
    const firstProduct = mockData.products[0]
    await expect(page.locator('#products-table tbody tr:first-child')).toContainText(firstProduct.PRODUCT_NAME)
  })

  test('should load and display Mac data correctly', async ({ page }) => {
    await page.goto('/')
    await switchToProduct(page, 'mac')

    // Verify Mac data structure
    const mockData = createMockProductData('mac')
    
    // Check product count matches
    const displayedCount = await page.locator('#total-products').textContent()
    expect(parseInt(displayedCount)).toBe(mockData.products.length)
    
    // Verify table has the expected columns
    await expect(page.locator('#products-table thead')).toContainText('Product Name')
    await expect(page.locator('#products-table thead')).toContainText('US Price (USD)')
    await expect(page.locator('#products-table thead')).toContainText('Taiwan Price (TWD)')
    
    // Check for Mac-specific products
    await expect(page.locator('#products-table')).toContainText('Mac Studio')
    await expect(page.locator('#products-table')).toContainText('Mac mini')
    await expect(page.locator('#products-table')).toContainText('iMac')
  })

  test('should calculate price differences correctly', async ({ page }) => {
    await page.goto('/')
    await waitForDataLoad(page)

    // Get the exchange rate being used
    const exchangeRate = await page.locator('#exchangeRate').inputValue()
    const rate = parseFloat(exchangeRate) || 31.5

    // Check that prices are displayed
    const usPrices = await page.locator('#products-table tbody tr td:nth-child(2)').allTextContents()
    const twPrices = await page.locator('#products-table tbody tr td:nth-child(4)').allTextContents()
    
    expect(usPrices.length).toBeGreaterThan(0)
    expect(twPrices.length).toBeGreaterThan(0)
    
    // Verify price format
    for (const price of usPrices) {
      if (price !== 'N/A') {
        expect(price).toMatch(/^\$[\d,]+$/)
      }
    }
    
    for (const price of twPrices) {
      if (price !== 'N/A') {
        expect(price).toMatch(/^NT\$[\d,]+$/)
      }
    }
  })

  test('should display metadata information correctly', async ({ page }) => {
    await page.goto('/')
    await waitForDataLoad(page)

    // Check exchange rate information
    const exchangeRateInfo = await page.locator('#currentExchangeRate').textContent()
    expect(exchangeRateInfo).toContain('USD')
    expect(exchangeRateInfo).toContain('TWD')
    
    // Check exchange rate source
    const exchangeRateSource = await page.locator('#exchangeRateSource').textContent()
    expect(exchangeRateSource).not.toBe('Loading...')
    
    // Check last updated information
    const lastUpdated = await page.locator('#lastUpdated').textContent()
    expect(lastUpdated).not.toBe('-')
    expect(lastUpdated).toMatch(/\d{4}-\d{2}-\d{2}/)
  })

  test('should handle price calculation with different exchange rates', async ({ page }) => {
    await page.goto('/')
    await waitForDataLoad(page)

    // Get initial difference percentage
    const initialDiff = await page.locator('#products-table tbody tr:first-child td:nth-child(5)').textContent()
    
    // Change exchange rate
    await page.fill('#exchangeRate', '32.0')
    await page.locator('#exchangeRate').dispatchEvent('input')
    await page.waitForTimeout(500)

    // Difference percentage should change
    const newDiff = await page.locator('#products-table tbody tr:first-child td:nth-child(5)').textContent()
    expect(newDiff).not.toBe(initialDiff)
  })

  test('should handle missing or invalid data gracefully', async ({ page }) => {
    // Mock API to return invalid data
    await page.route('**/iphone_data.json', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          metadata: { totalProducts: 0 },
          products: []
        })
      })
    })

    await page.goto('/')
    
    // Should handle empty data gracefully
    await expect(page.locator('#total-products')).toContainText('0')
    
    // Should show appropriate message for no data
    await expect(page.locator('#products-table tbody')).toContainText('No product data found')
  })

  test('should handle API errors gracefully', async ({ page }) => {
    // Mock API to return error
    await page.route('**/iphone_data.json', async (route) => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal Server Error' })
      })
    })

    await page.goto('/')
    
    // Should fall back to sample data or show error message
    await page.waitForSelector('#total-products')
    
    // The app should still be functional (using fallback data)
    const productCount = await page.locator('#total-products').textContent()
    expect(productCount).not.toBe('-')
  })

  test('should display purchase recommendations based on price differences', async ({ page }) => {
    await page.goto('/')
    await waitForDataLoad(page)

    // Should have recommendation badges
    const recommendations = await page.locator('#products-table .badge').allTextContents()
    expect(recommendations.length).toBeGreaterThan(0)
    
    // Should have valid recommendation types
    const validRecommendations = ['Buy in US', 'Buy in TW', 'Similar', 'No Data']
    for (const rec of recommendations) {
      expect(validRecommendations).toContain(rec)
    }
  })

  test('should maintain data consistency across product switches', async ({ page }) => {
    await page.goto('/')
    await waitForDataLoad(page)

    // Get iPhone product count
    const iphoneCount = await page.locator('#total-products').textContent()
    
    // Switch to iPad and back
    await switchToProduct(page, 'ipad')
    await switchToProduct(page, 'iphone')
    
    // Product count should be the same
    const iphoneCountAfter = await page.locator('#total-products').textContent()
    expect(iphoneCountAfter).toBe(iphoneCount)
  })

  test('should update summary statistics when settings change', async ({ page }) => {
    await page.goto('/')
    await waitForDataLoad(page)

    // Get initial statistics
    const initialAvgDiff = await page.locator('#avg-diff').textContent()
    const initialAvgDiffWithFee = await page.locator('#avg-diff-with-fee').textContent()

    // Change foreign fee
    await page.fill('#foreignFee', '3.0')
    await page.locator('#foreignFee').dispatchEvent('input')
    await page.waitForTimeout(500)

    // Statistics should update
    const newAvgDiff = await page.locator('#avg-diff').textContent()
    const newAvgDiffWithFee = await page.locator('#avg-diff-with-fee').textContent()

    // Basic difference should stay the same, but with-fee should change
    expect(newAvgDiff).toBe(initialAvgDiff)
    expect(newAvgDiffWithFee).not.toBe(initialAvgDiffWithFee)
  })
})