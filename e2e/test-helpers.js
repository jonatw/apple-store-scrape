// Test helper functions for Apple Store Price Comparison E2E tests

/**
 * Create mock product data for testing
 * @param {string} productType - 'iphone', 'ipad', or 'mac'
 * @returns {Object} Mock product data
 */
export function createMockProductData(productType) {
  const mockData = {
    iphone: {
      metadata: {
        lastUpdated: new Date().toISOString(),
        exchangeRates: { USD: 1.0, TWD: 31.5 },
        regions: ['US', 'TW'],
        productType: 'iphone',
        totalProducts: 3
      },
      products: [
        {
          SKU_US: 'MYMG3LL/A',
          SKU_TW: 'MYMG3ZP/A',
          Price_US: 1199,
          Price_TW: 41900,
          PRODUCT_NAME: 'iPhone 16 Pro 256GB Black Titanium',
          price_difference_percent: 1.5,
          product_type: 'iphone'
        },
        {
          SKU_US: 'MYMA3LL/A',
          SKU_TW: 'MYMA3ZP/A',
          Price_US: 999,
          Price_TW: 31900,
          PRODUCT_NAME: 'iPhone 16 128GB Pink',
          price_difference_percent: 2.1,
          product_type: 'iphone'
        },
        {
          SKU_US: 'MYMC3LL/A',
          SKU_TW: 'MYMC3ZP/A',
          Price_US: 1399,
          Price_TW: 46900,
          PRODUCT_NAME: 'iPhone 16 Pro Max 512GB Natural Titanium',
          price_difference_percent: 1.8,
          product_type: 'iphone'
        }
      ]
    },
    ipad: {
      metadata: {
        lastUpdated: new Date().toISOString(),
        exchangeRates: { USD: 1.0, TWD: 31.5 },
        regions: ['US', 'TW'],
        productType: 'ipad',
        totalProducts: 3
      },
      products: [
        {
          SKU: 'MPMJ3LL/A',
          Price_US: 1299,
          Price_TW: 44900,
          PRODUCT_NAME: 'iPad Pro 13-inch Wi-Fi 256GB Space Black',
          price_difference_percent: 1.2,
          product_type: 'ipad'
        },
        {
          SKU: 'MPMD3LL/A',
          Price_US: 599,
          Price_TW: 19900,
          PRODUCT_NAME: 'iPad Air Wi-Fi 128GB Blue',
          price_difference_percent: 1.8,
          product_type: 'ipad'
        },
        {
          SKU: 'MPMF3LL/A',
          Price_US: 379,
          Price_TW: 12900,
          PRODUCT_NAME: 'iPad mini Wi-Fi 64GB Purple',
          price_difference_percent: 2.3,
          product_type: 'ipad'
        }
      ]
    },
    mac: {
      metadata: {
        lastUpdated: new Date().toISOString(),
        exchangeRates: { USD: 1.0, TWD: 31.5 },
        regions: ['US', 'TW'],
        productType: 'mac',
        totalProducts: 4
      },
      products: [
        {
          SKU: 'MU963',
          Price_US: 1999,
          Price_TW: 67900,
          PRODUCT_NAME: 'Mac Studio M2 Max',
          price_difference_percent: 2.3,
          product_type: 'mac'
        },
        {
          SKU: 'MCYT4',
          Price_US: 999,
          Price_TW: 33900,
          PRODUCT_NAME: 'Mac mini M2 256GB',
          price_difference_percent: 1.8,
          product_type: 'mac'
        },
        {
          SKU: 'MWUC3',
          Price_US: 1299,
          Price_TW: 44900,
          PRODUCT_NAME: 'iMac 24-inch M3 8-core CPU 256GB Silver',
          price_difference_percent: 1.2,
          product_type: 'mac'
        },
        {
          SKU: 'MYLH3',
          Price_US: 4999,
          Price_TW: 159900,
          PRODUCT_NAME: 'Pro Display XDR - Standard Glass',
          price_difference_percent: 1.5,
          product_type: 'mac'
        }
      ]
    },
    watch: {
      metadata: {
        lastUpdated: new Date().toISOString(),
        exchangeRates: { USD: 1.0, TWD: 31.5 },
        regions: ['US', 'TW'],
        productType: 'watch',
        totalProducts: 3
      },
      products: [
        {
          SKU: 'MRVW3',
          Price_US: 399,
          Price_TW: 12900,
          PRODUCT_NAME: 'Apple Watch Series 10 GPS 42mm Aluminum',
          price_difference_percent: 2.1,
          product_type: 'watch'
        },
        {
          SKU: 'MXL73',
          Price_US: 799,
          Price_TW: 26900,
          PRODUCT_NAME: 'Apple Watch Ultra 2 GPS + Cellular 49mm Titanium',
          price_difference_percent: 1.8,
          product_type: 'watch'
        },
        {
          SKU: 'MRTN3',
          Price_US: 249,
          Price_TW: 8900,
          PRODUCT_NAME: 'Apple Watch SE GPS 40mm Aluminum',
          price_difference_percent: 2.5,
          product_type: 'watch'
        }
      ]
    },
    airpods: {
      metadata: {
        lastUpdated: new Date().toISOString(),
        exchangeRates: { USD: 1.0, TWD: 31.5 },
        regions: ['US', 'TW'],
        productType: 'airpods',
        totalProducts: 3
      },
      products: [
        {
          SKU: 'MXP63',
          Price_US: 129,
          Price_TW: 4290,
          PRODUCT_NAME: 'AirPods (4th generation)',
          price_difference_percent: 1.5,
          product_type: 'airpods'
        },
        {
          SKU: 'MTJV3',
          Price_US: 249,
          Price_TW: 7990,
          PRODUCT_NAME: 'AirPods Pro (2nd generation) with USB-C',
          price_difference_percent: 1.8,
          product_type: 'airpods'
        },
        {
          SKU: 'MGYM3',
          Price_US: 549,
          Price_TW: 18900,
          PRODUCT_NAME: 'AirPods Max',
          price_difference_percent: 2.2,
          product_type: 'airpods'
        }
      ]
    },
    tvhome: {
      metadata: {
        lastUpdated: new Date().toISOString(),
        exchangeRates: { USD: 1.0, TWD: 31.5 },
        regions: ['US', 'TW'],
        productType: 'tvhome',
        totalProducts: 4
      },
      products: [
        {
          SKU: 'MN873',
          Price_US: 129,
          Price_TW: 4590,
          PRODUCT_NAME: 'Apple TV 4K Wi-Fi 64GB (3rd generation)',
          price_difference_percent: 2.8,
          product_type: 'tvhome'
        },
        {
          SKU: 'MN893',
          Price_US: 149,
          Price_TW: 5290,
          PRODUCT_NAME: 'Apple TV 4K Wi-Fi + Ethernet 128GB (3rd generation)',
          price_difference_percent: 2.5,
          product_type: 'tvhome'
        },
        {
          SKU: 'MPB93',
          Price_US: 299,
          Price_TW: 9900,
          PRODUCT_NAME: 'HomePod (2nd generation)',
          price_difference_percent: 1.5,
          product_type: 'tvhome'
        },
        {
          SKU: 'MY5G2',
          Price_US: 99,
          Price_TW: 3290,
          PRODUCT_NAME: 'HomePod mini',
          price_difference_percent: 1.2,
          product_type: 'tvhome'
        }
      ]
    }
  }

  return mockData[productType] || mockData.iphone
}

