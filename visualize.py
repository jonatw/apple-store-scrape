import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('iphone_products_merged.csv')

# Filter out rows with 0 price
df = df[(df['Price_US'] > 0) & (df['Price_TW'] > 0)]

# Convert TW price to USD (Approx rate 32.0 for visualization)
EXCHANGE_RATE = 32.0
df['Price_TW_USD'] = df['Price_TW'] / EXCHANGE_RATE

# Calculate difference
df['Diff_USD'] = df['Price_TW_USD'] - df['Price_US']

# Sort by difference
df = df.sort_values('Diff_USD', ascending=False).head(10)  # Top 10 diffs

# Plot
plt.figure(figsize=(12, 8))
sns.set_style("whitegrid")

# Create bar plot
ax = sns.barplot(x='Diff_USD', y='PRODUCT_NAME', data=df, palette='viridis')

# Add labels
plt.title('Top 10 Apple Products: TW vs US Price Difference (in USD)', fontsize=16)
plt.xlabel('Price Difference (USD) - Positive means TW is more expensive', fontsize=12)
plt.ylabel('Product', fontsize=12)

# Add value labels
for i, v in enumerate(df['Diff_USD']):
    ax.text(v + 5, i, f"+${v:.0f}", color='black', va='center')

plt.tight_layout()
plt.savefig('price_diff.png')
print("Chart generated: price_diff.png")
