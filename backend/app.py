from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pandas as pd
import tempfile
from openpyxl import load_workbook

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins (production-ready)

# Environment configuration
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
app.config['HOST'] = os.environ.get('FLASK_HOST', '0.0.0.0')
app.config['PORT'] = int(os.environ.get('PORT', 5000))  # Dynamic port for production

# Configuration
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_tab_title_from_excel(file_path, sheet_name):
    """Extract title from merged cell (rows 1-4, columns A-B) in Excel sheet"""
    try:
        workbook = load_workbook(file_path, data_only=True)
        worksheet = workbook[sheet_name]
        
        # Check if there's a merged cell covering A1:B4
        for merged_range in worksheet.merged_cells.ranges:
            # Check if the merged cell covers the title area (A1:B4)
            if merged_range.min_row <= 4 and merged_range.max_row >= 1 and \
               merged_range.min_col <= 2 and merged_range.max_col >= 1:
                # Get the value from the top-left cell of the merged range
                title_cell = worksheet.cell(merged_range.min_row, merged_range.min_col)
                if title_cell.value:
                    return str(title_cell.value).strip()
        
        # Fallback: try to get value from A1 if no merged cell found
        title_cell = worksheet['A1']
        if title_cell.value:
            return str(title_cell.value).strip()
        
        return f"Tab: {sheet_name}"  # Default title if no title found
        
    except Exception as e:
        print(f"Error extracting title from {sheet_name}: {str(e)}")
        return f"Tab: {sheet_name}"  # Fallback title

def read_file_first_three_lines(file_path, file_type, is_schema=False):
    """Read the first three lines/rows of different file types"""
    try:
        if file_type == 'csv':
            if is_schema:
                # For schema files, read from line 5 onwards (skip first 4 lines, read 3 lines starting from line 5)
                df = pd.read_csv(file_path, skiprows=4, nrows=3)
            else:
                # For regular files, read first 3 lines (including headers)
                df = pd.read_csv(file_path, nrows=3)
            
            if len(df) > 0:
                lines = []
                for i in range(len(df)):
                    # Convert each row to string and join with spaces
                    line = ' '.join(str(value) for value in df.iloc[i].values)
                    lines.append(line)
                return {"single_tab": {"title": "CSV Data", "lines": lines}}
            else:
                return {"single_tab": {"title": "CSV Data", "lines": ["CSV file is empty"]}}
        
        elif file_type in ['xlsx', 'xls']:
            if is_schema:
                # For schema files, process multiple tabs and extract titles
                return process_excel_schema_file(file_path)
            else:
                # For regular files, read first 3 lines (including headers)
                df = pd.read_excel(file_path, nrows=3)
                
                if len(df) > 0:
                    lines = []
                    for i in range(len(df)):
                        # Convert each row to string and join with spaces
                        line = ' '.join(str(value) for value in df.iloc[i].values)
                        lines.append(line)
                    return {"single_tab": {"title": "Excel Data", "lines": lines}}
                else:
                    return {"single_tab": {"title": "Excel Data", "lines": ["Excel file is empty"]}}
        
        return {"single_tab": {"title": "Unknown", "lines": ["Unable to read file"]}}
    
    except Exception as e:
        return {"single_tab": {"title": "Error", "lines": [f"Error reading file: {str(e)}"]}}

def process_excel_schema_file(file_path):
    """Process Excel schema file with multiple tabs"""
    try:
        # Get all sheet names
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names
        
        tabs_data = {}
        
        for sheet_name in sheet_names:
            try:
                # Extract title from merged cell (A1:B4)
                title = extract_tab_title_from_excel(file_path, sheet_name)
                
                # Read data starting from row 5 (skip first 4 rows, read 3 lines)
                df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=4, nrows=3)
                
                lines = []
                if len(df) > 0:
                    for i in range(len(df)):
                        # Convert each row to string and join with spaces
                        line = ' '.join(str(value) for value in df.iloc[i].values)
                        lines.append(line)
                else:
                    lines = ["No data in this tab"]
                
                tabs_data[sheet_name] = {
                    "title": title,
                    "lines": lines
                }
                
            except Exception as e:
                tabs_data[sheet_name] = {
                    "title": f"Error reading {sheet_name}",
                    "lines": [f"Error processing tab: {str(e)}"]
                }
        
        return {"multiple_tabs": tabs_data}
        
    except Exception as e:
        return {"single_tab": {"title": "Error", "lines": [f"Error processing Excel file: {str(e)}"]}}

@app.route('/api/process-files', methods=['POST'])
def process_files():
    """Process uploaded files and return first three lines of each"""
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
                file_size = file.tell()
                file.seek(0)  # Reset to beginning
                
                if file_size > MAX_FILE_SIZE:
                    results.append({
                        'filename': file.filename,
                        'data': {"single_tab": {"title": "Error", "lines": [f"File too large (max 50MB)"]}},
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
                
                # Read first three lines
                file_data = read_file_first_three_lines(temp_file.name, file_ext, is_schema)
                print(f"DEBUG: Processing {file.filename} (schema: {is_schema}), data: {file_data}")  # Debug log
                results.append({
                    'filename': file.filename,
                    'data': file_data,
                    'error': False
                })
            
            else:
                results.append({
                    'filename': file.filename,
                    'data': {"single_tab": {"title": "Error", "lines": [f"Invalid file type. Only CSV and Excel files are supported."]}},
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
        
        print(f"DEBUG: Final results: {results}")  # Debug log
        
        return jsonify({
            'success': True,
            'results': results,
            'file_count': len(valid_files)
        })
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Bridgette backend is running'})

if __name__ == '__main__':
    print("Starting Bridgette Backend Server...")
    print(f"Backend will be available at: http://{app.config['HOST']}:{app.config['PORT']}")
    print("API Endpoints:")
    print("  POST /api/process-files - Process uploaded files (any number)")
    print("  GET  /api/health - Health check")
    print("Supported formats: CSV, Excel (.xlsx, .xls)")
    print(f"Environment: {'Development' if app.config['DEBUG'] else 'Production'}")
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])