#import pandas as pd

#sales = pd.read_excel('bm_sales.xlsx')
#print("COLUMNS IN YOUR SALES FILE:")
#for i, col in enumerate(sales.columns):
#    print(f"  {i+1}. '{col}'")

#print("\nFIRST 2 ROWS:")
#print(sales.head(2))
"""
-----------------------------------------------------
DATA PREPARATION PHASE 
-----------------------------------------------------
 columns: date, store_id, sku_id, customer_id, quantity, unit_price, 
              total_value, channel, discount_pct
"""

import pandas as pd
import numpy as np

print("=" * 60)
print("DATA PREPARATION PHASE - STARTING")
print("=" * 60)

# -----------------------------------------------------
# 1. LOAD ALL FILES
#-----------------------------------------------------

print("\n[STEP 1] Loading files...")

sales = pd.read_excel('bm_sales.xlsx')
stores = pd.read_excel('bm_stores.xlsx')
products = pd.read_excel('bm_skus.xlsx')
customers = pd.read_excel('bm_customers.xlsx')
inventory = pd.read_excel('bm_inventory.xlsx')
promotions = pd.read_excel('bm_promotions.xlsx')

print(f"✓ Sales: {sales.shape[0]:,} rows, {sales.shape[1]} columns")
print(f"✓ Stores: {stores.shape[0]} rows, {stores.shape[1]} columns")
print(f"✓ Products: {products.shape[0]:,} rows, {products.shape[1]} columns")
print(f"✓ Customers: {customers.shape[0]:,} rows, {customers.shape[1]} columns")
print(f"✓ Inventory: {inventory.shape[0]:,} rows, {inventory.shape[1]} columns")
print(f"✓ Promotions: {promotions.shape[0]} rows, {promotions.shape[1]} columns")

# Show column names for verification
print("\n[INFO] Sales columns:", list(sales.columns))

#-----------------------------------------------------
# 2. CLEAN SALES TRANSACTIONS
#-----------------------------------------------------

print("\n[STEP 2] Cleaning SALES data...")

# 2.1 Check for missing values
print("   Missing values in sales:")
print(f"     date: {sales['date'].isna().sum()}")
print(f"     store_id: {sales['store_id'].isna().sum()}")
print(f"     sku_id: {sales['sku_id'].isna().sum()}")
print(f"     customer_id: {sales['customer_id'].isna().sum()}")
print(f"     quantity: {sales['quantity'].isna().sum()}")
print(f"     unit_price: {sales['unit_price'].isna().sum()}")

# 2.2 Handle missing customer_id (fill with -1 for unknown/guest)
sales['customer_id'] = sales['customer_id'].fillna(-1).astype(int)
print("   ✓ Filled missing customer_id with -1 (guest checkout)")

# 2.3 Handle missing discount_pct (fill with 0)
if 'discount_pct' in sales.columns:
    sales['discount_pct'] = sales['discount_pct'].fillna(0)
    print("   ✓ Filled missing discount_pct with 0")

# 2.4 Remove rows with missing critical values
initial_rows = len(sales)
sales = sales.dropna(subset=['date', 'store_id', 'sku_id', 'quantity', 'unit_price', 'total_value'])
print(f"   Removed {initial_rows - len(sales):,} rows with missing critical values")

# 2.5 Remove invalid values (negative or zero)
initial_rows = len(sales)
sales = sales[sales['quantity'] > 0]
sales = sales[sales['unit_price'] > 0]
sales = sales[sales['total_value'] > 0]
print(f"   Removed {initial_rows - len(sales):,} rows with invalid values (<=0)")

# 2.6 Remove outliers (prices above 99.9th percentile)
q999 = sales['unit_price'].quantile(0.999)
before_outliers = len(sales)
sales = sales[sales['unit_price'] <= q999]
print(f"   Removed {before_outliers - len(sales)} price outliers (>99.9th percentile)")

# 2.7 Convert date and add time features
sales['date'] = pd.to_datetime(sales['date'], errors='coerce')
sales = sales.dropna(subset=['date'])

