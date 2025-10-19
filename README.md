# Research Paper Agent - MERN Stack Generator

A powerful agent that extracts content from research papers (PDF) and automatically generates complete MERN stack applications based on the analysis.

## 🚀 Features

- **PDF Content Extraction**: Extract text content from research papers using PyPDF2 and pdfplumber
- **Intelligent Analysis**: Analyze research paper content to identify key concepts, features, and requirements
- **MERN Stack Generation**: Generate complete MERN (MongoDB, Express.js, React.js, Node.js) applications
- **Code Display**: Display generated code content separately for review
- **ZIP Download**: Create downloadable ZIP files with complete project structure
- **Local Directory Support**: Download ZIP files to specified local directories

## 📋 Requirements

- Python 3.7+
- Google ADK
- Node.js (for running generated applications)
- MongoDB (for database)

## 🛠️ Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Node.js dependencies (after generating project):**
   ```bash
   cd backend && npm install
   cd ../frontend && npm install
   ```

## 🎯 Usage

### Basic Usage

```python
from agent import research_agent

# Extract content from PDF
content = research_agent.extract_pdf_content("path/to/research_paper.pdf")

# Analyze content and generate structure
project_structure, concepts = research_agent.analyze_content_and_generate_structure(content)

# Generate MERN stack code
generated_code = research_agent.generate_mern_code(concepts, "my-research-app")

# Create downloadable ZIP file
zip_path = research_agent.create_zip_file("my-research-app", "downloads/")
print(f"Project ready at: {zip_path}")
```

### Running the Example

```bash
python example_usage.py
```

## 📁 Generated Project Structure

The agent generates a complete MERN stack project with the following structure:

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
