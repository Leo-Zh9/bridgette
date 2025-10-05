import pandas as pd
import json
import os
import sys
from pathlib import Path
import argparse
from openai import OpenAI

def read_spreadsheet(file_path):
    """Read spreadsheet file and return appropriate engine"""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".xlsx":
        return pd.ExcelFile(file_path, engine="openpyxl")
    elif ext == ".xls":
        return pd.ExcelFile(file_path, engine="xlrd")
    elif ext == ".ods":
        return pd.ExcelFile(file_path, engine="odf")
    elif ext == ".csv":
        return "csv"
    else:
        raise ValueError(f"Unsupported file type: {ext}. Supported: .xlsx, .xls, .csv, .ods")

def clean_dataframe(df):
    """Clean dataframe by removing completely empty rows and columns"""
    # Remove completely empty rows
    df = df.dropna(how='all')
    # Remove completely empty columns
    df = df.dropna(axis=1, how='all')
    return df

def filter_header_rows(data_list):
    """Filter out header rows that contain 'name' and 'description'"""
    if not isinstance(data_list, list):
        return data_list
    
    filtered_data = []
    for item in data_list:
        if isinstance(item, dict):
            # Check if this looks like a header row
            # Look for common header patterns
            values = list(item.values())
            if len(values) >= 2:
                # Check if first two values are 'name' and 'description' (case insensitive)
                first_two = [str(v).lower().strip() for v in values[:2]]
                if 'name' in first_two and 'description' in first_two:
                    continue  # Skip this header row
                # Also check for other common header patterns
                if any(header in first_two for header in ['field', 'column', 'attribute', 'property']):
                    continue  # Skip this header row
            filtered_data.append(item)
        else:
            filtered_data.append(item)
    
    return filtered_data

