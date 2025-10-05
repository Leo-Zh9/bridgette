#!/usr/bin/env python3
"""
Debug script to check data extraction issues
"""

import os
import sys
import pandas as pd
sys.path.append('backend')

from main import find_data_files_by_category, extract_column_data

def debug_data_extraction():
    """Debug the data extraction process"""
    
    print("Debugging data extraction...")
    
    # Test a few specific cases
    test_cases = [
        ("Loan Accounts", 1, "customerId"),
        ("CurSav Accounts", 1, "customerId"),
        ("Loan Accounts", 2, "accountHolderKey"),
    ]
    
    for category, bank_num, expected_id_col in test_cases:
        print(f"\n{'='*60}")
        print(f"Testing: {category} (Bank {bank_num})")
        print(f"Expected ID column: {expected_id_col}")
        
        # Find files
        files = find_data_files_by_category(category, bank_num)
        print(f"Found {len(files)} files:")
        
        for file_path in files:
            filename = os.path.basename(file_path)
            print(f"\n  File: {filename}")
            
            # Check what columns are available
            try:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)
                
                print(f"    Columns: {list(df.columns)}")
                print(f"    Shape: {df.shape}")
                
                # Check if expected ID column exists
                if expected_id_col in df.columns:
                    print(f"    ✅ Expected ID column '{expected_id_col}' found")
                else:
                    print(f"    ❌ Expected ID column '{expected_id_col}' NOT found")
                
                # Show first few rows
                print(f"    First 3 rows:")
                for i, row in df.head(3).iterrows():
                    print(f"      Row {i}: {dict(row)}")
                    
            except Exception as e:
                print(f"    ❌ Error reading file: {e}")

if __name__ == "__main__":
    debug_data_extraction()
