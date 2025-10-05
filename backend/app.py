from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pandas as pd
import tempfile
import json
from openpyxl import load_workbook
from datetime import datetime
import numpy as np
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins (production-ready)

# Environment configuration
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
app.config['HOST'] = os.environ.get('FLASK_HOST', '0.0.0.0')
app.config['PORT'] = int(os.environ.get('PORT', 5000))  # Dynamic port for production

# Configuration
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Create directory for storing JSON files
JSON_STORAGE_DIR = 'json_storage'
if not os.path.exists(JSON_STORAGE_DIR):
    os.makedirs(JSON_STORAGE_DIR)

def convert_to_json_serializable(obj):
    """Convert numpy types and other non-JSON serializable objects to JSON serializable types"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (datetime, pd.Timestamp)):
        return obj.isoformat()
    elif pd.isna(obj):
        return None
    else:
        return obj

def save_json_data(json_data, filename, is_schema=False):
    """Save JSON data to a file with a unique ID"""
    # Generate unique ID for this conversion
    unique_id = str(uuid.uuid4())
    
    # Create filename with timestamp and unique ID
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_type = "schema" if is_schema else "data"
    json_filename = f"{timestamp}_{file_type}_{unique_id[:8]}_{filename.replace('.', '_')}.json"
    
    # Save to JSON storage directory
    json_filepath = os.path.join(JSON_STORAGE_DIR, json_filename)
    
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    return json_filename, unique_id

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_schema_title_from_excel(file_path, sheet_name):
    """Extract title from rows 1-4, columns A-B in Excel sheet for schema files"""
    try:
        workbook = load_workbook(file_path, data_only=True)
        worksheet = workbook[sheet_name]
        
        # Check merged cells first
        for merged_range in worksheet.merged_cells.ranges:
            if merged_range.min_row <= 4 and merged_range.max_row >= 1 and \
               merged_range.min_col <= 2 and merged_range.max_col >= 1:
                title_cell = worksheet.cell(merged_range.min_row, merged_range.min_col)
                if title_cell.value:
                    return str(title_cell.value).strip()
        
        # Try to get title from cells A1:B4
        title_parts = []
        for row in range(1, 5):  # Rows 1-4
            for col in range(1, 3):  # Columns A-B
                cell_value = worksheet.cell(row, col).value
                if cell_value:
                    title_parts.append(str(cell_value).strip())
        
        if title_parts:
            return ' '.join(title_parts)
        
        return f"Tab: {sheet_name}"  # Default title
        
    except Exception as e:
        print(f"Error extracting schema title from {sheet_name}: {str(e)}")
        return f"Tab: {sheet_name}"

def convert_csv_to_json(file_path, is_schema=False):
    """Convert CSV file to JSON format"""
    try:
        if is_schema:
            # For schema files: skip first 4 rows, use row 5 as headers, read all remaining data
            df = pd.read_csv(file_path, skiprows=4)
        else:
            # For normal files: use first row as headers, read all data
            df = pd.read_csv(file_path)
        
        if len(df) == 0:
            return {"error": "CSV file is empty"}
        
        # Get column names
        columns = df.columns.tolist()
        
        # Convert DataFrame to list of dictionaries
        data = []
        for _, row in df.iterrows():
            row_dict = {}
            for col in columns:
                row_dict[col] = convert_to_json_serializable(row[col])
            data.append(row_dict)
        
        return {
            "filename": os.path.basename(file_path),
            "file_type": "CSV",
            "is_schema": is_schema,
            "columns": columns,
            "row_count": len(data),
            "data": data
        }
        
    except Exception as e:
        return {"error": f"Error processing CSV file: {str(e)}"}

def convert_excel_to_json(file_path, is_schema=False):
    """Convert Excel file to JSON format"""
    try:
        # Get all sheet names
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names
        
        if len(sheet_names) == 1:
            # Single sheet - treat as regular file
            sheet_name = sheet_names[0]
            
            if is_schema:
                # For schema files: extract title from rows 1-4, skip first 4 rows, use row 5 as headers
                title = extract_schema_title_from_excel(file_path, sheet_name)
                df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=4)
            else:
                # For normal files: use first row as headers
                title = f"Sheet: {sheet_name}"
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            if len(df) == 0:
                return {"error": f"Excel sheet '{sheet_name}' is empty"}
            
            # Get column names
            columns = df.columns.tolist()
            
            # Convert DataFrame to list of dictionaries
            data = []
            for _, row in df.iterrows():
                row_dict = {}
                for col in columns:
                    row_dict[col] = convert_to_json_serializable(row[col])
                data.append(row_dict)
            
            return {
                "filename": os.path.basename(file_path),
                "file_type": "Excel",
                "is_schema": is_schema,
                "title": title,
                "sheet_name": sheet_name,
                "columns": columns,
                "row_count": len(data),
                "data": data
            }
        
        else:
            # Multiple sheets - process each sheet
            sheets_data = {}
            total_rows = 0
            
            for sheet_name in sheet_names:
                try:
                    if is_schema:
                        # For schema files: extract title from rows 1-4, skip first 4 rows, use row 5 as headers
                        title = extract_schema_title_from_excel(file_path, sheet_name)
                        df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=4)
                    else:
                        # For normal files: use first row as headers
                        title = f"Sheet: {sheet_name}"
                        df = pd.read_excel(file_path, sheet_name=sheet_name)
                    
                    if len(df) == 0:
                        sheets_data[sheet_name] = {
                            "title": title,
                            "columns": [],
                            "row_count": 0,
                            "data": [],
                            "error": f"Sheet '{sheet_name}' is empty"
                        }
                        continue
                    
                    # Get column names
                    columns = df.columns.tolist()
                    
                    # Convert DataFrame to list of dictionaries
                    data = []
                    for _, row in df.iterrows():
                        row_dict = {}
                        for col in columns:
                            row_dict[col] = convert_to_json_serializable(row[col])
                        data.append(row_dict)
                    
                    sheets_data[sheet_name] = {
                        "title": title,
                        "columns": columns,
                        "row_count": len(data),
                        "data": data
                    }
                    
                    total_rows += len(data)
                    
                except Exception as e:
                    sheets_data[sheet_name] = {
                        "title": f"Sheet: {sheet_name}",
                        "error": f"Error processing sheet '{sheet_name}': {str(e)}"
                    }
            
            return {
                "filename": os.path.basename(file_path),
                "file_type": "Excel",
                "is_schema": is_schema,
                "sheet_count": len(sheet_names),
                "total_rows": total_rows,
                "sheets": sheets_data
            }
        
    except Exception as e:
        return {"error": f"Error processing Excel file: {str(e)}"}

def convert_file_to_json(file_path, file_type, is_schema=False):
    """Convert file to JSON format based on file type"""
    try:
        if file_type == 'csv':
            return convert_csv_to_json(file_path, is_schema)
        elif file_type in ['xlsx', 'xls']:
            return convert_excel_to_json(file_path, is_schema)
        else:
            return {"error": f"Unsupported file type: {file_type}"}
    
    except Exception as e:
        return {"error": f"Error converting file to JSON: {str(e)}"}

@app.route('/api/process-files', methods=['POST'])
def process_files():
    """Process uploaded files and convert them to JSON format"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        # Check if this is a schema file request
        is_schema = request.args.get('schema', 'false').lower() == 'true'
        
        files = request.files.getlist('files')
        
        # Filter out empty files
        valid_files = [file for file in files if file and file.filename != '']
        
        if len(valid_files) == 0:
            return jsonify({'error': 'Please upload at least 1 file'}), 400
        
        results = []
        temp_files = []
        
        for file in valid_files:
            if allowed_file(file.filename):
                # Check file size
                file.seek(0, 2)  # Seek to end
                file_size = int(file.tell())
                file.seek(0)  # Reset to beginning
                
                if file_size > MAX_FILE_SIZE:
                    results.append({
                        'filename': file.filename,
                        'json_data': {"error": f"File too large (max {MAX_FILE_SIZE // (1024*1024)}MB)"},
                        'error': True
                    })
                    continue
                
                # Get file extension
                file_ext = file.filename.rsplit('.', 1)[1].lower()
                
                # Save file temporarily with proper Windows path handling
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_ext}')
                temp_file.close()  # Close the file handle to avoid conflicts
                file.save(temp_file.name)
                temp_files.append(temp_file.name)
                
                # Convert file to JSON
                json_data = convert_file_to_json(temp_file.name, file_ext, is_schema)
                print(f"DEBUG: Processing {file.filename} (schema: {is_schema}), rows: {json_data.get('row_count', json_data.get('total_rows', 0))}")  # Debug log
                
                # Save JSON data to file if conversion was successful
                json_filename = None
                unique_id = None
                if 'error' not in json_data:
                    json_filename, unique_id = save_json_data(json_data, file.filename, is_schema)
                    print(f"DEBUG: Saved JSON to {json_filename}")
                
                results.append({
                    'filename': file.filename,
                    'json_data': json_data,
                    'error': 'error' in json_data,
                    'json_filename': json_filename,
                    'unique_id': unique_id
                })
            
            else:
                results.append({
                    'filename': file.filename,
                    'json_data': {"error": "Invalid file type. Only CSV and Excel files are supported."},
                    'error': True
                })
        
        # Clean up temporary files with better error handling
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except Exception as cleanup_error:
                print(f"Warning: Could not delete temp file {temp_file}: {cleanup_error}")
                pass
        
        print(f"DEBUG: Final results count: {len(results)}")  # Debug log
        
        return jsonify({
            'success': True,
            'results': results,
            'file_count': len(valid_files),
            'is_schema': is_schema
        })
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Bridgette backend is running'})