def convert_to_json(file_path, output_file=None, clean_data=True, include_metadata=True):
    """
    Convert Excel/CSV file to JSON format
    
    Args:
        file_path (str): Path to input file
        output_file (str): Path to output JSON file (optional)
        clean_data (bool): Whether to clean empty rows/columns
        include_metadata (bool): Whether to include file metadata in output
    
    Returns:
        dict: The converted data
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Generate output filename if not provided
    if output_file is None:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file = f"{base_name}_converted.json"
    
    data = {}
    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext == ".csv":
            print(f"[INFO] Reading CSV file: {file_path}")
            df = pd.read_csv(file_path)
            if clean_data:
                df = clean_dataframe(df)
            records = df.to_dict(orient="records")
            # Filter out header rows
            records = filter_header_rows(records)
            data["data"] = records
            
            if include_metadata:
                data["metadata"] = {
                    "file_type": "CSV",
                    "file_name": os.path.basename(file_path),
                    "rows": len(records),
                    "columns": list(df.columns),
                    "column_count": len(df.columns)
                }
        else:
            print(f"[INFO] Reading Excel file: {file_path}")
            xls = read_spreadsheet(file_path)
            
            for sheet_name in xls.sheet_names:
                print(f"  [INFO] Processing sheet: {sheet_name}")
                df = pd.read_excel(file_path, sheet_name=sheet_name, engine=xls.engine)
                
                if clean_data:
                    df = clean_dataframe(df)
                
                records = df.to_dict(orient="records")
                # Filter out header rows
                records = filter_header_rows(records)
                data[sheet_name] = records
            
            if include_metadata:
                data["_metadata"] = {
                    "file_type": ext.upper(),
                    "file_name": os.path.basename(file_path),
                    "sheets": xls.sheet_names,
                    "sheet_count": len(xls.sheet_names),
                    "total_rows": sum(len(filter_header_rows(pd.read_excel(file_path, sheet_name=sheet, engine=xls.engine).to_dict(orient="records"))) for sheet in xls.sheet_names)
                }
        
        # Write to JSON file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"[SUCCESS] Successfully converted {file_path} to {output_file}")
        print(f"[INFO] Output file size: {os.path.getsize(output_file)} bytes")
        
        return data
        
    except Exception as e:
        print(f"[ERROR] Error processing file: {str(e)}")
        raise

def process_file(file_path, output_file=None, clean_data=True, include_metadata=True):
    """
    Process a file and convert it to JSON - main function to call directly
    
    Args:
        file_path (str): Path to the Excel/CSV file to convert
        output_file (str): Output JSON file path (optional)
        clean_data (bool): Whether to clean empty rows/columns
        include_metadata (bool): Whether to include metadata in output
    
    Returns:
        dict: The converted data
    """
    try:
        return convert_to_json(
            file_path=file_path,
            output_file=output_file,
            clean_data=clean_data,
            include_metadata=include_metadata
        )
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return None

def count_schemas_in_json(json_file_path):
    """
    Count the number of schemas in a JSON file, excluding sheet names and metadata
    
    Args:
        json_file_path (str): Path to the JSON file to analyze
    
    Returns:
        dict: Dictionary with schema counts and details
    """
    try:
        if not os.path.exists(json_file_path):
            print(f"[ERROR] JSON file not found: {json_file_path}")
            return None
        
        with open(json_file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        schema_count = 0
        sheet_counts = {}
        total_schemas = 0
        
        # Iterate through each sheet/tab in the JSON
        for sheet_name, sheet_data in json_data.items():
            # Skip metadata sections
            if sheet_name.startswith('_') or sheet_name.lower() in ['metadata', 'data']:
                continue
            
            # Count schemas in this sheet
            if isinstance(sheet_data, list):
                sheet_schema_count = len(sheet_data)
                sheet_counts[sheet_name] = sheet_schema_count
                total_schemas += sheet_schema_count
            else:
                sheet_counts[sheet_name] = 0
        
        result = {
            "file_name": os.path.basename(json_file_path),
            "total_schemas": total_schemas,
            "sheet_breakdown": sheet_counts,
            "number_of_sheets": len(sheet_counts)
        }
        
        print(f"[INFO] Schema count for {os.path.basename(json_file_path)}:")
        print(f"   Total schemas: {total_schemas}")
        print(f"   Sheets: {len(sheet_counts)}")
        for sheet, count in sheet_counts.items():
            print(f"   - {sheet}: {count} schemas")
        
        return result
        
    except Exception as e:
        print(f"[ERROR] Error counting schemas: {str(e)}")
        return None

def send_json_to_chatgpt(json_file_path, prompt, json_file_path2=None, api_key=None, model="gpt-4o", max_tokens=10000, temperature=0.7):
    """
    Send one or two JSON files to ChatGPT API with a custom prompt
    
    Args:
        json_file_path (str): Path to the first JSON file to send
        prompt (str): The prompt/question to ask about the JSON data
        json_file_path2 (str, optional): Path to the second JSON file to send
        api_key (str): OpenAI API key (optional, uses default if not provided)
        model (str): ChatGPT model to use (default: gpt-4o)
        max_tokens (int): Maximum tokens in response (default: 4000)
        temperature (float): Response creativity 0-1 (default: 0.7)
    
    Returns:
        str: ChatGPT's response, or None if error
    """
    try:
        # Read the first JSON file
        if not os.path.exists(json_file_path):
            print(f"[ERROR] JSON file not found: {json_file_path}")
            return None
        
        with open(json_file_path, 'r', encoding='utf-8') as f:
            json_data1 = json.load(f)
        
        # Read the second JSON file if provided
        json_data2 = None
        if json_file_path2:
            if not os.path.exists(json_file_path2):
                print(f"[ERROR] Second JSON file not found: {json_file_path2}")
                return None
            
            with open(json_file_path2, 'r', encoding='utf-8') as f:
                json_data2 = json.load(f)
        
        # Initialize OpenAI client
        if api_key:
            client = OpenAI(api_key=api_key)
        else:
            # Use API key from environment configuration
            try:
                from config import Config
                client = OpenAI(api_key=Config.OPENAI_API_KEY)
            except ImportError:
                raise ValueError("Configuration not found. Please ensure config.py exists and .env file is set up.")
            except Exception as e:
                raise ValueError(f"Error loading API key: {e}")
        
        # Prepare the data for the prompt
        json_str1 = json.dumps(json_data1, indent=2, ensure_ascii=False)
        
        # Calculate total length and truncate if needed
        total_length = len(json_str1)
        json_str2 = ""
        
        if json_data2:
            json_str2 = json.dumps(json_data2, indent=2, ensure_ascii=False)
            total_length += len(json_str2)
        
        # Truncate if too long (ChatGPT has token limits)
        max_length = 100000  # Rough estimate for token limit
        if total_length > max_length:
            # Distribute truncation between both files
            if json_data2:
                # Split available space between both files
                available_space = max_length - 2000  # Leave some space for prompt
                space_per_file = available_space // 2
                
                if len(json_str1) > space_per_file:
                    json_str1 = json_str1[:space_per_file] + "\n... (truncated due to length)"
                if len(json_str2) > space_per_file:
                    json_str2 = json_str2[:space_per_file] + "\n... (truncated due to length)"
            else:
                json_str1 = json_str1[:max_length] + "\n... (truncated due to length)"
            
            print("[WARNING] JSON data was truncated due to length")
        
        # Create the full prompt
        if json_data2:
            full_prompt = f"""
{prompt}

Here is the first JSON data:
{json_str1}

Here is the second JSON data:
{json_str2}
"""
        else:
            full_prompt = f"""
{prompt}

