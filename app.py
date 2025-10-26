from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
import os
import tempfile
import zipfile
from werkzeug.utils import secure_filename
from agent import research_agent
import json
import subprocess
import shutil
import time
import threading
import sys

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
os.makedirs(os.path.join(UPLOAD_FOLDER, 'previews'), exist_ok=True)

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
        # Use the PDF filename (without extension) as the project and ZIP name
        pdf_basename = os.path.splitext(filename)[0]  # Remove .pdf extension
        project_name = pdf_basename
        generated_code = research_agent.generate_code_for_technology(concepts, project_name, technology)
        
        # Create ZIP file in uploads directory for easier access
        uploads_dir = app.config['UPLOAD_FOLDER']
        research_agent.generated_code = generated_code
        zip_path = research_agent.create_zip_file(project_name, uploads_dir)
        
        if zip_path.startswith("Error"):
            return jsonify({'error': f'Error creating ZIP file: {zip_path}'}), 500
        
        # Clean up uploaded file (keep it for download/preview)
        # os.remove(file_path)  # Commented out to keep the file for download
        
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

def get_file_tree(directory, base_path=""):
    """Recursively get file tree structure"""
    tree = []
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            relative_path = os.path.join(base_path, item) if base_path else item
            
            if os.path.isdir(item_path):
                tree.append((relative_path, 'directory', None))
                sub_tree = get_file_tree(item_path, relative_path)
                tree.extend(sub_tree)
            else:
                tree.append((relative_path, 'file', item_path))
    except PermissionError:
        pass
    return tree

