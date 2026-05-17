import pandas as pd
import sqlite3
import io
import os

# =================================================================
# 1. EMBEDDED SETTINGS DATA
# This data is fixed and no longer requires a separate CSV file.
# =================================================================
SETTINGS_CSV_CONTENT = """Myanmar Gold Weight Conversion (as provided),,
Key,Value,Note
GRAM_PER_KYAT,16.606,1 ကျပ်သား = 16.606 g
GRAM_PER_PE,1.038,1 ပဲ = 1.038 g
GRAM_PER_YWE,0.129,1 ရွေး = 0.129 g
YWE_PER_KYAT,128,1 ကျပ်သား = 16 ပဲ = 128 ရွေး
YWE_PER_PE,8,1 ပဲ = 8 ရွေး
Tip: Keep these constants if you want consistent gram calculations across all sheets.,,
"""

# =================================================================
# 2. CONFIGURATION
# =================================================================
ITEMS_CSV = 'Final Gold_stock_Full_with_Modules - Items.csv'
DB_NAME = 'gold_stock.db'

def convert_to_sqlite():
    # Verify if the Items file exists
    if not os.path.exists(ITEMS_CSV):
        print(f"Error: The file '{ITEMS_CSV}' was not found in this folder.")
        return

    try:
        print(f"Starting conversion to {DB_NAME}...")

        # --- 1. Load Settings (from embedded string) ---
        # Note: We skip the first row because it contains a title, not headers.
        settings_df = pd.read_csv(io.StringIO(SETTINGS_CSV_CONTENT), skiprows=1)
        
        # --- 2. Load Items (from local CSV file) ---
        items_df = pd.read_csv(ITEMS_CSV)

        # Filter: Skip rows where item_code, category, or item_name are null (original logic)
        items_df = items_df.dropna(subset=['item_code', 'category', 'item_name'])

        # --- 3. Database Operations ---
        conn = sqlite3.connect(DB_NAME)
        
        # Write 'settings' table
        settings_df.to_sql('settings', conn, if_exists='replace', index=False)
        
        # Write 'items' table
        items_df.to_sql('items', conn, if_exists='replace', index=False)
        
        conn.close()
        
        print(f"Successfully converted data to {DB_NAME}")
        print(f"Table 'settings' updated with {len(settings_df)} rows.")
        print(f"Table 'items' updated with {len(items_df)} rows.")
        
    except Exception as e:
        print(f"An error occurred during conversion: {e}")

if __name__ == "__main__":
    convert_to_sqlite()