Here is the JSON data:
{json_str1}
"""
        
        print(f"[INFO] Sending request to ChatGPT...")
        print(f"[INFO] JSON file 1: {json_file_path}")
        if json_file_path2:
            print(f"[INFO] JSON file 2: {json_file_path2}")
        print(f"[INFO] Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
        
        # Send to ChatGPT
        response = client.chat.completions.create(
            model=model,
messages=[
    {
        "role": "system",
                    "content": "You are a helpful assistant that analyzes JSON data. Provide clear, detailed responses based on the data provided."
                },
                {
                    "role": "user", 
                    "content": full_prompt
                }
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        result = response.choices[0].message.content
        print(f"[SUCCESS] Received response from ChatGPT ({len(result)} characters)")
        
        return result
        
    except Exception as e:
        print(f"[ERROR] Error sending to ChatGPT: {str(e)}")
        return None

def parse_chatgpt_response(response_text, bank1_data, bank2_data):
    """
    Parse ChatGPT response and extract matched and unmatched schemas
    
    Expected format:
    (Bank 1: schema_category/schema, Bank 2: schema category/ schema(s))
    (Bank 1: schema_category/schema, Bank 2: schema category/ schema(s)) etc.
    [ one empty line ]
    header: list of bank 1 schemas unmatched)
    [ one empty line ]
    (list of bank 1 schemas unmatched)
    [ one empty line ]
    header: list of bank 1 schemas unmatched
    [ one empty line ]
    (list of bank 2 schemas unmatched)
    
    Args:
        response_text (str): The response from ChatGPT
        bank1_data (dict): Bank 1 JSON data
        bank2_data (dict): Bank 2 JSON data
    
    Returns:
        dict: Dictionary containing matched, unmatched_bank1, and unmatched_bank2 schemas
    """
    try:
        lines = response_text.strip().split('\n')
        
        matched_schemas = []
        unmatched_bank1 = []
        unmatched_bank2 = []
        
        # Track which schemas have been matched
        matched_bank1_schemas = set()
        matched_bank2_schemas = set()
        
        # Parse the response in sections
        current_section = "matched"  # Start with matched schemas
        bank1_header_found = False
        bank2_header_found = False
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check for section headers
            if "list of bank 1 schemas unmatched" in line.lower():
                current_section = "unmatched_bank1"
                bank1_header_found = True
                continue
            elif "list of bank 2 schemas unmatched" in line.lower():
                current_section = "unmatched_bank2"
                bank2_header_found = True
                continue
            
            # Parse matched schemas (lines that start with "(" and contain "Bank 1:" and "Bank 2:")
            if line.startswith('(') and 'Bank 1:' in line and 'Bank 2:' in line:
                # Extract Bank 1 schema info
                bank1_part = line.split('Bank 1:')[1].split('Bank 2:')[0].strip()
                bank2_part = line.split('Bank 2:')[1].strip()
                
                # Remove parentheses
                bank1_part = bank1_part.rstrip(')').strip()
                bank2_part = bank2_part.rstrip(')').strip()
                
                # Split category and schema name
                bank1_parts = bank1_part.split('/', 1)
                bank2_parts = bank2_part.split('/', 1)
                
                bank1_category = bank1_parts[0].strip() if len(bank1_parts) > 0 else ""
                bank1_schema = bank1_parts[1].strip() if len(bank1_parts) > 1 else bank1_parts[0].strip()
                
                bank2_category = bank2_parts[0].strip() if len(bank2_parts) > 0 else ""
                bank2_schema = bank2_parts[1].strip() if len(bank2_parts) > 1 else bank2_parts[0].strip()
                
                # Clean up any trailing commas or extra characters
                bank1_schema = bank1_schema.rstrip(',').strip()
                bank2_schema = bank2_schema.rstrip(',').strip()
                
                matched_schemas.append({
                    "bank1": {
                        "category": bank1_category,
                        "schema": bank1_schema
                    },
                    "bank2": {
                        "category": bank2_category,
                        "schema": bank2_schema
                    }
                })
                
                # Track matched schemas
                matched_bank1_schemas.add(f"{bank1_category}/{bank1_schema}")
                matched_bank2_schemas.add(f"{bank2_category}/{bank2_schema}")
            
            # Parse unmatched schemas (lines that start with "(" but don't contain "Bank 1:" and "Bank 2:")
            elif line.startswith('(') and current_section in ["unmatched_bank1", "unmatched_bank2"]:
                # Remove parentheses and clean up
                schema_text = line.strip('()').strip()
                
                # Extract category and schema name from formats like "Bank 1: Customer/ legalIssueAuthorised"
                if "Bank 1:" in schema_text and "/" in schema_text:
                    # Format: "Bank 1: Customer/ legalIssueAuthorised"
                    parts = schema_text.split("Bank 1:")[1].strip()
                    if "/" in parts:
                        category, schema_name = parts.split("/", 1)
                        category = category.strip()
                        schema_name = schema_name.strip()
                    else:
                        category = "Unknown"
                        schema_name = parts
                elif "Bank 2:" in schema_text and "/" in schema_text:
                    # Format: "Bank 2: Customer/ legalIssueAuthorised"
                    parts = schema_text.split("Bank 2:")[1].strip()
                    if "/" in parts:
                        category, schema_name = parts.split("/", 1)
                        category = category.strip()
                        schema_name = schema_name.strip()
                    else:
                        category = "Unknown"
                        schema_name = parts
                elif "/" in schema_text:
                    # Format: "Customer/ legalIssueAuthorised"
                    category, schema_name = schema_text.split("/", 1)
                    category = category.strip()
                    schema_name = schema_name.strip()
                else:
                    # Just schema name
                    category = "Unknown"
                    schema_name = schema_text
                
                if current_section == "unmatched_bank1":
                    unmatched_bank1.append({
                        "schema": schema_name,
                        "category": category,
                        "description": "",
                        "data": {}
                    })
                elif current_section == "unmatched_bank2":
                    unmatched_bank2.append({
                        "schema": schema_name,
                        "category": category,
                        "description": "",
                        "data": {}
                    })
        
        # If no unmatched schemas were found in the response, find them by comparing with original data
        if not bank1_header_found or not unmatched_bank1:
            # Find unmatched Bank 1 schemas by comparing with original data
            for sheet_name, sheet_data in bank1_data.items():
                if sheet_name.startswith('_') or sheet_name.lower() in ['metadata', 'data']:
                    continue
                    
                if isinstance(sheet_data, list):
                    for item in sheet_data:
                        if isinstance(item, dict):
                            # Try to find schema name and category
                            schema_name = item.get('name', item.get('schema_name', item.get('field_name', '')))
                            if schema_name:
                                schema_key = f"{sheet_name}/{schema_name}"
                                if schema_key not in matched_bank1_schemas:
                                    unmatched_bank1.append({
                                        "category": sheet_name,
                                        "schema": schema_name,
                                        "description": item.get('description', item.get('desc', '')),
                                        "data": item
                                    })
        
        if not bank2_header_found or not unmatched_bank2:
            # Find unmatched Bank 2 schemas by comparing with original data
            for sheet_name, sheet_data in bank2_data.items():
                if sheet_name.startswith('_') or sheet_name.lower() in ['metadata', 'data']:
                    continue
                    
                if isinstance(sheet_data, list):
                    for item in sheet_data:
                        if isinstance(item, dict):
                            # Try to find schema name and category
                            schema_name = item.get('name', item.get('schema_name', item.get('field_name', '')))
                            if schema_name:
                                schema_key = f"{sheet_name}/{schema_name}"
                                if schema_key not in matched_bank2_schemas:
                                    unmatched_bank2.append({
                                        "category": sheet_name,
                                        "schema": schema_name,
                                        "description": item.get('description', item.get('desc', '')),
                                        "data": item
                                    })
        
        return {
            "matched_schemas": matched_schemas,
            "unmatched_bank1": unmatched_bank1,
            "unmatched_bank2": unmatched_bank2,
            "statistics": {
                "total_matched": len(matched_schemas),
                "total_unmatched_bank1": len(unmatched_bank1),
                "total_unmatched_bank2": len(unmatched_bank2),
                "total_schemas": len(matched_schemas) + len(unmatched_bank1) + len(unmatched_bank2)
            }
        }
        
    except Exception as e:
        print(f"[ERROR] Error parsing ChatGPT response: {str(e)}")
        return None

def create_schema_json_files(parsed_data, output_dir="."):
    """
    Create separate JSON files for matched and unmatched schemas
    
    Args:
        parsed_data (dict): Parsed data from ChatGPT response
        output_dir (str): Directory to save JSON files
    
    Returns:
        dict: Paths to created files
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        file_paths = {}
        
        # Create matched schemas JSON
        matched_file = os.path.join(output_dir, "matched_schemas.json")
        with open(matched_file, 'w', encoding='utf-8') as f:
            json.dump({
                "matched_schemas": parsed_data["matched_schemas"],
                "statistics": parsed_data["statistics"]
            }, f, indent=2, ensure_ascii=False)
        file_paths["matched"] = matched_file
        print(f"[SUCCESS] Created matched schemas file: {matched_file}")
        
        # Create unmatched Bank 1 schemas JSON
        unmatched_bank1_file = os.path.join(output_dir, "unmatched_bank1_schemas.json")
        with open(unmatched_bank1_file, 'w', encoding='utf-8') as f:
            json.dump({
                "unmatched_schemas": parsed_data["unmatched_bank1"],
                "bank": "Bank 1",
                "count": len(parsed_data["unmatched_bank1"])
            }, f, indent=2, ensure_ascii=False)
        file_paths["unmatched_bank1"] = unmatched_bank1_file
        print(f"[SUCCESS] Created unmatched Bank 1 schemas file: {unmatched_bank1_file}")
        
        # Create unmatched Bank 2 schemas JSON
        unmatched_bank2_file = os.path.join(output_dir, "unmatched_bank2_schemas.json")
        with open(unmatched_bank2_file, 'w', encoding='utf-8') as f:
            json.dump({
                "unmatched_schemas": parsed_data["unmatched_bank2"],
                "bank": "Bank 2",
                "count": len(parsed_data["unmatched_bank2"])
            }, f, indent=2, ensure_ascii=False)
        file_paths["unmatched_bank2"] = unmatched_bank2_file
        print(f"[SUCCESS] Created unmatched Bank 2 schemas file: {unmatched_bank2_file}")
        
        # Print statistics
        stats = parsed_data["statistics"]
        print(f"\n[INFO] Schema Matching Statistics:")
        print(f"   Total matched: {stats['total_matched']}")
        print(f"   Unmatched Bank 1: {stats['total_unmatched_bank1']}")
        print(f"   Unmatched Bank 2: {stats['total_unmatched_bank2']}")
        print(f"   Total schemas processed: {stats['total_schemas']}")
        
        return file_paths
        
    except Exception as e:
        print(f"[ERROR] Error creating JSON files: {str(e)}")
        return None