/**
 * Setup mock API routes for product data
 * @param {Page} page - Playwright page object
 */
export async function setupMockDataRoutes(page) {
  // Mock iPhone data
  await page.route('**/iphone_data.json', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(createMockProductData('iphone'))
    })
  })

  // Mock iPad data
  await page.route('**/ipad_data.json', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(createMockProductData('ipad'))
    })
  })

  // Mock Mac data
  await page.route('**/mac_data.json', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(createMockProductData('mac'))
    })
  })

  // Mock Apple Watch data
  await page.route('**/watch_data.json', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(createMockProductData('watch'))
    })
  })

  // Mock AirPods data
  await page.route('**/airpods_data.json', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(createMockProductData('airpods'))
    })
  })

  // Mock Apple TV/Home data
  await page.route('**/tvhome_data.json', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(createMockProductData('tvhome'))
    })
  })
}

/**
 * Wait for page to load and data to be displayed
 * @param {Page} page - Playwright page object
 * @param {number} timeout - Timeout in milliseconds
 */
export async function waitForDataLoad(page, timeout = 10000) {
  // Wait for the page to load
  await page.waitForSelector('#total-products', { timeout })
  
  // Wait for product count to be displayed (not "-")
  await page.waitForFunction(() => {
    const element = document.getElementById('total-products')
    return element && element.textContent !== '-' && element.textContent !== ''
  }, { timeout })

  // Wait for table to have data
  await page.waitForSelector('#products-table tbody tr', { timeout })
  
  // Ensure we're not showing loading state
  await page.waitForFunction(() => {
    const tbody = document.querySelector('#products-table tbody')
    if (!tbody) return false
    const loadingRow = tbody.querySelector('tr .loading')
    return !loadingRow
  }, { timeout })
}

/**
 * Get product count from summary
 * @param {Page} page - Playwright page object
 * @returns {Promise<number>} Product count
 */
export async function getProductCount(page) {
  const countText = await page.locator('#total-products').textContent()
  return parseInt(countText) || 0
}

/**
 * Get visible table rows (excluding header)
 * @param {Page} page - Playwright page object
 * @returns {Promise<number>} Number of visible rows
 */
export async function getVisibleRowCount(page) {
  return await page.locator('#products-table tbody tr').count()
}

/**
 * Switch to a product category
 * @param {Page} page - Playwright page object
 * @param {string} productType - 'iphone', 'ipad', or 'mac'
 */
export async function switchToProduct(page, productType) {
  const navLink = page.locator(`[data-product="${productType}"]`)
  await navLink.click()
  
  // Wait for the tab to become active
  await page.waitForFunction((type) => {
    const link = document.querySelector(`[data-product="${type}"]`)
    return link && link.classList.contains('active')
  }, productType)
  
  // Wait for data to load
  await waitForDataLoad(page)
}

/**
 * Update settings and wait for changes to apply
 * @param {Page} page - Playwright page object
 * @param {Object} settings - Settings object with exchangeRate and/or foreignFee
 */
export async function updateSettings(page, settings) {
  if (settings.exchangeRate !== undefined) {
    await page.fill('#exchangeRate', settings.exchangeRate.toString())
    await page.locator('#exchangeRate').dispatchEvent('input')
  }
  
  if (settings.foreignFee !== undefined) {
    await page.fill('#foreignFee', settings.foreignFee.toString())
    await page.locator('#foreignFee').dispatchEvent('input')
  }
  
  // Wait a moment for calculations to update
  await page.waitForTimeout(500)
}