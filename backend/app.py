from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pandas as pd
import tempfile

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

def read_file_first_three_lines(file_path, file_type):
    """Read the first three lines/rows of different file types"""
    try:
        if file_type == 'csv':
            df = pd.read_csv(file_path, nrows=3)
            if len(df) > 0:
                lines = []
                for i in range(len(df)):
                    # Convert each row to string and join with spaces
                    line = ' '.join(str(value) for value in df.iloc[i].values)
                    lines.append(line)
                return lines
            else:
                return ["CSV file is empty"]
        
        elif file_type in ['xlsx', 'xls']:
            df = pd.read_excel(file_path, nrows=3)
            if len(df) > 0:
                lines = []
                for i in range(len(df)):
                    # Convert each row to string and join with spaces
                    line = ' '.join(str(value) for value in df.iloc[i].values)
                    lines.append(line)
                return lines
            else:
                return ["Excel file is empty"]
        
        return ["Unable to read file"]
    
    except Exception as e:
        return [f"Error reading file: {str(e)}"]

@app.route('/api/process-files', methods=['POST'])
def process_files():
    """Process uploaded files and return first three lines of each"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400
        
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
                        'lines': [f"File too large (max 50MB)"],
                        'error': True
                    })
                    continue
                
                # Get file extension
                file_ext = file.filename.rsplit('.', 1)[1].lower()
                
                # Save file temporarily
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_ext}')
                file.save(temp_file.name)
                temp_files.append(temp_file.name)
                
                # Read first three lines
                lines = read_file_first_three_lines(temp_file.name, file_ext)
                print(f"DEBUG: Processing {file.filename}, lines: {lines}")  # Debug log
                results.append({
                    'filename': file.filename,
                    'lines': lines,
                    'error': False
                })
            
            else:
                results.append({
                    'filename': file.filename,
                    'lines': [f"Invalid file type. Only CSV and Excel files are supported."],
                    'error': True
                })
        
        # Clean up temporary files
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
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