def find_data_files_by_category(category_name, bank_num):
    """
    Find data files that contain the specified category
    
    Args:
        category_name (str): Category name to search for
        bank_num (int): Bank number (1 or 2)
    
    Returns:
        list: List of matching file paths
    """
    import glob
    
    # Updated to look in uploaded_files directory instead of Archive
    bank_dir = f"uploaded_files/bank{bank_num}"
    matching_files = []
    
    # Common patterns for different categories
    category_patterns = {
        "customer": ["*Customer*", "*customer*"],
        "addresses": ["*Address*", "*address*"],
        "identifications": ["*Identif*", "*identif*"],
        "accounts": ["*Account*", "*account*"],
        "loans": ["*Loan*", "*loan*"],
        "deposits": ["*Deposit*", "*deposit*"],
        "transactions": ["*Transaction*", "*transaction*"]
    }
    
    # Get all files in the bank directory
    all_files = glob.glob(f"{bank_dir}/*")
    
    # Filter by category patterns
    for file_path in all_files:
        filename = os.path.basename(file_path).lower()
        category_lower = category_name.lower()
        
        # Direct match
        if category_lower in filename:
            matching_files.append(file_path)
        # Split category name and check individual words
        elif " " in category_lower:
            category_words = category_lower.split()
            for word in category_words:
                if word in filename:
                    matching_files.append(file_path)
                    break
        # Pattern match
        elif category_lower in category_patterns:
            for pattern in category_patterns[category_lower]:
                if glob.fnmatch.fnmatch(filename, pattern.lower()):
                    matching_files.append(file_path)
                    break
    
    # Filter out temporary files
    matching_files = [f for f in matching_files if not os.path.basename(f).startswith('~$')]
    
    # Simple and direct matching based on category name
    # The key insight: match the exact category name from matched_schemas.json to the file names
    
    # Convert category name to a pattern that matches the file naming convention
    category_lower = category_name.lower()
    
    # Handle the specific cases we know about
    if "loan accounts" in category_lower and "transaction" not in category_lower:
        # Match files with "loan" and "account" but not "transaction"
        matching_files = [f for f in matching_files if "loan" in os.path.basename(f).lower() and "account" in os.path.basename(f).lower() and "transaction" not in os.path.basename(f).lower()]
    elif "loan account transactions" in category_lower:
        # Match files with "loan" and "transaction"
        matching_files = [f for f in matching_files if "loan" in os.path.basename(f).lower() and "transaction" in os.path.basename(f).lower()]
    elif "fixed term accounts" in category_lower and "transaction" not in category_lower:
        # Match files with "fixedterm" and "account" but not "transaction"
        matching_files = [f for f in matching_files if "fixedterm" in os.path.basename(f).lower() and "account" in os.path.basename(f).lower() and "transaction" not in os.path.basename(f).lower()]
    elif "fixed term account transactions" in category_lower:
        # Match files with "fixedterm" and "transaction"
        matching_files = [f for f in matching_files if "fixedterm" in os.path.basename(f).lower() and "transaction" in os.path.basename(f).lower()]
    elif "cursav accounts" in category_lower and "transaction" not in category_lower:
        # Match files with "cursav" and "account" but not "transaction"
        matching_files = [f for f in matching_files if "cursav" in os.path.basename(f).lower() and "account" in os.path.basename(f).lower() and "transaction" not in os.path.basename(f).lower()]
    elif "cursav account transactions" in category_lower:
        # Match files with "cursav" and "transaction"
        matching_files = [f for f in matching_files if "cursav" in os.path.basename(f).lower() and "transaction" in os.path.basename(f).lower()]
    elif "deposit accounts" in category_lower and "transaction" not in category_lower:
        # Match files with "deposit" and "account" but not "transaction"
        matching_files = [f for f in matching_files if "deposit" in os.path.basename(f).lower() and "account" in os.path.basename(f).lower() and "transaction" not in os.path.basename(f).lower()]
    elif "deposit account transactions" in category_lower:
        # Match files with "deposit" and "transaction"
        matching_files = [f for f in matching_files if "deposit" in os.path.basename(f).lower() and "transaction" in os.path.basename(f).lower()]
    
    return matching_files

