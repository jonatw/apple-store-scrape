// CSS and Bootstrap (Vite extracts CSS to separate file in production)
import './scss/custom-bootstrap.scss';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import './icons.js';

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
    const response = await fetch(`data/${product}_data.json`);
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
    console.error('Failed to load product data:', error);
    return {
      metadata: {
        lastUpdated: null,
        regions: ['US', 'TW'],
        productType: product,
        totalProducts: 0,
        exchangeRates: { TWD: exchangeRate }
      },
      products: []
    };
  }
}

// Render product table
function renderProductTable(products) {
  const tableBody = document.querySelector('#products-table tbody');
  const tableHead = document.querySelector('#products-table thead tr');
  
  tableBody.innerHTML = '';
  
  tableHead.innerHTML = `
    <th scope="col">Product</th>
    <th scope="col">US (USD)</th>
    <th scope="col" class="d-none d-md-table-cell">US+Fee (TWD)</th>
    <th scope="col">TW (TWD)</th>
    <th scope="col">Diff</th>
    <th scope="col" class="d-none d-md-table-cell">Rec.</th>
  `;
  
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
    
    // Build product name cell safely (no innerHTML for user data)
    const nameCell = document.createElement('td');
    nameCell.textContent = product.PRODUCT_NAME;

    if (currentProduct === 'mac') {
        const specs = [];
        if (product.Chip) specs.push(product.Chip);
        if (product.Memory) specs.push(product.Memory);
        if (product.Storage) specs.push(product.Storage);
        if (product.CPU_Cores && product.GPU_Cores) {
            specs.push(`${product.CPU_Cores}C CPU / ${product.GPU_Cores}C GPU`);
        }
        if (specs.length > 0) {
            const specEl = document.createElement('small');
            specEl.className = 'text-muted d-block';
            specEl.textContent = specs.join(' \u2022 ');
            nameCell.appendChild(specEl);
        }
    }

    // Build recommendation badge
    let recBadge = 'No Data';
    let recClass = 'bg-secondary';
    if (usdPrice > 0 && twdPrice > 0) {
      if (differenceWithFee > 2) { recBadge = 'Buy in US'; recClass = 'bg-danger'; }
      else if (differenceWithFee < -2) { recBadge = 'Buy in Taiwan'; recClass = 'bg-success'; }
      else { recBadge = 'Similar'; recClass = 'bg-info'; }
    }

    // Build cells using DOM API (safe against XSS)
    const usPriceCell = document.createElement('td');
    usPriceCell.textContent = formatCurrency(usdPrice, 'USD');

    const usFeeCell = document.createElement('td');
    usFeeCell.className = 'd-none d-md-table-cell';
    usFeeCell.textContent = formatCurrency(usdWithFeeTWD, 'TWD');

    const twPriceCell = document.createElement('td');
    twPriceCell.textContent = formatCurrency(twdPrice, 'TWD');

    const diffCell = document.createElement('td');
    diffCell.className = diffClass;
    diffCell.textContent = formatPercentage(differenceWithFee.toFixed(1));

    const recCell = document.createElement('td');
    recCell.className = 'd-none d-md-table-cell';
    const badge = document.createElement('span');
    badge.className = `badge ${recClass}`;
    badge.textContent = recBadge;
    recCell.appendChild(badge);

    row.appendChild(nameCell);
    row.appendChild(usPriceCell);
    row.appendChild(usFeeCell);
    row.appendChild(twPriceCell);
    row.appendChild(diffCell);
    row.appendChild(recCell);
    
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

// Navigate to a product category
async function navigateTo(product) {
  currentProduct = product;

  // Update nav active state
  document.querySelectorAll('.nav-link').forEach(l => {
    l.classList.toggle('active', l.dataset.product === product);
  });

  // Update page title
  document.getElementById('page-title').textContent = `Apple ${product.toUpperCase()} Price Comparison`;

  // Load and render
  productData = await loadProductData(product);
  updateSummaryStats(productData);
  renderProductTable(productData.products);

  // Clear search
  const searchInput = document.getElementById('product-search');
  if (searchInput) searchInput.value = '';
}

// Set up event listeners
function setupEventListeners() {
  // Nav clicks update hash — hashchange handler does the actual navigation
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      window.location.hash = e.target.dataset.product;
    });
  });

  // Hash change drives navigation (supports back/forward in PWA standalone)
  window.addEventListener('hashchange', () => {
    const product = window.location.hash.slice(1) || 'iphone';
    if (product !== currentProduct) {
      navigateTo(product);
    }
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
  initTheme();
  initSettings();

  // Read product from URL hash (e.g. #ipad), default to iphone
  const validProducts = ['iphone', 'ipad', 'mac', 'watch', 'airpods', 'tvhome'];
  const hashProduct = window.location.hash.slice(1);
  if (hashProduct && validProducts.includes(hashProduct)) {
    currentProduct = hashProduct;
  }

  // Set up event listeners (before navigateTo so hashchange works)
  setupSearch();
  setupEventListeners();

  // Load and render initial product
  await navigateTo(currentProduct);

  // Register service worker for offline PWA support
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('./sw.js').catch(() => {});
  }

  detectIOSSafari();
}

// Launch application
window.addEventListener('DOMContentLoaded', init);