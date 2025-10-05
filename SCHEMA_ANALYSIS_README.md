# Schema Analysis and Matching

This document describes the new functionality for processing ChatGPT responses and creating separate JSON files for matched and unmatched schemas.

## Overview

The system now includes functions to:
1. Parse ChatGPT responses that contain schema matches in a specific format
2. Create separate JSON files for matched schemas and unmatched schemas from each bank
3. Provide statistics about the matching process

## New Functions

### `parse_chatgpt_response(response_text, bank1_data, bank2_data)`

Parses a ChatGPT response and extracts matched and unmatched schemas.

**Parameters:**
- `response_text` (str): The response from ChatGPT
- `bank1_data` (dict): Bank 1 JSON data
- `bank2_data` (dict): Bank 2 JSON data

**Returns:**
- Dictionary containing matched schemas, unmatched schemas for each bank, and statistics

### `create_schema_json_files(parsed_data, output_dir=".")`

Creates separate JSON files for matched and unmatched schemas.

**Parameters:**
- `parsed_data` (dict): Parsed data from ChatGPT response
- `output_dir` (str): Directory to save JSON files

**Returns:**
- Dictionary with paths to created files

### `process_chatgpt_schema_analysis(chatgpt_response, bank1_json_path, bank2_json_path, output_dir="schema_analysis")`

Complete function that processes ChatGPT response and creates all JSON files.

**Parameters:**
- `chatgpt_response` (str): The response text from ChatGPT
- `bank1_json_path` (str): Path to Bank 1 JSON file
- `bank2_json_path` (str): Path to Bank 2 JSON file
- `output_dir` (str): Directory to save output JSON files

**Returns:**
- Dictionary with paths to created files, or None if error

## Expected ChatGPT Response Format

The system expects ChatGPT responses in this specific format:

```
(Bank 1: schema_category/schema_name, Bank 2: schema_category/schema_name)
(Bank 1: schema_category/schema_name, Bank 2: schema_category/schema_name)
...

(list of bank 1 schemas unmatched)

(list of bank 2 schemas unmatched)
```

## Output Files

The system creates three JSON files:

### 1. `matched_schemas.json`
Contains all matched schemas between the two banks:
```json
{
  "matched_schemas": [
    {
      "bank1": {
        "category": "Customer",
        "schema": "name"
      },
      "bank2": {
        "category": "Customer", 
        "schema": "full_name"
      }
    }
  ],
  "statistics": {
    "total_matched": 5,
    "total_unmatched_bank1": 2,
    "total_unmatched_bank2": 3,
    "total_schemas": 10
  }
}
```

### 2. `unmatched_bank1_schemas.json`
Contains unmatched schemas from Bank 1:
```json
{
  "unmatched_schemas": [
    {
      "category": "Customer",
      "schema": "customer_id",
      "description": "Unique customer identifier",
      "data": { /* original schema data */ }
    }
  ],
  "bank": "Bank 1",
  "count": 2
}
```

### 3. `unmatched_bank2_schemas.json`
Contains unmatched schemas from Bank 2:
```json
{
  "unmatched_schemas": [
    {
      "category": "Account",
      "schema": "account_number",
      "description": "Account identifier",
      "data": { /* original schema data */ }
    }
  ],
  "bank": "Bank 2", 
  "count": 3
}
```

## Usage Example

```python
from backend.main import process_chatgpt_schema_analysis

# Process ChatGPT response and create JSON files
file_paths = process_chatgpt_schema_analysis(
    chatgpt_response=your_chatgpt_response,
    bank1_json_path="Bank1_Schema_converted.json",
    bank2_json_path="Bank2_Schema_converted.json",
    output_dir="schema_analysis"
)

if file_paths:
    print("Files created:")
    for file_type, file_path in file_paths.items():
        print(f"  {file_type}: {file_path}")
```

## Integration with Main Workflow

The main execution in `main.py` now automatically:
1. Converts Excel files to JSON
2. Sends data to ChatGPT for analysis
3. Parses the ChatGPT response
4. Creates separate JSON files for matched and unmatched schemas
5. Provides statistics about the matching process

## Error Handling

The functions include comprehensive error handling and will:
- Print error messages for debugging
- Return None on failure
- Continue processing even if some schemas can't be parsed
- Provide detailed statistics about the matching process