def extract_column_data(file_path, column_name, customer_id_column="customerId"):
    """
    Extract data from a specific column in a data file
    
    Args:
        file_path (str): Path to the data file
        column_name (str): Name of the column to extract
        customer_id_column (str): Name of the customer ID column
    
    Returns:
        dict: Dictionary mapping customer_id to column value
    """
    try:
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == ".csv":
            df = pd.read_csv(file_path)
        else:
            # Use context manager to ensure file is properly closed
            with pd.ExcelFile(file_path) as xls:
                df = pd.read_excel(xls)
        
        # Check if the column exists
        if column_name not in df.columns:
            print(f"[WARNING] Column '{column_name}' not found in {file_path}")
            return {}
        
        # Check if customer ID column exists
        if customer_id_column not in df.columns:
            print(f"[WARNING] Customer ID column '{customer_id_column}' not found in {file_path}")
            return {}
        
        # Create mapping of customer_id to column value
        data_map = {}
        for _, row in df.iterrows():
            customer_id = row[customer_id_column]
            column_value = row[column_name]
            data_map[customer_id] = column_value
        
        print(f"[SUCCESS] Extracted {len(data_map)} records from {column_name} in {os.path.basename(file_path)}")
        return data_map
        
    except Exception as e:
        print(f"[ERROR] Error extracting data from {file_path}: {str(e)}")
        return {}

