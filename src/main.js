// Global variables
let currentProduct = 'iphone';
let productData = null;
let exchangeRate = 31.5;
let cardFee = 1.5;

// ==================== Dark Mode Settings ====================

// Initialize theme
function initTheme() {
  // Check locally stored theme settings
  const savedTheme = localStorage.getItem('theme');
  
  if (savedTheme) {
    // Use saved theme
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
    updateThemeIcon(savedTheme);
  } else {
    // Use system preference
    const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = prefersDarkMode ? 'dark' : 'light';
    
    // Debug logging for development
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      console.log(`System prefers dark mode: ${prefersDarkMode}`);
      console.log(`Setting theme to: ${theme}`);
    }
    
    document.documentElement.setAttribute('data-bs-theme', theme);
    updateThemeIcon(theme);
  }
  
  // Listen for system theme changes
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    // Only update if no manual preference is stored
    if (!localStorage.getItem('theme')) {
      const newTheme = e.matches ? 'dark' : 'light';
      document.documentElement.setAttribute('data-bs-theme', newTheme);
      updateThemeIcon(newTheme);
      
      if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        console.log(`System theme changed to: ${newTheme}`);
      }
    }
  });
  
  // Set theme toggle listener
  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
}

// Update theme icon
function updateThemeIcon(theme) {
  const icon = document.querySelector('#theme-toggle i');
  if (theme === 'dark') {
    icon.className = 'fas fa-moon fs-5';
  } else {
    icon.className = 'fas fa-sun fs-5';
  }
}

// Toggle theme
function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-bs-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  
  document.documentElement.setAttribute('data-bs-theme', newTheme);
  localStorage.setItem('theme', newTheme);
  
  updateThemeIcon(newTheme);
}

// ==================== Calculation and Formatting Functions ====================

// Format currency display
function formatCurrency(amount, currency) {
  if (amount === null || amount === undefined) return '-';
  
  const formatter = new Intl.NumberFormat('zh-TW', {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  });
  
  return formatter.format(amount);
}

// Format percentage
function formatPercentage(value) {
  if (value === null || value === undefined) return '-';
  
  return `${value > 0 ? '+' : ''}${value}%`;
}