@app.route('/api/json-files', methods=['GET'])
def list_json_files():
    """List all saved JSON files"""
    try:
        if not os.path.exists(JSON_STORAGE_DIR):
            return jsonify({'files': []})
        
        files = []
        for filename in os.listdir(JSON_STORAGE_DIR):
            if filename.endswith('.json'):
                filepath = os.path.join(JSON_STORAGE_DIR, filename)
                file_stats = os.stat(filepath)
                files.append({
                    'filename': filename,
                    'size': file_stats.st_size,
                    'created': datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
                    'modified': datetime.fromtimestamp(file_stats.st_mtime).isoformat()
                })
        
        # Sort by creation time (newest first)
        files.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({'files': files})
    
    except Exception as e:
        return jsonify({'error': f'Error listing files: {str(e)}'}), 500

@app.route('/api/json-files/<filename>', methods=['GET'])
def get_json_file(filename):
    """Get a specific JSON file by filename"""
    try:
        filepath = os.path.join(JSON_STORAGE_DIR, filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        with open(filepath, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        return jsonify(json_data)
    
    except Exception as e:
        return jsonify({'error': f'Error reading file: {str(e)}'}), 500

@app.route('/api/json-files/<filename>', methods=['DELETE'])
def delete_json_file(filename):
    """Delete a specific JSON file"""
    try:
        filepath = os.path.join(JSON_STORAGE_DIR, filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        os.remove(filepath)
        return jsonify({'message': f'File {filename} deleted successfully'})
    
    except Exception as e:
        return jsonify({'error': f'Error deleting file: {str(e)}'}), 500

@app.route('/api/start-merging', methods=['POST'])
def start_merging():
    """Start the merging process with OpenAI API"""
    try:
        data = request.get_json()
        
        if not data or 'files' not in data:
            return jsonify({'error': 'No files provided for merging'}), 400
        
        files = data['files']
        
        if len(files) == 0:
            return jsonify({'error': 'No files in merging queue'}), 400
        
        # Load all JSON files
        merged_data = {
            'merged_at': datetime.now().isoformat(),
            'total_files': len(files),
            'files': []
        }
        
        for file_info in files:
            json_filename = file_info['jsonFilename']
            filepath = os.path.join(JSON_STORAGE_DIR, json_filename)
            
            if not os.path.exists(filepath):
                return jsonify({'error': f'JSON file not found: {json_filename}'}), 404
            
            # Load JSON data
            with open(filepath, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            merged_data['files'].append({
                'original_filename': file_info['originalFilename'],
                'json_filename': json_filename,
                'unique_id': file_info['uniqueId'],
                'data': json_data
            })
        
        # Save merged data
        merged_filename = f"merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        merged_filepath = os.path.join(JSON_STORAGE_DIR, merged_filename)
        
        with open(merged_filepath, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, indent=2, ensure_ascii=False)
        
        print(f"DEBUG: Merged data saved to {merged_filename}")
        
        return jsonify({
            'success': True,
            'message': 'Merging completed successfully',
            'merged_filename': merged_filename,
            'merged_url': f'/api/json-files/{merged_filename}',
            'total_files': len(files),
            'files_processed': [f['originalFilename'] for f in files]
        })
    
    except Exception as e:
        return jsonify({'error': f'Error during merging: {str(e)}'}), 500

if __name__ == '__main__':
    print("Starting Bridgette Backend Server...")
    print(f"Backend will be available at: http://{app.config['HOST']}:5001")
    print("API Endpoints:")
    print("  POST /api/process-files - Convert uploaded files to JSON format")
    print("    - ?schema=true for schema files (titles from rows 1-4, headers from row 5)")
    print("    - No parameter for normal files (headers from row 1)")
    print("  GET  /api/health - Health check")
    print("  GET  /api/json-files - List all saved JSON files")
    print("  GET  /api/json-files/<filename> - Get specific JSON file")
    print("  DELETE /api/json-files/<filename> - Delete JSON file")
    print("  POST /api/start-merging - Start merging process for OpenAI API")
    print("Supported formats: CSV, Excel (.xlsx, .xls)")
    print("Features:")
    print("  - Converts all data to JSON with key-value pairs")
    print("  - Preserves filenames and metadata")
    print("  - Handles multiple Excel tabs with titles")
    print("  - Optimized for large files (up to 50MB)")
    print(f"Environment: {'Development' if app.config['DEBUG'] else 'Production'}")
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=5001)