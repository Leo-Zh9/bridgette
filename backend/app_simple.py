from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import csv
import tempfile

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
ALLOWED_EXTENSIONS = {'csv'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_csv_first_two_lines(file_path):
    """Read the first two lines of a CSV file"""
    try:
        lines = []
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i >= 2:  # Only read first 2 lines
                    break
                # Join row values with spaces
                line = ' '.join(str(value) for value in row)
                lines.append(line)
        return lines
    except Exception as e:
        return [f"Error reading file: {str(e)}"]

@app.route('/api/process-files', methods=['POST'])
def process_files():
    """Process exactly two uploaded CSV files and return first two lines of each"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        files = request.files.getlist('files')
        
        # Filter out empty files
        valid_files = [file for file in files if file and file.filename != '']
        
        if len(valid_files) != 2:
            return jsonify({'error': 'Please upload exactly 2 files'}), 400
        
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
                        'lines': [f"File too large (max 10MB)"],
                        'error': True
                    })
                    continue
                
                # Save file temporarily
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
                file.save(temp_file.name)
                temp_files.append(temp_file.name)
                
                # Read first two lines
                lines = read_csv_first_two_lines(temp_file.name)
                results.append({
                    'filename': file.filename,
                    'lines': lines,
                    'error': False
                })
            
            else:
                results.append({
                    'filename': file.filename,
                    'lines': [f"Invalid file type. Only CSV files are supported in this simplified version."],
                    'error': True
                })
        
        # Clean up temporary files
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
        
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
    return jsonify({'status': 'healthy', 'message': 'Bridgette backend is running (CSV only)'})

if __name__ == '__main__':
    print("Starting Bridgette Backend Server (Simplified - CSV Only)...")
    print("Backend will be available at: http://localhost:5000")
    print("API Endpoints:")
    print("  POST /api/process-files - Process exactly 2 CSV files")
    print("  GET  /api/health - Health check")
    print("Supported formats: CSV only (simplified version)")
    app.run(debug=True, host='0.0.0.0', port=5000)