// Format date to YYYY-MM-DD
function formatDate(dateString) {
  if (!dateString) return '-';
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

// Calculate US price with fee (converted to TWD)
function calculateUSPriceWithFee(usdPrice) {
  if (!usdPrice) return 0;
  
  // Calculate USD price with fees
  const usdWithFee = usdPrice * (1 + (cardFee / 100));
  
  // Convert to TWD
  return usdWithFee * exchangeRate;
}

// Calculate price difference statistics
function calculatePriceStats(products) {
  if (!products || products.length === 0) {
    return { avg: 0, avgWithFee: 0, max: 0, min: 0 };
  }
  
  // Basic price difference (without fees)
  const differences = products.map(p => {
    const usdPrice = p.Price_US || 0;
    const twdPrice = p.Price_TW || 0;
    if (usdPrice <= 0 || twdPrice <= 0) return 0;
    const usdTWD = usdPrice * exchangeRate;
    return ((twdPrice - usdTWD) / usdTWD) * 100;
  }).filter(diff => diff !== 0);
  
  // Price difference with fees
  const differencesWithFee = products.map(p => {
    const usdPrice = p.Price_US || 0;
    const twdPrice = p.Price_TW || 0;
    
    if (usdPrice <= 0 || twdPrice <= 0) return 0;
    
    const usdWithFeeTWD = calculateUSPriceWithFee(usdPrice);
    return ((twdPrice - usdWithFeeTWD) / usdWithFeeTWD) * 100;
  }).filter(diff => diff !== 0);
  
  if (differences.length === 0) {
    return { avg: 0, avgWithFee: 0, max: 0, min: 0 };
  }
  
  // Calculate basic average price difference
  const sum = differences.reduce((acc, curr) => acc + curr, 0);
  const avg = sum / differences.length;
  
  // Calculate average price difference with fees
  const sumWithFee = differencesWithFee.reduce((acc, curr) => acc + curr, 0);
  const avgWithFee = sumWithFee / differencesWithFee.length;
  
  const max = Math.max(...differences);
  const min = Math.min(...differences);
  
  return { avg, avgWithFee, max, min };
}

// ==================== Data Processing Functions ====================

// Load product data
async function loadProductData(product) {
  try {
    // Direct load from root directory
    const response = await fetch(`${product}_data.json`);
    if (!response.ok) {
      throw new Error(`Failed to load ${product} data: ${response.status}`);
    }
    const data = await response.json();
    
    // Update default exchange rate if available in metadata
    if (data.metadata && data.metadata.exchangeRates && data.metadata.exchangeRates.TWD) {
      // Only update if we haven't loaded data before
      if (!productData) {
        exchangeRate = data.metadata.exchangeRates.TWD;
        // Update the input field as well
        const exchangeRateInput = document.getElementById('exchange-rate');
        if (exchangeRateInput) {
          exchangeRateInput.value = exchangeRate;
        }
        console.log(`Using exchange rate from data: ${exchangeRate}`);
      }
    }
    
    // Display exchange rate update date if available
    if (data.metadata && data.metadata.lastExchangeRateUpdate) {
      const exchangeRateDate = formatDate(data.metadata.lastExchangeRateUpdate);
      const exchangeRateFormText = document.querySelector('#exchange-rate + .input-group + .form-text');
      if (exchangeRateFormText) {
        exchangeRateFormText.innerHTML = `Current rate from Cathay Bank (updated: ${exchangeRateDate})`;
      }
    }
    
    // Add calculated price difference (with fees)
    data.products.forEach(p => {
      const usdPrice = p.Price_US || 0;
      const twdPrice = p.Price_TW || 0;
      
      if (usdPrice > 0 && twdPrice > 0) {
        // Calculate USD price with fees (converted to TWD)
        const usdWithFeeTWD = calculateUSPriceWithFee(usdPrice);
        
        // Calculate price difference percentage
        p.price_difference_with_fee_percent = ((twdPrice - usdWithFeeTWD) / usdWithFeeTWD) * 100;
        p.price_difference_with_fee_percent = parseFloat(p.price_difference_with_fee_percent.toFixed(1));
        
        // Recommended purchase location
        p.recommended_purchase = (p.price_difference_with_fee_percent > 0) ? 'US' : 'TW';
      } else {
        p.price_difference_with_fee_percent = 0;
        p.recommended_purchase = 'N/A';
      }
    });
    
    return data;
  } catch (error) {
    console.error(error);
    // Simulated data for testing (if unable to load real data)
    const sampleProducts = {
      iphone: [
        {
          PRODUCT_NAME: 'iPhone 16 Pro 256GB Black Titanium',
          Price_US: 1199,
          Price_TW: 41900,
          price_difference_percent: 1.5,
          price_difference_with_fee_percent: 0.2,
          recommended_purchase: 'TW'
        },
        {
          PRODUCT_NAME: 'iPhone 16 128GB Pink',
          Price_US: 999,
          Price_TW: 31900,
          price_difference_percent: 2.1,
          price_difference_with_fee_percent: 0.5,
          recommended_purchase: 'TW'
        }
      ],
      ipad: [
        {
          PRODUCT_NAME: 'iPad Pro 13-inch Wi-Fi 256GB Space Black',
          Price_US: 1299,
          Price_TW: 44900,
          price_difference_percent: 1.2,
          price_difference_with_fee_percent: -0.3,
          recommended_purchase: 'TW'
        },
        {
          PRODUCT_NAME: 'iPad Air Wi-Fi 128GB Blue',
          Price_US: 599,
          Price_TW: 19900,
          price_difference_percent: 1.8,
          price_difference_with_fee_percent: 0.1,
          recommended_purchase: 'TW'
        }
      ],
      mac: [
        {
          PRODUCT_NAME: 'Mac Studio M2 Max',
          Price_US: 1999,
          Price_TW: 67900,
          price_difference_percent: 2.3,
          price_difference_with_fee_percent: 0.8,
          recommended_purchase: 'TW'
        },
        {
          PRODUCT_NAME: 'MacBook Pro 14-inch M3 Pro 512GB',
          Price_US: 2399,
          Price_TW: 79900,
          price_difference_percent: 1.7,
          price_difference_with_fee_percent: 0.2,
          recommended_purchase: 'TW'
        },
        {
          PRODUCT_NAME: 'iMac 24-inch M3 8-core CPU 256GB Silver',
          Price_US: 1299,
          Price_TW: 44900,
          price_difference_percent: 1.2,
          price_difference_with_fee_percent: -0.3,
          recommended_purchase: 'TW'
        },
        {
          PRODUCT_NAME: 'Mac mini M2 256GB',
          Price_US: 599,
          Price_TW: 19900,
          price_difference_percent: 1.8,
          price_difference_with_fee_percent: 0.1,
          recommended_purchase: 'TW'
        }
      ],
      watch: [
        {
          PRODUCT_NAME: 'Apple Watch Series 10 GPS 42mm Aluminum',
          Price_US: 399,
          Price_TW: 12900,
          price_difference_percent: 2.1,
          price_difference_with_fee_percent: 0.5,
          recommended_purchase: 'TW'
        },
        {
          PRODUCT_NAME: 'Apple Watch Ultra 2 GPS + Cellular 49mm Titanium',
          Price_US: 799,
          Price_TW: 26900,
          price_difference_percent: 1.8,
          price_difference_with_fee_percent: 0.2,
          recommended_purchase: 'TW'
        },
        {
          PRODUCT_NAME: 'Apple Watch SE GPS 40mm Aluminum',
          Price_US: 249,
          Price_TW: 8900,
          price_difference_percent: 2.5,
          price_difference_with_fee_percent: 0.9,
          recommended_purchase: 'TW'
        }
      ],
      airpods: [
        {
          PRODUCT_NAME: 'AirPods (4th generation)',
          Price_US: 129,
          Price_TW: 4290,
          price_difference_percent: 1.5,
          price_difference_with_fee_percent: -0.1,
          recommended_purchase: 'TW'
        },
        {
          PRODUCT_NAME: 'AirPods Pro (2nd generation) with USB-C',
          Price_US: 249,
          Price_TW: 7990,
          price_difference_percent: 1.8,
          price_difference_with_fee_percent: 0.2,
          recommended_purchase: 'TW'
        },
        {
          PRODUCT_NAME: 'AirPods Max',
          Price_US: 549,
          Price_TW: 18900,
          price_difference_percent: 2.2,
          price_difference_with_fee_percent: 0.6,
          recommended_purchase: 'TW'
        }
      ],
      tvhome: [
        {
          PRODUCT_NAME: 'Apple TV 4K Wi-Fi 64GB (3rd generation)',
          Price_US: 129,
          Price_TW: 4590,
          price_difference_percent: 2.8,
          price_difference_with_fee_percent: 1.2,
          recommended_purchase: 'TW'
        },
        {
          PRODUCT_NAME: 'Apple TV 4K Wi-Fi + Ethernet 128GB (3rd generation)',
          Price_US: 149,
          Price_TW: 5290,
          price_difference_percent: 2.5,
          price_difference_with_fee_percent: 0.9,
          recommended_purchase: 'TW'
        },
        {
          PRODUCT_NAME: 'HomePod (2nd generation)',
          Price_US: 299,
          Price_TW: 9900,
          price_difference_percent: 1.5,
          price_difference_with_fee_percent: -0.1,
          recommended_purchase: 'TW'
        },
        {
          PRODUCT_NAME: 'HomePod mini',
          Price_US: 99,
          Price_TW: 3290,
          price_difference_percent: 1.2,
          price_difference_with_fee_percent: -0.4,
          recommended_purchase: 'TW'
        }
      ]
    };

    return {
      metadata: {
        lastUpdated: new Date().toISOString(),
        regions: ['US', 'TW'],
        productType: product,
        totalProducts: sampleProducts[product]?.length || 2,
        exchangeRates: {
          TWD: 31.5
        }
      },
      products: sampleProducts[product] || [
        {
          PRODUCT_NAME: `${product.toUpperCase()} Sample Product`,
          Price_US: 999,
          Price_TW: 31000,
          price_difference_percent: 1.5,
          price_difference_with_fee_percent: 0.2,
          recommended_purchase: 'TW'
        }
      ]
    };
  }
}

// Render product table
function renderProductTable(products) {
  const tableBody = document.querySelector('#products-table tbody');
  tableBody.innerHTML = '';
  
  if (!products || products.length === 0) {
    tableBody.innerHTML = `
      <tr>
        <td colspan="6" class="text-center py-3">No product data found</td>
      </tr>
    `;
    return;
  }
  
  products.forEach(product => {
    const row = document.createElement('tr');
    
    const usdPrice = product.Price_US || 0;
    const twdPrice = product.Price_TW || 0;
    const usdWithFeeTWD = calculateUSPriceWithFee(usdPrice);
    
    // Real-time calculation of price difference percentage with fees
    const differenceWithFee = twdPrice > 0 && usdWithFeeTWD > 0 
      ? ((twdPrice - usdWithFeeTWD) / usdWithFeeTWD) * 100
      : 0;
    
    // Price difference style
    const diffClass = differenceWithFee > 0 ? 'price-higher' : differenceWithFee < 0 ? 'price-lower' : '';
    
    // Purchase recommendation
    let recommendation = '';
    if (usdPrice <= 0 || twdPrice <= 0) {
      recommendation = '<span class="badge bg-secondary">No Data</span>';
    } else if (differenceWithFee > 2) {
      recommendation = '<span class="badge bg-danger">Buy in US</span>';
    } else if (differenceWithFee < -2) {
      recommendation = '<span class="badge bg-success">Buy in Taiwan</span>';
    } else {
      recommendation = '<span class="badge bg-info">Similar</span>';
    }
    
    row.innerHTML = `
      <td>${product.PRODUCT_NAME}</td>
      <td>${formatCurrency(usdPrice, 'USD')}</td>
      <td>${formatCurrency(usdWithFeeTWD, 'TWD')}</td>
      <td>${formatCurrency(twdPrice, 'TWD')}</td>
      <td class="${diffClass}">${formatPercentage(differenceWithFee.toFixed(1))}</td>
      <td>${recommendation}</td>
    `;
    
    tableBody.appendChild(row);
  });
}

// Update summary statistics
function updateSummaryStats(data) {
  if (!data || !data.products) return;
  
  const totalProducts = document.getElementById('total-products');
  const avgDiff = document.getElementById('avg-diff');
  const avgDiffWithFee = document.getElementById('avg-diff-with-fee');
  const lastUpdated = document.getElementById('last-updated');
  
  totalProducts.textContent = data.products.length;
  
  const stats = calculatePriceStats(data.products);
  
  // Update regular price difference
  avgDiff.textContent = formatPercentage(stats.avg.toFixed(1));
  avgDiff.className = stats.avg > 0 ? 'card-text display-4 price-higher' : 'card-text display-4 price-lower';
  
  // Update price difference with fees
  avgDiffWithFee.textContent = formatPercentage(stats.avgWithFee.toFixed(1));
  avgDiffWithFee.className = stats.avgWithFee > 0 ? 'card-text display-4 price-higher' : 'card-text display-4 price-lower';
  
  lastUpdated.textContent = formatDate(data.metadata.lastUpdated);
}

// ==================== Initialization and Settings Functions ====================

// Initialize exchange rate and card fee settings
function initSettings() {
  const exchangeRateInput = document.getElementById('exchange-rate');
  const cardFeeInput = document.getElementById('card-fee');
  const settingsChangedBadge = document.getElementById('settings-changed');
  
  // Load saved settings
  const savedSettings = localStorage.getItem('price-settings');
  if (savedSettings) {
    const settings = JSON.parse(savedSettings);
    exchangeRate = settings.exchangeRate || 31.5;
    cardFee = settings.cardFee || 1.5;
    
    exchangeRateInput.value = exchangeRate;
    cardFeeInput.value = cardFee;
  }
  
  // Set change listeners
  exchangeRateInput.addEventListener('change', updateSettings);
  cardFeeInput.addEventListener('change', updateSettings);
  
  // Update UI when settings change
  function updateSettings() {
    const newExchangeRate = parseFloat(exchangeRateInput.value);
    const newCardFee = parseFloat(cardFeeInput.value);
    
    if (!isNaN(newExchangeRate) && !isNaN(newCardFee) && 
        newExchangeRate > 0 && newCardFee >= 0) {
      
      // Check if there are changes
      const hasChanged = (exchangeRate !== newExchangeRate || cardFee !== newCardFee);
      
      // Update global variables
      exchangeRate = newExchangeRate;
      cardFee = newCardFee;
      
      // Save settings
      localStorage.setItem('price-settings', JSON.stringify({
        exchangeRate,
        cardFee
      }));
      
      // Show changed marker
      if (hasChanged) {
        settingsChangedBadge.style.display = 'inline-block';
        setTimeout(() => {
          settingsChangedBadge.style.display = 'none';
        }, 3000);
        
        // Re-render data
        if (productData) {
          renderProductTable(productData.products);
          updateSummaryStats(productData);
        }
      }
    }
  }
}

// Set up search functionality
function setupSearch() {
  const searchInput = document.getElementById('product-search');
  if (!searchInput) return;
  
  searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    
    // Exit if no data
    if (!productData || !productData.products) return;
    
    // Filter products
    const filteredProducts = productData.products.filter(product => {
      return product.PRODUCT_NAME.toLowerCase().includes(searchTerm);
    });
    
    // Re-render table
    renderProductTable(filteredProducts);
  });
}