def create_combined_customer_data(matched_schemas, output_file="combined_customer_data.xlsx", max_customers=1000):
    """
    Create a combined spreadsheet with matched schema data from both banks
    
    Args:
        matched_schemas (list): List of matched schema pairs
        output_file (str): Output file path
        max_customers (int): Maximum number of customers to process (for performance)
    
    Returns:
        str: Path to the created file
    """
    try:
        print("[INFO] Creating combined customer data...")
        
        # Get customer IDs from each bank separately (don't try to match them)
        bank1_customer_ids = set()
        bank2_customer_ids = set()
        
        # Collect customer IDs from Bank 1
        bank1_customer_files = find_data_files_by_category("customer", 1)
        for file_path in bank1_customer_files:
            try:
                # Use context manager to ensure file is properly closed
                with pd.ExcelFile(file_path) as xls:
                    df = pd.read_excel(xls)
                    if "customerId" in df.columns:
                        # Limit to first max_customers for performance
                        customer_ids = df["customerId"].head(max_customers).tolist()
                        bank1_customer_ids.update(customer_ids)
            except Exception as e:
                print(f"[WARNING] Error reading {file_path}: {e}")
        
        # Collect customer IDs from Bank 2
        bank2_customer_files = find_data_files_by_category("customer", 2)
        for file_path in bank2_customer_files:
            try:
                # Use context manager to ensure file is properly closed
                with pd.ExcelFile(file_path) as xls:
                    df = pd.read_excel(xls)
                    if "id" in df.columns:
                        # Limit to first max_customers for performance
                        customer_ids = df["id"].head(max_customers).tolist()
                        bank2_customer_ids.update(customer_ids)
            except Exception as e:
                print(f"[WARNING] Error reading {file_path}: {e}")
        
        # Create combined list with bank prefixes to keep them separate
        all_customer_ids = [f"B1_{cid}" for cid in bank1_customer_ids] + [f"B2_{cid}" for cid in bank2_customer_ids]
        
        print(f"[INFO] Found {len(bank1_customer_ids)} Bank 1 customers and {len(bank2_customer_ids)} Bank 2 customers")
        
        # Create Bank 2 ID mapping (encodedKey -> id)
        print("[INFO] Creating Bank 2 ID mapping...")
        bank2_id_mapping = {}
        bank2_customer_files = find_data_files_by_category("customer", 2)
        for file_path in bank2_customer_files:
            try:
                df = pd.read_excel(file_path)
                if "id" in df.columns and "encodedKey" in df.columns:
                    for _, row in df.iterrows():
                        customer_id = row["id"]
                        encoded_key = row["encodedKey"]
                        bank2_id_mapping[encoded_key] = customer_id
            except Exception as e:
                print(f"[WARNING] Error reading {file_path}: {e}")
        
        print(f"[INFO] Created mapping for {len(bank2_id_mapping)} Bank 2 IDs")
        
        # Add hardcoded fixes for missing data
        print("[INFO] Applying hardcoded fixes for missing data...")
        
        # Pre-load all data maps for efficiency
        print("[INFO] Pre-loading data maps...")
        data_maps = {}
        
        for match in matched_schemas:
            bank1_schema = match["bank1"]
            bank2_schema = match["bank2"]
            
            # Load Bank 1 data
            bank1_files = find_data_files_by_category(bank1_schema["category"], 1)
            for file_path in bank1_files:
                key = f"bank1_{bank1_schema['category']}_{bank1_schema['schema']}"
                if key not in data_maps:
                    data_maps[key] = extract_column_data(file_path, bank1_schema["schema"], "customerId")
            
            # Load Bank 2 data
            bank2_files = find_data_files_by_category(bank2_schema["category"], 2)
            for file_path in bank2_files:
                # Determine the correct customer ID column based on file type
                filename = os.path.basename(file_path).lower()
                if "customer" in filename:
                    customer_id_col = "id"
                elif "address" in filename:
                    customer_id_col = "parentKey"
                elif "identif" in filename:
                    customer_id_col = "clientKey"
                elif "account" in filename:
                    customer_id_col = "accountHolderKey"
                else:
                    customer_id_col = "id"  # Default fallback
                key = f"bank2_{bank2_schema['category']}_{bank2_schema['schema']}"
                if key not in data_maps:
                    # Extract data with the appropriate customer ID column
                    raw_data = extract_column_data(file_path, bank2_schema["schema"], customer_id_col)
                    
                    # If this is account data, map accountHolderKey to customer id
                    if "account" in filename and customer_id_col == "accountHolderKey":
                        mapped_data = {}
                        for encoded_key, value in raw_data.items():
                            if encoded_key in bank2_id_mapping:
                                customer_id = bank2_id_mapping[encoded_key]
                                mapped_data[customer_id] = value
                        data_maps[key] = mapped_data
                    else:
                        data_maps[key] = raw_data
        
        # Apply hardcoded fixes for missing data
        print("[INFO] Applying hardcoded data fixes...")
        
        # Fix 1: Ensure Bank 2 account data uses correct customer ID mapping
        for key in data_maps:
            if "bank2" in key and "account" in key.lower():
                # Re-extract with proper mapping if data is empty
                if len(data_maps[key]) == 0:
                    print(f"[INFO] Fixing empty data for {key}")
                    # Find the original file and re-extract
                    for match in matched_schemas:
                        bank2_schema = match["bank2"]
                        if f"bank2_{bank2_schema['category']}_{bank2_schema['schema']}" == key:
                            bank2_files = find_data_files_by_category(bank2_schema["category"], 2)
                            for file_path in bank2_files:
                                if "account" in os.path.basename(file_path).lower():
                                    raw_data = extract_column_data(file_path, bank2_schema["schema"], "accountHolderKey")
                                    mapped_data = {}
                                    for encoded_key, value in raw_data.items():
                                        if encoded_key in bank2_id_mapping:
                                            customer_id = bank2_id_mapping[encoded_key]
                                            mapped_data[customer_id] = value
                                    data_maps[key] = mapped_data
                                    break
        
        # Fix 2: Handle transaction data with proper account ID mapping
        for key in data_maps:
            if "transaction" in key.lower():
                if len(data_maps[key]) == 0:
                    print(f"[INFO] Fixing empty transaction data for {key}")
                    # Re-extract transaction data with proper account ID mapping
                    for match in matched_schemas:
                        if "bank1" in key:
                            bank1_schema = match["bank1"]
                            if f"bank1_{bank1_schema['category']}_{bank1_schema['schema']}" == key:
                                bank1_files = find_data_files_by_category(bank1_schema["category"], 1)
                                for file_path in bank1_files:
                                    if "transaction" in os.path.basename(file_path).lower():
                                        # Use accountId for transaction files
                                        data_maps[key] = extract_column_data(file_path, bank1_schema["schema"], "accountId")
                                        break
                        elif "bank2" in key:
                            bank2_schema = match["bank2"]
                            if f"bank2_{bank2_schema['category']}_{bank2_schema['schema']}" == key:
                                bank2_files = find_data_files_by_category(bank2_schema["category"], 2)
                                for file_path in bank2_files:
                                    if "transaction" in os.path.basename(file_path).lower():
                                        # Use parentAccountKey for transaction files
                                        raw_data = extract_column_data(file_path, bank2_schema["schema"], "parentAccountKey")
                                        # Map parentAccountKey to customer ID through account files
                                        mapped_data = {}
                                        for account_key, value in raw_data.items():
                                            # Find customer ID through account mapping
                                            for acc_key, customer_id in bank2_id_mapping.items():
                                                if account_key == acc_key:
                                                    mapped_data[customer_id] = value
                                                    break
                                        data_maps[key] = mapped_data
                                        break
        
        print(f"[SUCCESS] Applied hardcoded fixes")
        
        # Create combined data structure
        combined_data = []
        
        for customer_id in all_customer_ids:
            customer_row = {"customer_id": customer_id}
            
            # Determine which bank this customer belongs to
            is_bank1 = customer_id.startswith("B1_")
            is_bank2 = customer_id.startswith("B2_")
            actual_customer_id = customer_id[3:]  # Remove B1_ or B2_ prefix
            
            # Process each matched schema pair
            for match in matched_schemas:
                bank1_schema = match["bank1"]
                bank2_schema = match["bank2"]
                
                # Create column name for the combined data
                combined_column_name = f"{bank1_schema['category']}_{bank1_schema['schema']}_to_{bank2_schema['category']}_{bank2_schema['schema']}"
                
                # Get data only from the customer's bank
                if is_bank1:
                    bank1_key = f"bank1_{bank1_schema['category']}_{bank1_schema['schema']}"
                    bank1_value = data_maps.get(bank1_key, {}).get(actual_customer_id)
                    customer_row[combined_column_name] = bank1_value
                elif is_bank2:
                    bank2_key = f"bank2_{bank2_schema['category']}_{bank2_schema['schema']}"
                    bank2_value = data_maps.get(bank2_key, {}).get(actual_customer_id)
                    customer_row[combined_column_name] = bank2_value
                else:
                    customer_row[combined_column_name] = None
            
            combined_data.append(customer_row)
        
        # Create DataFrame and save
        df_combined = pd.DataFrame(combined_data)
        df_combined.to_excel(output_file, index=False)
        
        print(f"[SUCCESS] Created combined customer data file: {output_file}")
        print(f"[INFO] Combined data shape: {df_combined.shape}")
        print(f"[INFO] Columns: {list(df_combined.columns)}")
        
        return output_file
        
    except Exception as e:
        print(f"[ERROR] Error creating combined customer data: {str(e)}")
        return None

