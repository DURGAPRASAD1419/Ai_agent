from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
import os
import tempfile
import zipfile
from werkzeug.utils import secure_filename
from agent import research_agent
import json

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serve the main web interface"""
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Research Paper Agent API is running'})

@app.route('/api/upload', methods=['POST'])
def upload_pdf():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        technology = request.form.get('technology', 'MERN Stack')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the PDF
        content = research_agent.extract_pdf_content(file_path)
        
        if content.startswith("Error"):
            return jsonify({'error': f'Error extracting PDF: {content}'}), 400
        
        # Analyze content and generate structure
        project_structure, concepts = research_agent.analyze_content_and_generate_structure(content)
        
        # Generate code with specified technology
        project_name = "research-app"
        generated_code = research_agent.generate_code_for_technology(concepts, project_name, technology)
        
        # Create ZIP file in uploads directory for easier access
        uploads_dir = app.config['UPLOAD_FOLDER']
        research_agent.generated_code = generated_code
        zip_path = research_agent.create_zip_file(project_name, uploads_dir)
        
        if zip_path.startswith("Error"):
            return jsonify({'error': f'Error creating ZIP file: {zip_path}'}), 500
        
        # Clean up uploaded file
        os.remove(file_path)
        
        # Return analysis results and ZIP file info
        return jsonify({
            'success': True,
            'analysis': {
                'keywords': concepts['keywords'][:10],
                'technical_terms': concepts['technical_terms'],
                'features': concepts['features'],
                'abstract': content[:800] + "..." if len(content) > 800 else content
            },
            'project_structure': list(generated_code.keys()),
            'zip_filename': os.path.basename(zip_path),
            'zip_path': zip_path,
            'technology': technology
        })
        
    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500

@app.route('/api/download/<filename>')
def download_zip(filename):
    try:
        # Look for ZIP file in uploads directory first
        uploads_dir = app.config['UPLOAD_FOLDER']
        zip_path = os.path.join(uploads_dir, filename)
        
        if os.path.exists(zip_path):
            return send_file(zip_path, as_attachment=True, download_name=filename)
        
        # If not found in uploads, check temp directories
        temp_dirs = [tempfile.gettempdir()]
        
        for temp_dir in temp_dirs:
            zip_path = os.path.join(temp_dir, filename)
            if os.path.exists(zip_path):
                return send_file(zip_path, as_attachment=True, download_name=filename)
        
        return jsonify({'error': 'File not found'}), 404
        
    except Exception as e:
        return jsonify({'error': f'Download error: {str(e)}'}), 500

@app.route('/api/technologies', methods=['GET'])
def get_technologies():
    technologies = [
        {'id': 'MERN Stack', 'name': 'MERN Stack', 'description': 'MongoDB, Express.js, React.js, Node.js'},
        {'id': 'MEAN Stack', 'name': 'MEAN Stack', 'description': 'MongoDB, Express.js, Angular, Node.js'},
        {'id': 'LAMP Stack', 'name': 'LAMP Stack', 'description': 'Linux, Apache, MySQL, PHP'},
        {'id': 'Django Stack', 'name': 'Django Stack', 'description': 'Python, Django, PostgreSQL, React'},
        {'id': 'Spring Boot Stack', 'name': 'Spring Boot Stack', 'description': 'Java, Spring Boot, MySQL, React'},
        {'id': 'Laravel Stack', 'name': 'Laravel Stack', 'description': 'PHP, Laravel, MySQL, Vue.js'},
        {'id': 'Flask Stack', 'name': 'Flask Stack', 'description': 'Python, Flask, SQLite, React'},
        {'id': 'Ruby on Rails Stack', 'name': 'Ruby on Rails Stack', 'description': 'Ruby, Rails, PostgreSQL, React'}
    ]
    return jsonify(technologies)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
