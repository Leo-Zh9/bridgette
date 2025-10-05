"""
Test script to demonstrate main.py integration with Flask app
"""

import requests
import json

# Configuration
BACKEND_URL = "http://localhost:5001"

def test_analyze_schemas():
    """Test the analyze_schemas functionality"""
    print("🔍 Testing Schema Analysis...")
    
    response = requests.post(f"{BACKEND_URL}/api/process-with-main", 
                           json={"action": "analyze_schemas"})
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Schema analysis successful!")
        print(f"   Bank 1 file: {data.get('bank1_file', 'N/A')}")
        print(f"   Bank 2 file: {data.get('bank2_file', 'N/A')}")
        print(f"   Bank 1 schemas: {data.get('bank1_schema_count', 0)}")
        print(f"   Bank 2 schemas: {data.get('bank2_schema_count', 0)}")
        print(f"   Total schemas: {data.get('total_schemas', 0)}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

def test_compare_schemas():
    """Test the compare_schemas functionality"""
    print("\n🔄 Testing Schema Comparison...")
    
    response = requests.post(f"{BACKEND_URL}/api/process-with-main", 
                           json={"action": "compare_schemas"})
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Schema comparison ready!")
        print(f"   Message: {data.get('message', 'N/A')}")
        print(f"   File 1: {data.get('file1', 'N/A')}")
        print(f"   File 2: {data.get('file2', 'N/A')}")
        print(f"   Note: {data.get('note', 'N/A')}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

def test_list_json_files():
    """Test listing JSON files in storage"""
    print("\n📁 Testing JSON Files List...")
    
    response = requests.get(f"{BACKEND_URL}/api/json-files")
    
    if response.status_code == 200:
        data = response.json()
        files = data.get('files', [])
        print(f"✅ Found {len(files)} JSON files in storage:")
        
        schema_files = [f for f in files if 'schema' in f['filename'].lower()]
        data_files = [f for f in files if 'schema' not in f['filename'].lower()]
        
        print(f"   📊 Schema files: {len(schema_files)}")
        print(f"   📈 Data files: {len(data_files)}")
        
        for file_info in files[:5]:  # Show first 5 files
            print(f"     - {file_info['filename']} ({file_info['size']} bytes)")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

def main():
    """Main test function"""
    print("Testing main.py Integration with Flask App")
    print("=" * 50)
    
    # Test backend health first
    try:
        response = requests.get(f"{BACKEND_URL}/api/health")
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print("❌ Backend is not responding")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return
    
    # Run tests
    test_list_json_files()
    test_analyze_schemas()
    test_compare_schemas()
    
    print("\n🎉 Integration test completed!")

if __name__ == "__main__":
    main()