def process_chatgpt_schema_analysis(chatgpt_response, bank1_json_path, bank2_json_path, output_dir="schema_analysis"):
    """
    Process ChatGPT response and create separate JSON files for matched and unmatched schemas
    
    Args:
        chatgpt_response (str): The response text from ChatGPT
        bank1_json_path (str): Path to Bank 1 JSON file
        bank2_json_path (str): Path to Bank 2 JSON file
        output_dir (str): Directory to save output JSON files
    
    Returns:
        dict: Paths to created files, or None if error
    """
    try:
        # Load the JSON data
        with open(bank1_json_path, 'r', encoding='utf-8') as f:
            bank1_data = json.load(f)
        
        with open(bank2_json_path, 'r', encoding='utf-8') as f:
            bank2_data = json.load(f)
        
        # Parse the ChatGPT response
        parsed_data = parse_chatgpt_response(chatgpt_response, bank1_data, bank2_data)
        
        if not parsed_data:
            print("[ERROR] Failed to parse ChatGPT response")
            return None
        
        # Create separate JSON files
        file_paths = create_schema_json_files(parsed_data, output_dir)
        
        if file_paths:
            print(f"\n[SUCCESS] Successfully processed ChatGPT response and created JSON files:")
            for file_type, file_path in file_paths.items():
                print(f"   {file_type}: {file_path}")
            return file_paths
        else:
            print("[ERROR] Failed to create JSON files")
            return None
            
    except Exception as e:
        print(f"[ERROR] Error processing ChatGPT response: {str(e)}")
        return None

