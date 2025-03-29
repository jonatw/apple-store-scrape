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
    // Or use system preference
    const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = prefersDarkMode ? 'dark' : 'light';
    document.documentElement.setAttribute('data-bs-theme', theme);
    updateThemeIcon(theme);
  }
  
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

// Format date
function formatDate(dateString) {
  if (!dateString) return '-';
  
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-TW', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
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
  const differences = products
    .map(p => p.price_difference_percent || 0)
    .filter(diff => diff !== 0);
  
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
    // 直接從根目錄載入
    const response = await fetch(`${product}_data.json`);
    if (!response.ok) {
      throw new Error(`Failed to load ${product} data: ${response.status}`);
    }
    const data = await response.json();
    
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
    return {
      metadata: {
        lastUpdated: new Date().toISOString(),
        regions: ['US', 'TW'],
        productType: product,
        totalProducts: 5,
        exchangeRates: {
          TWD: 31.5
        }
      },
      products: [
        {
          PRODUCT_NAME: `${product.toUpperCase()} Sample 1`,
          Price_US: 999,
          Price_TW: 31000,
          price_difference_percent: 1.5,
          price_difference_with_fee_percent: 0.2,
          recommended_purchase: 'TW'
        },
        {
          PRODUCT_NAME: `${product.toUpperCase()} Sample 2`,
          Price_US: 1199,
          Price_TW: 37500,
          price_difference_percent: 2.1,
          price_difference_with_fee_percent: 0.5,
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