# Add time-based features for analysis
sales['order_year'] = sales['date'].dt.year
sales['order_month'] = sales['date'].dt.month
sales['order_day'] = sales['date'].dt.day
sales['order_day_of_week'] = sales['date'].dt.dayofweek  # Monday=0, Sunday=6
sales['order_weekend'] = sales['order_day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
sales['order_quarter'] = sales['date'].dt.quarter

print(f"   ✓ Added time features: year, month, day, day_of_week, weekend, quarter")

print(f"\n   ✓ FINAL Sales cleaned: {len(sales):,} rows")

# -----------------------------------------------------
# 3. CLEAN STORES
# -----------------------------------------------------

print("\n[STEP 3] Cleaning STORES data...")

print(f"   Before: {stores.shape[0]} rows")
stores = stores.drop_duplicates()
print(f"   After dedup: {stores.shape[0]} rows")

# Standardize text columns
if 'store_name' in stores.columns:
    stores['store_name'] = stores['store_name'].fillna('Unknown').astype(str).str.strip().str.title()
if 'city' in stores.columns:
    stores['city'] = stores['city'].fillna('Unknown').astype(str).str.strip().str.title()
if 'store_type' in stores.columns:
    stores['store_type'] = stores['store_type'].fillna('Unknown').astype(str).str.strip().str.upper()

print(f"   ✓ Stores cleaned: {stores.shape[0]} rows")
print(f"     Unique cities: {stores['city'].nunique() if 'city' in stores.columns else 'N/A'}")

#-----------------------------------------------------
# 4. CLEAN PRODUCTS
#-----------------------------------------------------

print("\n[STEP 4] Cleaning PRODUCTS data...")

print(f"   Before: {products.shape[0]:,} rows")
products = products.drop_duplicates()
print(f"   After dedup: {products.shape[0]:,} rows")

# Handle missing values and standardize
if 'sku_name' in products.columns:
    products['sku_name'] = products['sku_name'].fillna('Unknown').astype(str).str.strip().str.title()
if 'category' in products.columns:
    products['category'] = products['category'].fillna('Unknown').astype(str).str.strip().str.lower()
if 'subcategory' in products.columns:
    products['subcategory'] = products['subcategory'].fillna('Unknown').astype(str).str.strip().str.lower()
if 'brand' in products.columns:
    products['brand'] = products['brand'].fillna('Unknown').astype(str).str.strip().str.title()

# Ensure prices are positive
if 'unit_price' in products.columns:
    products = products[products['unit_price'] > 0]
if 'cost_price' in products.columns:
    products = products[products['cost_price'] > 0]

print(f"   ✓ Products cleaned: {products.shape[0]:,} rows")
if 'category' in products.columns:
    print(f"     Unique categories: {products['category'].nunique()}")
    print(f"     Categories: {products['category'].unique().tolist()}")

# -----------------------------------------------------
# 5. CLEAN CUSTOMERS
# -----------------------------------------------------

print("\n[STEP 5] Cleaning CUSTOMERS data...")

print(f"   Before: {customers.shape[0]:,} rows")
customers = customers.drop_duplicates()
print(f"   After dedup: {customers.shape[0]:,} rows")

# Standardize text columns
if 'gender' in customers.columns:
    customers['gender'] = customers['gender'].fillna('Unknown').astype(str).str.strip().str.upper()
if 'loyalty_segment' in customers.columns:
    customers['loyalty_segment'] = customers['loyalty_segment'].fillna('Unknown').astype(str).str.strip().str.title()
if 'city' in customers.columns:
    customers['city'] = customers['city'].fillna('Unknown').astype(str).str.strip().str.title()
if 'preferred_channel' in customers.columns:
    customers['preferred_channel'] = customers['preferred_channel'].fillna('Unknown').astype(str).str.strip().str.title()

# Handle age outliers (if age column exists)
if 'age' in customers.columns:
    customers['age'] = customers['age'].fillna(customers['age'].median())
    customers = customers[(customers['age'] >= 18) & (customers['age'] <= 100)]
    print(f"   Filtered age to 18-100 range")

print(f"   ✓ Customers cleaned: {customers.shape[0]:,} rows")

# -----------------------------------------------------
# 6. CLEAN INVENTORY
# -----------------------------------------------------

print("\n[STEP 6] Cleaning INVENTORY data...")

print(f"   Before: {inventory.shape[0]:,} rows")
inventory = inventory.drop_duplicates()
print(f"   After dedup: {inventory.shape[0]:,} rows")

# Handle missing or negative inventory values
if 'stock_on_hand' in inventory.columns:
    inventory['stock_on_hand'] = inventory['stock_on_hand'].fillna(0).clip(lower=0)
if 'reorder_point' in inventory.columns:
    inventory['reorder_point'] = inventory['reorder_point'].fillna(0)
if 'safety_stock' in inventory.columns:
    inventory['safety_stock'] = inventory['safety_stock'].fillna(0)

print(f"   ✓ Inventory cleaned: {inventory.shape[0]:,} rows")

# -----------------------------------------------------
# 7. CLEAN PROMOTIONS
#-----------------------------------------------------

print("\n[STEP 7] Cleaning PROMOTIONS data...")

print(f"   Before: {promotions.shape[0]} rows")
promotions = promotions.drop_duplicates()
print(f"   After dedup: {promotions.shape[0]} rows")

# Standardize text columns
if 'promo_name' in promotions.columns:
    promotions['promo_name'] = promotions['promo_name'].fillna('Unknown').astype(str).str.strip().str.title()
if 'promo_type' in promotions.columns:
    promotions['promo_type'] = promotions['promo_type'].fillna('Unknown').astype(str).str.strip().str.title()

# Ensure discount percentage is between 0 and 100
if 'discount_pct' in promotions.columns:
    promotions['discount_pct'] = promotions['discount_pct'].fillna(0)
    promotions['discount_pct'] = promotions['discount_pct'].clip(0, 100)

print(f"   ✓ Promotions cleaned: {promotions.shape[0]} rows")

# -----------------------------------------------------
# 8. SAVE ALL CLEANED FILES
# -----------------------------------------------------

print("\n[STEP 8] Saving cleaned files...")

sales.to_csv('sales_cleaned.csv', index=False)
stores.to_csv('stores_cleaned.csv', index=False)
products.to_csv('products_cleaned.csv', index=False)
customers.to_csv('customers_cleaned.csv', index=False)
inventory.to_csv('inventory_cleaned.csv', index=False)
promotions.to_csv('promotions_cleaned.csv', index=False)

print("✓ All files saved as CSV")
print("   - sales_cleaned.csv")
print("   - stores_cleaned.csv")
print("   - products_cleaned.csv")
print("   - customers_cleaned.csv")
print("   - inventory_cleaned.csv")
print("   - promotions_cleaned.csv")

# -----------------------------------------------------
# 9. VERIFICATION REPORT
# -----------------------------------------------------

print("\n" + "=" * 60)
print("CLEANING VERIFICATION REPORT")
print("=" * 60)

print("\n--- Sales Data Summary ---")
print(f"  Total transactions: {len(sales):,}")
print(f"  Date range: {sales['date'].min().date()} to {sales['date'].max().date()}")
print(f"  Unique stores: {sales['store_id'].nunique()}")
print(f"  Unique products: {sales['sku_id'].nunique()}")
print(f"  Unique customers: {sales['customer_id'].nunique() - 1:,} (excluding guest)")
print(f"  Channels: {sales['channel'].unique().tolist() if 'channel' in sales.columns else 'N/A'}")
print(f"  Total revenue: ${sales['total_value'].sum():,.2f}")

print("\n--- Data Quality Checks ---")
print(f"  Missing values in sales: {sales.isnull().sum().sum()}")
print(f"  Negative values: {((sales[['quantity', 'unit_price', 'total_value']] < 0).sum().sum())}")

print("\n--- Data Ready for SQL ---")
print("✓ No missing values in critical columns")
print("✓ All dates converted to datetime")
print("✓ Time features added (year, month, day_of_week, quarter, weekend)")
print("✓ Invalid rows removed")
print("✓ Duplicates removed")

print("\n" + "=" * 60)
print("DATA PREPARATION PHASE COMPLETE!")
print("=" * 60)