// Set up event listeners
function setupEventListeners() {
  // Product switching
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', async (e) => {
      e.preventDefault();
      
      // Update navigation state
      document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
      e.target.classList.add('active');
      
      // Switch product type
      currentProduct = e.target.dataset.product;
      
      // Update page title
      document.getElementById('page-title').textContent = `Apple ${currentProduct.toUpperCase()} Price Comparison`;
      
      // Reload data
      productData = await loadProductData(currentProduct);
      
      // Update statistics summary
      updateSummaryStats(productData);
      
      // Update UI
      renderProductTable(productData.products);
      
      // Clear search box
      const searchInput = document.getElementById('product-search');
      if (searchInput) searchInput.value = '';
    });
  });
}

// Detect iOS Safari and show "Add to Home Screen" prompt
function detectIOSSafari() {
  const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
  const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
  
  // Only show on iOS Safari
  if (isIOS && isSafari) {
    // Check if already in "Add to Home Screen" mode
    const isStandalone = window.navigator.standalone === true;
    
    if (!isStandalone) {
      // Check if prompt has already been shown
      const hasShownPrompt = localStorage.getItem('ios-add-prompt-shown');
      
      if (!hasShownPrompt) {
        // Show prompt
        const prompt = document.getElementById('ios-add-to-home');
        if (prompt) {
          prompt.classList.remove('d-none');
          
          // Record that prompt has been shown (won't show again for 24 hours)
          localStorage.setItem('ios-add-prompt-shown', Date.now());
          
          // Set to expire after 24 hours
          setTimeout(() => {
            localStorage.removeItem('ios-add-prompt-shown');
          }, 24 * 60 * 60 * 1000);
        }
      }
    }
  }
}

// ==================== Main Initialization ====================

// Initialize page
async function init() {
  // Initialize theme
  initTheme();
  
  // Initialize settings
  initSettings();
  
  // Update page title
  document.getElementById('page-title').textContent = `Apple ${currentProduct.toUpperCase()} Price Comparison`;
  
  // Load data
  productData = await loadProductData(currentProduct);
  
  // Update statistics summary
  updateSummaryStats(productData);
  
  // Render table
  renderProductTable(productData.products);
  
  // Set up search functionality
  setupSearch();
  
  // Set up event listeners
  setupEventListeners();
  
  // Detect iOS Safari and show prompt
  detectIOSSafari();
}

// Launch application
window.addEventListener('DOMContentLoaded', init);