#!/usr/bin/env python3
"""
Debug script to check schema extraction issues
"""

import os
import sys
import json
sys.path.append('backend')

from main import find_data_files_by_category, extract_column_data

def debug_schema_extraction():
    """Debug the schema extraction process"""
    
    print("Debugging schema extraction...")
    
    # Load matched schemas
    with open('schema_analysis/matched_schemas.json', 'r') as f:
        matched_data = json.load(f)
    
    matched_schemas = matched_data['matched_schemas']
    
    print(f"Total matched schemas: {len(matched_schemas)}")
    
    # Test a few specific schemas
    test_schemas = [
        ("Loan Accounts", 1, "customerId"),
        ("CurSav Accounts", 1, "customerId"),
        ("Loan Accounts", 2, "accountHolderKey"),
    ]
    
    for category, bank_num, expected_id_col in test_schemas:
        print(f"\n{'='*60}")
        print(f"Testing: {category} (Bank {bank_num})")
        
        # Find schemas for this category
        schemas_for_category = []
        for schema in matched_schemas:
            if bank_num == 1 and schema['bank1']['category'] == category:
                schemas_for_category.append(schema['bank1'])
            elif bank_num == 2 and schema['bank2']['category'] == category:
                schemas_for_category.append(schema['bank2'])
        
        print(f"Found {len(schemas_for_category)} schemas for this category:")
        for schema in schemas_for_category[:5]:  # Show first 5
            print(f"  - {schema['schema']}")
        
        # Find files for this category
        files = find_data_files_by_category(category, bank_num)
        print(f"Found {len(files)} files for this category")
        
        if files and schemas_for_category:
            file_path = files[0]
            filename = os.path.basename(file_path)
            print(f"\nTesting extraction from: {filename}")
            
            # Test extracting a few schemas
            for schema in schemas_for_category[:3]:  # Test first 3 schemas
                schema_name = schema['schema']
                print(f"\n  Testing schema: {schema_name}")
                
                try:
                    data_map = extract_column_data(file_path, schema_name, expected_id_col)
                    print(f"    ✅ Successfully extracted {len(data_map)} records")
                    
                    if len(data_map) > 0:
                        # Show a sample
                        sample_key = list(data_map.keys())[0]
                        sample_value = data_map[sample_key]
                        print(f"    Sample: {sample_key} -> {sample_value}")
                    else:
                        print(f"    ⚠️  No data extracted")
                        
                except Exception as e:
                    print(f"    ❌ Error: {e}")

if __name__ == "__main__":
    debug_schema_extraction()