@app.route('/api/preview/<filename>')
def preview_application(filename):
    try:
        # Look for ZIP file in uploads directory
        uploads_dir = app.config['UPLOAD_FOLDER']
        zip_path = os.path.join(uploads_dir, filename)
        
        if not os.path.exists(zip_path):
            return jsonify({'error': 'File not found'}), 404
        
        # Extract ZIP to a temporary directory for preview
        project_name = os.path.splitext(filename)[0]
        preview_dir = os.path.join(UPLOAD_FOLDER, 'previews', project_name)
        
        # Clean up old preview if it exists
        if os.path.exists(preview_dir):
            import shutil
            try:
                shutil.rmtree(preview_dir)
            except:
                pass
        
        # Create preview directory
        os.makedirs(preview_dir, exist_ok=True)
        
        # Extract ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(preview_dir)
        
        # Get the extracted project directory
        # List what was extracted to determine the structure
        extracted_contents = os.listdir(preview_dir)
        
        # Check if the ZIP created a nested directory structure
        extracted_dir = preview_dir
        if len(extracted_contents) == 1 and os.path.isdir(os.path.join(preview_dir, extracted_contents[0])):
            # ZIP contains a single top-level directory with project name
            extracted_dir = os.path.join(preview_dir, extracted_contents[0])
        
        # Verify the directory exists
        if not os.path.exists(extracted_dir):
            raise Exception(f"Extracted directory does not exist: {extracted_dir}")
        
        # Get file tree from the root of extracted files
        file_tree = get_file_tree(extracted_dir)
        
        # Look for README.md
        readme_path = os.path.join(extracted_dir, 'README.md')
        readme_content = ""
        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
        
        # Generate HTML preview
        file_list_html = ""
        for file_path, file_type, full_path in file_tree:
            if file_type == 'directory':
                file_list_html += f'<div class="file-item dir">📁 {file_path}/</div>'
            else:
                # Get file icon based on extension
                ext = os.path.splitext(file_path)[1].lower()
                icon = '📄'
                if ext in ['.js', '.jsx']:
                    icon = '📜'
                elif ext in ['.json']:
                    icon = '📋'
                elif ext in ['.html']:
                    icon = '🌐'
                elif ext in ['.css']:
                    icon = '🎨'
                elif ext in ['.py']:
                    icon = '🐍'
                elif ext in ['.java']:
                    icon = '☕'
                elif ext in ['.php']:
                    icon = '🐘'
                elif ext in ['.rb']:
                    icon = '💎'
                elif ext in ['.md']:
                    icon = '📝'
                elif ext in ['.yml', '.yaml']:
                    icon = '⚙️'
                elif ext in ['.env']:
                    icon = '🔧'
                elif ext in ['.gitignore']:
                    icon = '🚫'
                
                file_list_html += f'<div class="file-item file">{icon} {file_path}</div>'
        
        # Generate the preview page
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{project_name} - Application Preview</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
                        'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                    color: #333;
                }}
                .container {{ 
                    max-width: 1200px; 
                    margin: 0 auto; 
                    background: white;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    overflow: hidden;
                }}
                .header {{ 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 40px;
                    text-align: center;
                }}
                .header h1 {{ font-size: 2.5rem; margin-bottom: 10px; }}
                .header p {{ font-size: 1.1rem; opacity: 0.9; }}
                .content {{ padding: 40px; }}
                .section {{ margin-bottom: 40px; }}
                .section h2 {{ 
                    font-size: 1.8rem; 
                    color: #667eea; 
                    margin-bottom: 20px;
                    border-bottom: 3px solid #667eea;
                    padding-bottom: 10px;
                }}
                .file-tree {{ 
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 20px;
                    max-height: 500px;
                    overflow-y: auto;
                    font-family: 'Courier New', monospace;
                }}
                .file-item {{ 
                    padding: 8px 10px;
                    margin: 3px 0;
                    border-radius: 5px;
                    transition: all 0.2s;
                }}
                .file-item.dir {{ 
                    font-weight: bold;
                    color: #667eea;
                }}
                .file-item.file {{ 
                    color: #555;
                    padding-left: 30px;
                }}
                .file-item:hover {{
                    background: white;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .readme {{ 
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 20px;
                    border-left: 4px solid #667eea;
                    white-space: pre-wrap;
                    font-family: 'Courier New', monospace;
                    line-height: 1.6;
                    overflow-x: auto;
                }}
                .actions {{ 
                    text-align: center;
                    padding: 30px;
                    background: #f8f9fa;
                    border-top: 1px solid #e0e0e0;
                }}
                .btn {{ 
                    display: inline-block;
                    padding: 15px 40px;
                    margin: 0 10px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 50px;
                    font-weight: 600;
                    transition: all 0.3s;
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
                }}
                .btn:hover {{ 
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
                }}
                .download-btn {{ 
                    background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
                }}
                .download-btn:hover {{ 
                    box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📦 Application Preview</h1>
                    <p>{project_name}</p>
                </div>
                <div class="content">
                    <div class="section">
                        <h2>📁 Project Structure</h2>
                        <div class="file-tree">
                            {file_list_html}
                        </div>
                    </div>
                    {f'<div class="section"><h2>📝 README.md</h2><div class="readme">{readme_content}</div></div>' if readme_content else ''}
                </div>
                <div class="actions">
                    <a href="/api/download/{filename}" class="btn download-btn">⬇️ Download Full ZIP</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
        
    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html>
        <head><title>Error</title></head>
        <body style="padding: 50px; font-family: Arial, sans-serif;">
            <h1>Preview Error</h1>
            <p>{str(e)}</p>
        </body>
        </html>
        """, 500

# Store running applications
running_apps = {}

@app.route('/api/run/<filename>')
def run_application(filename):
    """Extract and run the application"""
    try:
        # Look for ZIP file
        uploads_dir = app.config['UPLOAD_FOLDER']
        zip_path = os.path.join(uploads_dir, filename)
        
        # Debug: print available files
        if os.path.exists(uploads_dir):
            available_files = os.listdir(uploads_dir)
            print(f"Available files in {uploads_dir}: {available_files}")
            print(f"Looking for: {filename}")
            print(f"Full path: {zip_path}")
            print(f"File exists: {os.path.exists(zip_path)}")
        
        if not os.path.exists(zip_path):
            # Try to find similar files
            similar_files = [f for f in os.listdir(uploads_dir) if filename.lower() in f.lower() or f.lower() in filename.lower()]
            return jsonify({
                'error': f'File not found: {filename}',
                'available_files': similar_files,
                'searched_path': zip_path
            }), 404
        
        project_name = os.path.splitext(filename)[0]
        
        # Check if already running
        if project_name in running_apps:
            return jsonify({
                'status': 'running',
                'message': 'Application is already running',
                'url': f'http://localhost:5000'  # Default backend URL
            })
        
        # Extract application
        extract_dir = os.path.join(UPLOAD_FOLDER, 'extracted', project_name)
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
        os.makedirs(extract_dir, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Get extracted directory
        extracted_contents = os.listdir(extract_dir)
        if len(extracted_contents) == 1 and os.path.isdir(os.path.join(extract_dir, extracted_contents[0])):
            extract_dir = os.path.join(extract_dir, extracted_contents[0])
        
        # Check for backend directory
        backend_dir = os.path.join(extract_dir, 'backend')
        frontend_dir = os.path.join(extract_dir, 'frontend')
        
        running_info = {
            'backend_port': 5000,
            'frontend_port': 3000,
            'backend_process': None,
            'frontend_process': None,
            'extract_dir': extract_dir
        }
        
        # Install and start backend
        if os.path.exists(backend_dir) and os.path.exists(os.path.join(backend_dir, 'package.json')):
            def install_and_start_backend():
                try:
                    # Use shell=True on Windows for better command execution
                    is_windows = sys.platform.startswith('win')
                    
                    # Install dependencies
                    install_process = subprocess.run(
                        ['npm', 'install'], 
                        cwd=backend_dir,
                        shell=is_windows,
                        capture_output=True,
                        timeout=120
                    )
                    
                    # Start backend server in a new window so user can see output
                    if is_windows:
                        subprocess.Popen(
                            ['npm', 'start'],
                            cwd=backend_dir,
                            shell=True,
                            creationflags=subprocess.CREATE_NEW_CONSOLE
                        )
                    else:
                        subprocess.Popen(
                            ['npm', 'start'],
                            cwd=backend_dir,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                    
                    print(f"Backend started successfully")
                except Exception as e:
                    print(f"Backend error: {e}")
            
            thread = threading.Thread(target=install_and_start_backend, daemon=True)
            thread.start()
            time.sleep(1)  # Give the thread a moment to start
        
        # Install and start frontend
        if os.path.exists(frontend_dir) and os.path.exists(os.path.join(frontend_dir, 'package.json')):
            def install_and_start_frontend():
                try:
                    is_windows = sys.platform.startswith('win')
                    
                    # Install dependencies
                    install_process = subprocess.run(
                        ['npm', 'install'],
                        cwd=frontend_dir,
                        shell=is_windows,
                        capture_output=True,
                        timeout=120
                    )
                    
                    # Start frontend server in a new window
                    if is_windows:
                        subprocess.Popen(
                            ['npm', 'start'],
                            cwd=frontend_dir,
                            shell=True,
                            creationflags=subprocess.CREATE_NEW_CONSOLE
                        )
                    else:
                        subprocess.Popen(
                            ['npm', 'start'],
                            cwd=frontend_dir,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                    
                    print(f"Frontend started successfully")
                except Exception as e:
                    print(f"Frontend error: {e}")
            
            thread = threading.Thread(target=install_and_start_frontend, daemon=True)
            thread.start()
            time.sleep(1)  # Give the thread a moment to start
        
        running_apps[project_name] = running_info
        
        # Wait a bit for servers to start
        time.sleep(3)
        
        return jsonify({
            'status': 'success',
            'message': 'Application is starting...',
            'backend_url': f'http://localhost:5000',
            'frontend_url': f'http://localhost:3000',
            'note': 'Please wait a moment for dependencies to install and servers to start'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error running application: {str(e)}'}), 500

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