def main():
    """Command line interface for the converter"""
    parser = argparse.ArgumentParser(description="Convert Excel/CSV files to JSON")
    parser.add_argument("file_path", help="Path to the Excel/CSV file to convert")
    parser.add_argument("-o", "--output", help="Output JSON file path")
    parser.add_argument("--no-clean", action="store_true", help="Don't clean empty rows/columns")
    parser.add_argument("--no-metadata", action="store_true", help="Don't include metadata in output")
    
    args = parser.parse_args()
    
    try:
        convert_to_json(
            file_path=args.file_path,
            output_file=args.output,
            clean_data=not args.no_clean,
            include_metadata=not args.no_metadata
        )
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        sys.exit(1)

 

if __name__ == "__main__":
    # Example usage - you can call process_file directly
    process_file("Archive/Bank 1 Data/Bank1_Schema.xlsx")
    process_file("Archive/Bank 2 Data/Bank2_Schema.xlsx")
    
    # Count schemas in each JSON file
    bank1_count = count_schemas_in_json("Bank1_Schema_converted.json")
    bank2_count = count_schemas_in_json("Bank2_Schema_converted.json")

    print(bank1_count, bank2_count)
    
    # Load the JSON data for parsing
    with open("Bank1_Schema_converted.json", 'r', encoding='utf-8') as f:
        bank1_data = json.load(f)
    
    with open("Bank2_Schema_converted.json", 'r', encoding='utf-8') as f:
        bank2_data = json.load(f)
    
    # Two files - compare Bank 1 and Bank 2 schemas
    response = send_json_to_chatgpt("Bank1_Schema_converted.json", 
f"""compare the schemas from the two banks provided in the JSON files. For each schema, evaluate all possible combinations and identify the best corresponding schemas based on their descriptions.

MAKE THE MAX NUMBER OF MATCHES AS POSSIBLE, HENCE LEAVE A FEW UN MATCHED SCHEMAS AS POSSIBLE. but do not force connections — if a schema really does not correspond to any other, leave it unmatched.

ALSO DO NOT MATCH A SCHEMA TO ITSELF. OR MATCH A BANK 1 SCHEMA TO A BANK 1 SCHEMA.

No schema should be omitted: every schema from both JSON files must appear in your final output, whether matched or not. HOWEVER, do not repeat any single schema twice

There are {bank1_count['total_schemas']} in the first JSON, {bank2_count['total_schemas']} in the second JSON. the list you output should have this number of schemas, weather matched or unmatched

Some schemas from one bank may correspond to multiple schemas from the other (e.g., (Bank 1: address) ↔ (Bank 2: street, house number)), while others may have no corresponding schema.

When comparing, ignore the schema category (e.g., "addresses" or "savings accounts") and rely only on the schema names and descriptions to determine correspondence.

Be careful with schemas that have similar names but different meanings — use the descriptions to distinguish them.

Output format requirement:

(Bank 1: schema cateogry / schema, Bank 2: schema category/ schema(s))
(Bank 1: schema cateogry / schema, Bank 2: schema category/ schema(s)) etc.

[ one empty line ]

header: list of bank 1 schemas unmatched

[ one empty line ]

(list of bank 1 schemas unmatched)

[ one empty line ]

header: list of bank 2 schemas unmatched

[ one empty line ]

(list of bank 2 schemas unmatched)

Provide no unnecessary text, only matches in the format above.

After all matches, include:

A list of unmatched schemas from each bank.

Statistics:

Number of all  schemas in the first JSON file

Number of all  schemas in the first JSON file

Number of schemas matched

Number of schemas unmatched

Ensure all numbers align and confirm that no schemas were left out in your analysis.""",
       "Bank2_Schema_converted.json")
    
    if response:
        print("[INFO] ChatGPT Response received, parsing and creating JSON files...")
        
        # Parse the ChatGPT response
        parsed_data = parse_chatgpt_response(response, bank1_data, bank2_data)
        
        if parsed_data:
            # Create separate JSON files for matched and unmatched schemas
            file_paths = create_schema_json_files(parsed_data, "schema_analysis")
            
            if file_paths:
                print(f"\n[SUCCESS] Successfully created all JSON files:")
                for file_type, file_path in file_paths.items():
                    print(f"   {file_type}: {file_path}")
                
                # Create combined customer data spreadsheet
                print(f"\n[INFO] Creating combined customer data spreadsheet...")
                combined_file = create_combined_customer_data(
                    parsed_data["matched_schemas"], 
                    "combined_customer_data.xlsx"
                )
                
                if combined_file:
                    print(f"[SUCCESS] Successfully created combined customer data: {combined_file}")
                else:
                    print("[ERROR] Failed to create combined customer data")
            else:
                print("[ERROR] Failed to create JSON files")
        else:
            print("[ERROR] Failed to parse ChatGPT response")
    else:
        print("[ERROR] Failed to get response from ChatGPT")
    
    # response = send_json_to_chatgpt("Bank1_Mock_CurSav_Transactions_converted.json", "What patterns do you see in these transactions?")
    
    # Run command line interface
    
