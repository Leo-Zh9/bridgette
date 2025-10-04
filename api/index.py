from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pandas as pd
import tempfile

app = Flask(__name__)
CORS(app)

# Configuration
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_file_first_three_lines(file_path, file_type):
    try:
        if file_type == 'csv':
            df = pd.read_csv(file_path, nrows=3)
            if len(df) > 0:
                lines = []
                for i in range(len(df)):
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
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        files = request.files.getlist('files')
        valid_files = [file for file in files if file and file.filename != '']
        
        if len(valid_files) == 0:
            return jsonify({'error': 'Please upload at least 1 file'}), 400
        
        results = []
        temp_files = []
        
        for file in valid_files:
            if allowed_file(file.filename):
                file.seek(0, 2)
                file_size = file.tell()
                file.seek(0)
                
                if file_size > MAX_FILE_SIZE:
                    results.append({
                        'filename': file.filename,
                        'lines': [f"File too large (max 10MB)"],
                        'error': True
                    })
                    continue
                
                file_ext = file.filename.rsplit('.', 1)[1].lower()
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_ext}')
                file.save(temp_file.name)
                temp_files.append(temp_file.name)
                
                lines = read_file_first_three_lines(temp_file.name, file_ext)
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
    return jsonify({'status': 'healthy', 'message': 'Bridgette backend is running'})

# Vercel handler
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
