# Research Paper Agent - Web Application Generator

A powerful web application that extracts content from research papers (PDF) and automatically generates complete web applications based on the analysis. Upload a PDF, choose your technology stack, and download a ready-to-use application!

## 🌟 Features

- **Modern Web Interface**: Beautiful, responsive React frontend with drag-and-drop PDF upload
- **PDF Content Extraction**: Extract text content from research papers using PyPDF2 and pdfplumber
- **Intelligent Analysis**: Analyze research paper content to identify key concepts, features, and requirements
- **Multiple Technology Stacks**: Generate applications using MERN, MEAN, LAMP, Django, Spring Boot, Laravel, Flask, or Ruby on Rails
- **Real-time Processing**: Upload PDF and get instant analysis with progress indicators
- **ZIP Download**: Create downloadable ZIP files with complete project structure
- **RESTful API**: Clean Flask backend API for easy integration

## 📋 Requirements

- Python 3.7+
- Node.js 16+
- Google ADK
- Modern web browser

## 🛠️ Quick Setup

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create necessary directories:**
   ```bash
   mkdir uploads
   ```

## 🎯 Usage

### Starting the Application

1. **Run the setup script:**
   ```bash
   # Windows
   setup.bat
   
   # Linux/Mac
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Start the application:**
   ```bash
   python app.py
   ```

3. **Open your browser** and go to `http://localhost:8080`

### Using the Web Interface

1. **Upload a PDF** research paper using the drag-and-drop interface
2. **Choose your technology stack** from the dropdown menu
3. **Click "Generate Application"** and wait for processing
4. **Download the ZIP file** containing your complete application
5. **Extract the ZIP file** and follow the included README instructions

### Running Generated Applications

Each generated ZIP file includes:

- **Complete web application** with all necessary files
- **Comprehensive README.md** with detailed setup instructions
- **Startup scripts** for easy launching:
  - `start-windows.bat` (Windows)
  - `start.sh` (Linux/Mac)
- **Environment configuration** files
- **All dependencies** properly configured

#### Quick Start for Generated Apps:
1. **Extract the ZIP file**
2. **Run the startup script:**
   - Windows: Double-click `start-windows.bat`
   - Linux/Mac: Run `chmod +x start.sh && ./start.sh`
3. **Open browser** to `http://localhost:3000`

### API Usage

You can also use the API directly:

```bash
# Upload a PDF and generate application
curl -X POST -F "file=@research_paper.pdf" -F "technology=MERN Stack" http://localhost:8080/api/upload

# Download the generated ZIP file
curl -O http://localhost:8080/api/download/research-app.zip
```

## 📁 Generated Project Structure

The agent generates complete web applications with the following structure (example for MERN Stack):

```
research-app/
├── backend/
│   ├── package.json
│   ├── server.js
│   ├── .env
│   ├── models/
│   │   ├── User.js
│   │   └── ResearchPaper.js
│   └── routes/
│       ├── auth.js
│       └── research.js
├── frontend/
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.js
│       ├── index.js
│       ├── components/
│       ├── pages/
│       │   ├── Dashboard.js
│       │   └── UploadPaper.js
│       └── styles/
│           └── App.css
└── README.md
```

**Note:** The structure varies based on the selected technology stack (MERN, MEAN, LAMP, Django, Spring Boot, Laravel, Flask, or Ruby on Rails).

## 🔧 Generated Features

Based on research paper analysis, the agent automatically generates:

- **User Authentication System**: Registration, login, JWT tokens
- **Research Paper Management**: Upload, view, and manage papers
- **Dashboard**: Analytics and overview of papers
- **Admin Panel**: User and content management
- **API Endpoints**: RESTful API for all operations
- **Responsive UI**: Modern React components with CSS styling

## 📊 Content Analysis

The agent analyzes research papers to extract:

- **Keywords**: Important terms and concepts
- **Technical Terms**: API, database, authentication, etc.
- **Features**: User management, dashboards, analytics, etc.
- **Requirements**: Based on content patterns and terminology

## 🎨 Customization

You can customize the generated applications by:

1. **Modifying the analysis logic** in `extract_key_concepts()`
2. **Adding new code templates** in `generate_mern_code()`
3. **Extending the project structure** in `analyze_content_and_generate_structure()`

## 📝 API Reference

### ResearchPaperAgent Class

#### Methods

- `extract_pdf_content(pdf_path)`: Extract text from PDF file
- `analyze_content_and_generate_structure(content)`: Analyze content and generate project structure
- `generate_mern_code(concepts, project_name)`: Generate MERN stack code files
- `create_zip_file(project_name, download_path)`: Create downloadable ZIP file

## 🚀 Running Generated Applications

### Backend Setup
```bash
cd backend
npm install
npm run dev
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Database Setup
1. Install MongoDB
2. Update `.env` file with your MongoDB connection string
3. Start MongoDB service

## 🔍 Example Output

When you run the agent with a research paper, you'll get:

1. **Extracted Content**: Full text from the PDF
2. **Analysis Results**: Keywords, features, and concepts
3. **Project Structure**: Complete MERN stack layout
4. **Generated Code**: All necessary files with proper implementation
5. **ZIP File**: Ready-to-use project in your specified directory

## 🛡️ Security Features

- JWT-based authentication
- Password hashing with bcrypt
- CORS configuration
- Input validation
- Error handling

## 📈 Performance Features

- Efficient PDF text extraction
- Optimized React components
- MongoDB indexing
- Responsive design
- Modern ES6+ JavaScript

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the example usage
2. Review the generated code
3. Ensure all dependencies are installed
4. Verify MongoDB is running

## 🔄 Updates

The agent continuously improves based on:
- New research paper patterns
- Updated MERN stack best practices
- User feedback and requirements
- Technology advancements

---

**Happy coding! 🎉**
