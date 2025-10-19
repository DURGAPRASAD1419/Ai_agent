from google.adk.agents.llm_agent import Agent
import PyPDF2
import pdfplumber
import zipfile
import os
import json
import re
from pathlib import Path
import tempfile
import shutil

class ResearchPaperAgent:
    def __init__(self):
        self.extracted_content = ""
        self.project_structure = {}
        self.generated_code = {}
        
    def extract_pdf_content(self, pdf_path):
        """Extract text content from PDF file"""
        try:
            content = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        content += page_text + "\n"
            
            self.extracted_content = content
            return content
        except Exception as e:
            return f"Error extracting PDF: {str(e)}"
    
    def analyze_content_and_generate_structure(self, content):
        """Analyze research paper content and generate MERN stack project structure"""
        # Extract key concepts and requirements from the research paper
        concepts = self.extract_key_concepts(content)
        
        # Generate project structure based on analysis
        project_structure = {
            "backend": {
                "package.json": "Node.js backend package configuration",
                "server.js": "Express server setup",
                "models/": "MongoDB models directory",
                "routes/": "API routes directory",
                "controllers/": "Business logic controllers",
                "middleware/": "Custom middleware",
                "config/": "Database and app configuration",
                ".env": "Environment variables"
            },
            "frontend": {
                "package.json": "React frontend package configuration",
                "public/": "Static assets",
                "src/": {
                    "components/": "React components",
                    "pages/": "Page components",
                    "services/": "API service calls",
                    "utils/": "Utility functions",
                    "styles/": "CSS/styling files",
                    "App.js": "Main App component",
                    "index.js": "React entry point"
                }
            },
            "database": {
                "models/": "MongoDB schemas and models",
                "seeders/": "Database seed data"
            }
        }
        
        self.project_structure = project_structure
        return project_structure, concepts
    
    def extract_key_concepts(self, content):
        """Extract key concepts, features, and requirements from research paper"""
        # Simple keyword extraction and analysis
        keywords = re.findall(r'\b[A-Z][a-z]+\b', content)
        technical_terms = re.findall(r'\b(?:API|database|authentication|user|admin|dashboard|analytics|reporting|management|system)\b', content, re.IGNORECASE)
        
        # Extract potential features based on common patterns
        features = []
        if 'user' in content.lower():
            features.append('User Management')
        if 'authentication' in content.lower() or 'login' in content.lower():
            features.append('Authentication System')
        if 'dashboard' in content.lower():
            features.append('Dashboard')
        if 'analytics' in content.lower() or 'report' in content.lower():
            features.append('Analytics & Reporting')
        if 'admin' in content.lower():
            features.append('Admin Panel')
        
        return {
            'keywords': list(set(keywords[:20])),  # Top 20 unique keywords
            'technical_terms': list(set(technical_terms)),
            'features': features,
            'content_length': len(content)
        }
    
    def generate_mern_code(self, concepts, project_name="research-app"):
        """Generate MERN stack code files based on extracted concepts"""
        generated_code = {}
        
        # Backend package.json
        generated_code['backend/package.json'] = {
            "name": f"{project_name}-backend",
            "version": "1.0.0",
            "description": "Backend API for research paper application",
            "main": "server.js",
            "scripts": {
                "start": "node server.js",
                "dev": "nodemon server.js"
            },
            "dependencies": {
                "express": "^4.18.2",
                "mongoose": "^7.5.0",
                "cors": "^2.8.5",
                "dotenv": "^16.3.1",
                "bcryptjs": "^2.4.3",
                "jsonwebtoken": "^9.0.2",
                "multer": "^1.4.5-lts.1"
            },
            "devDependencies": {
                "nodemon": "^3.0.1"
            }
        }
        
        # Express server.js
        generated_code['backend/server.js'] = f'''const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({{ extended: true }}));

// Database connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/{project_name}', {{
    useNewUrlParser: true,
    useUnifiedTopology: true,
}})
.then(() => console.log('MongoDB connected successfully'))
.catch(err => console.log('MongoDB connection error:', err));

// Routes
app.get('/', (req, res) => {{
    res.json({{ message: 'Research Paper Application API is running!' }});
}});

// API routes
app.use('/api/auth', require('./routes/auth'));
app.use('/api/users', require('./routes/users'));
app.use('/api/research', require('./routes/research'));

app.listen(PORT, () => {{
    console.log(`Server is running on port ${{PORT}}`);
}});
'''
        
        # MongoDB User model
        generated_code['backend/models/User.js'] = '''const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
    username: {
        type: String,
        required: true,
        unique: true,
        trim: true
    },
    email: {
        type: String,
        required: true,
        unique: true,
        lowercase: true
    },
    password: {
        type: String,
        required: true,
        minlength: 6
    },
    role: {
        type: String,
        enum: ['user', 'admin'],
        default: 'user'
    },
    researchPapers: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'ResearchPaper'
    }]
}, {
    timestamps: true
});

// Hash password before saving
userSchema.pre('save', async function(next) {
    if (!this.isModified('password')) return next();
    this.password = await bcrypt.hash(this.password, 12);
    next();
});

// Compare password method
userSchema.methods.comparePassword = async function(candidatePassword) {
    return await bcrypt.compare(candidatePassword, this.password);
};

module.exports = mongoose.model('User', userSchema);
'''
        
        # Research Paper model
        generated_code['backend/models/ResearchPaper.js'] = '''const mongoose = require('mongoose');

const researchPaperSchema = new mongoose.Schema({
    title: {
        type: String,
        required: true
    },
    abstract: {
        type: String,
        required: true
    },
    authors: [{
        name: String,
        affiliation: String
    }],
    keywords: [String],
    content: {
        type: String,
        required: true
    },
    extractedFeatures: {
        concepts: [String],
        technicalTerms: [String],
        features: [String]
    },
    uploadedBy: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true
    },
    filePath: String,
    uploadDate: {
        type: Date,
        default: Date.now
    }
}, {
    timestamps: true
});

module.exports = mongoose.model('ResearchPaper', researchPaperSchema);
'''
        
        # Auth routes
        generated_code['backend/routes/auth.js'] = '''const express = require('express');
const jwt = require('jsonwebtoken');
const User = require('../models/User');
const router = express.Router();

// Register
router.post('/register', async (req, res) => {
    try {
        const { username, email, password } = req.body;
        
        // Check if user exists
        const existingUser = await User.findOne({ $or: [{ email }, { username }] });
        if (existingUser) {
            return res.status(400).json({ message: 'User already exists' });
        }
        
        const user = new User({ username, email, password });
        await user.save();
        
        const token = jwt.sign({ userId: user._id }, process.env.JWT_SECRET || 'fallback-secret', { expiresIn: '7d' });
        
        res.status(201).json({
            message: 'User created successfully',
            token,
            user: { id: user._id, username: user.username, email: user.email }
        });
    } catch (error) {
        res.status(500).json({ message: 'Server error', error: error.message });
    }
});

// Login
router.post('/login', async (req, res) => {
    try {
        const { email, password } = req.body;
        
        const user = await User.findOne({ email });
        if (!user) {
            return res.status(400).json({ message: 'Invalid credentials' });
        }
        
        const isMatch = await user.comparePassword(password);
        if (!isMatch) {
            return res.status(400).json({ message: 'Invalid credentials' });
        }
        
        const token = jwt.sign({ userId: user._id }, process.env.JWT_SECRET || 'fallback-secret', { expiresIn: '7d' });
        
        res.json({
            message: 'Login successful',
            token,
            user: { id: user._id, username: user.username, email: user.email }
        });
    } catch (error) {
        res.status(500).json({ message: 'Server error', error: error.message });
    }
});

module.exports = router;
'''
        
        # Research routes
        generated_code['backend/routes/research.js'] = '''const express = require('express');
const ResearchPaper = require('../models/ResearchPaper');
const router = express.Router();

// Get all research papers
router.get('/', async (req, res) => {
    try {
        const papers = await ResearchPaper.find().populate('uploadedBy', 'username');
        res.json(papers);
    } catch (error) {
        res.status(500).json({ message: 'Server error', error: error.message });
    }
});

// Get single research paper
router.get('/:id', async (req, res) => {
    try {
        const paper = await ResearchPaper.findById(req.params.id).populate('uploadedBy', 'username');
        if (!paper) {
            return res.status(404).json({ message: 'Research paper not found' });
        }
        res.json(paper);
    } catch (error) {
        res.status(500).json({ message: 'Server error', error: error.message });
    }
});

// Create new research paper
router.post('/', async (req, res) => {
    try {
        const paper = new ResearchPaper(req.body);
        await paper.save();
        res.status(201).json(paper);
    } catch (error) {
        res.status(500).json({ message: 'Server error', error: error.message });
    }
});

module.exports = router;
'''
        
        # Frontend package.json
        generated_code['frontend/package.json'] = {
            "name": f"{project_name}-frontend",
            "version": "1.0.0",
            "private": True,
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.15.0",
                "axios": "^1.5.0",
                "react-scripts": "5.0.1"
            },
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "eject": "react-scripts eject"
            },
            "eslintConfig": {
                "extends": ["react-app", "react-app/jest"]
            },
            "browserslist": {
                "production": [">0.2%", "not dead", "not op_mini all"],
                "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
            }
        }
        
        # React App.js
        generated_code['frontend/src/App.js'] = '''import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import ResearchPapers from './pages/ResearchPapers';
import UploadPaper from './pages/UploadPaper';
import Login from './pages/Login';
import Register from './pages/Register';
import './styles/App.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      // Verify token and set user
      setUser({ token });
    }
    setLoading(false);
  }, []);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <Router>
      <div className="App">
        <Navbar user={user} setUser={setUser} />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/papers" element={<ResearchPapers />} />
            <Route 
              path="/upload" 
              element={user ? <UploadPaper /> : <Navigate to="/login" />} 
            />
            <Route 
              path="/login" 
              element={user ? <Navigate to="/" /> : <Login setUser={setUser} />} 
            />
            <Route 
              path="/register" 
              element={user ? <Navigate to="/" /> : <Register setUser={setUser} />} 
            />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
'''
        
        # React Dashboard component
        generated_code['frontend/src/pages/Dashboard.js'] = '''import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Dashboard.css';

const Dashboard = () => {
  const [papers, setPapers] = useState([]);
  const [stats, setStats] = useState({
    totalPapers: 0,
    totalUsers: 0,
    recentUploads: 0
  });

  useEffect(() => {
    fetchPapers();
    fetchStats();
  }, []);

  const fetchPapers = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/research');
      setPapers(response.data);
    } catch (error) {
      console.error('Error fetching papers:', error);
    }
  };

  const fetchStats = async () => {
    // Mock stats for now
    setStats({
      totalPapers: papers.length,
      totalUsers: 10,
      recentUploads: papers.filter(p => {
        const uploadDate = new Date(p.uploadDate);
        const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
        return uploadDate > weekAgo;
      }).length
    });
  };

  return (
    <div className="dashboard">
      <h1>Research Paper Dashboard</h1>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Papers</h3>
          <p className="stat-number">{stats.totalPapers}</p>
        </div>
        <div className="stat-card">
          <h3>Total Users</h3>
          <p className="stat-number">{stats.totalUsers}</p>
        </div>
        <div className="stat-card">
          <h3>Recent Uploads</h3>
          <p className="stat-number">{stats.recentUploads}</p>
        </div>
      </div>

      <div className="recent-papers">
        <h2>Recent Research Papers</h2>
        <div className="papers-grid">
          {papers.slice(0, 6).map(paper => (
            <div key={paper._id} className="paper-card">
              <h3>{paper.title}</h3>
              <p className="authors">
                {paper.authors.map(author => author.name).join(', ')}
              </p>
              <p className="abstract">{paper.abstract.substring(0, 150)}...</p>
              <div className="keywords">
                {paper.keywords.slice(0, 3).map(keyword => (
                  <span key={keyword} className="keyword-tag">{keyword}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
'''
        
        # Upload Paper component
        generated_code['frontend/src/pages/UploadPaper.js'] = '''import React, { useState } from 'react';
import axios from 'axios';
import './UploadPaper.css';

const UploadPaper = () => {
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState('');
  const [abstract, setAbstract] = useState('');
  const [authors, setAuthors] = useState('');
  const [keywords, setKeywords] = useState('');
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !title || !abstract) {
      setMessage('Please fill in all required fields');
      return;
    }

    setUploading(true);
    setMessage('');

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('title', title);
      formData.append('abstract', abstract);
      formData.append('authors', authors);
      formData.append('keywords', keywords);

      const response = await axios.post('http://localhost:5000/api/research/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      setMessage('Research paper uploaded successfully!');
      setFile(null);
      setTitle('');
      setAbstract('');
      setAuthors('');
      setKeywords('');
    } catch (error) {
      setMessage('Error uploading paper: ' + error.response?.data?.message || error.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-paper">
      <h1>Upload Research Paper</h1>
      
      <form onSubmit={handleSubmit} className="upload-form">
        <div className="form-group">
          <label htmlFor="file">PDF File *</label>
          <input
            type="file"
            id="file"
            accept=".pdf"
            onChange={handleFileChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="title">Title *</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="abstract">Abstract *</label>
          <textarea
            id="abstract"
            value={abstract}
            onChange={(e) => setAbstract(e.target.value)}
            rows="4"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="authors">Authors (comma-separated)</label>
          <input
            type="text"
            id="authors"
            value={authors}
            onChange={(e) => setAuthors(e.target.value)}
            placeholder="John Doe, Jane Smith"
          />
        </div>

        <div className="form-group">
          <label htmlFor="keywords">Keywords (comma-separated)</label>
          <input
            type="text"
            id="keywords"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
            placeholder="machine learning, AI, research"
          />
        </div>

        <button type="submit" disabled={uploading} className="submit-btn">
          {uploading ? 'Uploading...' : 'Upload Paper'}
        </button>

        {message && (
          <div className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
            {message}
          </div>
        )}
      </form>
    </div>
  );
};

export default UploadPaper;
'''
        
        # Environment file
        generated_code['backend/.env'] = '''PORT=5000
MONGODB_URI=mongodb://localhost:27017/research-app
JWT_SECRET=your-super-secret-jwt-key-here
NODE_ENV=development
'''
        
        # README file
        generated_code['README.md'] = f'''# {project_name.title()} - Research Paper Analysis Application

## Overview
This MERN stack application was generated based on the analysis of a research paper. It provides functionality for uploading, analyzing, and managing research papers.

## Features
{chr(10).join([f"- {feature}" for feature in concepts.get('features', [])])}

## Tech Stack
- **Frontend**: React.js
- **Backend**: Node.js, Express.js
- **Database**: MongoDB
- **Authentication**: JWT

## Installation

### Backend Setup
1. Navigate to backend directory: `cd backend`
2. Install dependencies: `npm install`
3. Create a `.env` file with your configuration
4. Start the server: `npm run dev`

### Frontend Setup
1. Navigate to frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the development server: `npm start`

## API Endpoints
- `GET /api/research` - Get all research papers
- `POST /api/research` - Create new research paper
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

## Generated Features
Based on the research paper analysis, the following features were identified and implemented:
{chr(10).join([f"- {feature}" for feature in concepts.get('features', [])])}

## Key Concepts Extracted
{chr(10).join([f"- {keyword}" for keyword in concepts.get('keywords', [])[:10]])}
'''
        
        self.generated_code = generated_code
        return generated_code
    
    def create_zip_file(self, project_name="research-app", download_path=None):
        """Create a ZIP file with all generated code and return the local path"""
        try:
            # Create temporary directory for the project
            temp_dir = tempfile.mkdtemp()
            project_dir = os.path.join(temp_dir, project_name)
            os.makedirs(project_dir, exist_ok=True)
            
            # Create directory structure
            backend_dir = os.path.join(project_dir, 'backend')
            frontend_dir = os.path.join(project_dir, 'frontend')
            models_dir = os.path.join(backend_dir, 'models')
            routes_dir = os.path.join(backend_dir, 'routes')
            src_dir = os.path.join(frontend_dir, 'src')
            components_dir = os.path.join(src_dir, 'components')
            pages_dir = os.path.join(src_dir, 'pages')
            styles_dir = os.path.join(src_dir, 'styles')
            public_dir = os.path.join(frontend_dir, 'public')
            
            for directory in [backend_dir, frontend_dir, models_dir, routes_dir, 
                            src_dir, components_dir, pages_dir, styles_dir, public_dir]:
                os.makedirs(directory, exist_ok=True)
            
            # Write all generated files
            for file_path, content in self.generated_code.items():
                full_path = os.path.join(project_dir, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                if isinstance(content, dict):
                    # Handle JSON files like package.json
                    with open(full_path, 'w') as f:
                        json.dump(content, f, indent=2)
                else:
                    # Handle text files
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)
            
            # Create additional necessary files
            self._create_additional_files(project_dir, src_dir, public_dir)
            
            # Create ZIP file
            zip_path = os.path.join(download_path or temp_dir, f"{project_name}.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(project_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, project_dir)
                        zipf.write(file_path, arcname)
            
            return zip_path
            
        except Exception as e:
            return f"Error creating ZIP file: {str(e)}"
    
    def _create_additional_files(self, project_dir, src_dir, public_dir):
        """Create additional necessary files for the MERN stack project"""
        
        # Frontend index.js
        index_js = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
'''
        with open(os.path.join(src_dir, 'index.js'), 'w') as f:
            f.write(index_js)
        
        # Frontend index.html
        index_html = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="Research Paper Analysis Application" />
    <title>Research Paper App</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
'''
        with open(os.path.join(public_dir, 'index.html'), 'w') as f:
            f.write(index_html)
        
        # Basic CSS
        app_css = '''* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f5f5;
}

.App {
  min-height: 100vh;
}

.main-content {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: 18px;
}

/* Dashboard Styles */
.dashboard h1 {
  color: #333;
  margin-bottom: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
}

.stat-number {
  font-size: 2em;
  font-weight: bold;
  color: #007bff;
  margin-top: 10px;
}

.papers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.paper-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.paper-card h3 {
  color: #333;
  margin-bottom: 10px;
}

.authors {
  color: #666;
  font-style: italic;
  margin-bottom: 10px;
}

.abstract {
  color: #555;
  line-height: 1.5;
  margin-bottom: 15px;
}

.keywords {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.keyword-tag {
  background: #e9ecef;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8em;
  color: #495057;
}

/* Upload Form Styles */
.upload-form {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  max-width: 600px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #333;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.submit-btn {
  background: #007bff;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  width: 100%;
}

.submit-btn:hover:not(:disabled) {
  background: #0056b3;
}

.submit-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.message {
  margin-top: 15px;
  padding: 10px;
  border-radius: 4px;
}

.message.success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.message.error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}
'''
        with open(os.path.join(src_dir, 'styles', 'App.css'), 'w') as f:
            f.write(app_css)

# Initialize the research paper agent
research_agent = ResearchPaperAgent()

def process_user_query(user_input, pdf_file_path=None):
    """
    Process user queries and handle PDF uploads for research paper analysis
    """
    try:
        # Check if user is greeting
        if any(keyword in user_input.lower() for keyword in ['hi', 'hello', 'hey', 'greetings']):
            return "Please upload your research paper in the form of PDF."
        
        # If PDF file is provided, ask for programming language
        if pdf_file_path and os.path.exists(pdf_file_path):
            return "Please specify the programming language you want to use for the MERN stack implementation."
        
        # Check if user is specifying programming language
        if any(keyword in user_input.lower() for keyword in ['javascript', 'typescript', 'python', 'java', 'c#', 'php', 'go', 'rust', 'node', 'react', 'angular', 'vue']):
            return process_pdf_with_language(pdf_file_path, user_input)
        
        # For any other input, ask for PDF upload
        return "Please upload your research paper in the form of PDF."
    
    except Exception as e:
        return "Please upload your research paper in the form of PDF."

def process_pdf_with_language(pdf_path, language):
    """
    Process a PDF file with specified programming language and generate MERN stack application
    """
    try:
        # Step 1: Extract content from PDF
        content = research_agent.extract_pdf_content(pdf_path)
        
        if content.startswith("Error"):
            return f"Error extracting PDF: {content}"
        
        # Step 2: Analyze content and generate structure
        project_structure, concepts = research_agent.analyze_content_and_generate_structure(content)
        
        # Step 3: Generate MERN stack code with specified language
        project_name = "research-app"
        generated_code = research_agent.generate_mern_code(concepts, project_name)
        
        # Step 4: Create ZIP file in project's downloads folder
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        downloads_folder = os.path.join(project_root, "downloads")
        os.makedirs(downloads_folder, exist_ok=True)
        
        zip_path = research_agent.create_zip_file(project_name, downloads_folder)
        
        if zip_path.startswith("Error"):
            return f"Error creating ZIP file: {zip_path}"
        
        # Step 5: Generate comprehensive response
        response = f"""
RESEARCH PAPER ANALYSIS COMPLETE!

ABSTRACT:
{content[:500]}...

KEY INSIGHTS:
- Keywords: {', '.join(concepts['keywords'][:10])}
- Technical Terms: {', '.join(concepts['technical_terms'])}
- Features: {', '.join(concepts['features'])}
- Content Length: {concepts['content_length']} characters

PROJECT STRUCTURE:
"""
        
        for file_path in generated_code.keys():
            response += f"- {file_path}\n"
        
        response += f"""

CODE IMPLEMENTATIONS:

=== BACKEND SERVER.JS ===
"""
        
        # Add backend server code
        if 'backend/server.js' in generated_code:
            server_code = generated_code['backend/server.js']
            response += server_code + "\n"
        
        response += """
=== FRONTEND APP.JS ===
"""
        
        # Add frontend app code
        if 'frontend/src/App.js' in generated_code:
            app_code = generated_code['frontend/src/App.js']
            response += app_code + "\n"
        
        response += """
=== BACKEND PACKAGE.JSON ===
"""
        
        # Add package.json content
        if 'backend/package.json' in generated_code:
            import json
            package_json = generated_code['backend/package.json']
            response += json.dumps(package_json, indent=2) + "\n"
        
        response += """
=== FRONTEND PACKAGE.JSON ===
"""
        
        # Add frontend package.json
        if 'frontend/package.json' in generated_code:
            frontend_package = generated_code['frontend/package.json']
            response += json.dumps(frontend_package, indent=2) + "\n"
        
        # Add all other code files
        for file_path, file_content in generated_code.items():
            if file_path not in ['backend/server.js', 'frontend/src/App.js', 'backend/package.json', 'frontend/package.json']:
                response += f"""
=== {file_path.upper()} ===
"""
                if isinstance(file_content, dict):
                    response += json.dumps(file_content, indent=2) + "\n"
        else:
                    response += str(file_content) + "\n"
        
        response += f"""

DOWNLOAD INFORMATION:
- ZIP File Path: {zip_path}
- File Name: {os.path.basename(zip_path)}
- File Size: {os.path.getsize(zip_path)} bytes
- Programming Language: {language}
- Download Location: Your project folder

DIRECT DOWNLOAD LINK:
file://{zip_path.replace(os.sep, '/')}

CLICK TO DOWNLOAD:
The ZIP file has been automatically saved to your project folder.
You can access it at: {zip_path}

NEXT STEPS:
1. Navigate to your project folder: {project_root}
2. Open the downloads folder
3. Find the file: {os.path.basename(zip_path)}
4. Extract the ZIP file
5. Install dependencies: npm install (in both backend and frontend folders)
6. Set up MongoDB database
7. Update .env file with your configuration
8. Start backend: npm run dev (in backend folder)
9. Start frontend: npm start (in frontend folder)

Your complete MERN stack application is ready to use!
"""
        
        return response
    
    except Exception as e:
        return f"Error processing PDF: {str(e)}"

def process_pdf_file(pdf_path):
    """
    Process a PDF file and generate MERN stack application
    """
    try:
        # Step 1: Extract content from PDF
        content = research_agent.extract_pdf_content(pdf_path)
        
        if content.startswith("Error"):
            return f"Error extracting PDF: {content}"
        
        # Step 2: Analyze content and generate structure
        project_structure, concepts = research_agent.analyze_content_and_generate_structure(content)
        
        # Step 3: Generate MERN stack code
        project_name = "research-app"
        generated_code = research_agent.generate_mern_code(concepts, project_name)
        
        # Step 4: Create ZIP file
        download_path = os.path.join(os.getcwd(), "downloads")
        os.makedirs(download_path, exist_ok=True)
        
        zip_path = research_agent.create_zip_file(project_name, download_path)
        
        if zip_path.startswith("Error"):
            return f"Error creating ZIP file: {zip_path}"
        
        # Prepare comprehensive response
        response = f"""
RESEARCH PAPER ANALYSIS COMPLETE!

Analysis Results:
- Keywords: {', '.join(concepts['keywords'][:5])}...
- Technical Terms: {', '.join(concepts['technical_terms'])}
- Features: {', '.join(concepts['features'])}
- Content Length: {concepts['content_length']} characters

GENERATED PROJECT STRUCTURE:
"""
        
        for file_path in generated_code.keys():
            response += f"- {file_path}\n"
        
        response += f"""

MERN STACK APPLICATION GENERATED SUCCESSFULLY!

DOWNLOAD INFORMATION:
- ZIP File: {zip_path}
- File Size: {os.path.getsize(zip_path)} bytes
- Project Name: {project_name}

SAMPLE GENERATED CODE:

=== BACKEND SERVER.JS ===
"""
        
        # Add sample backend code
        if 'backend/server.js' in generated_code:
            server_code = generated_code['backend/server.js']
            response += server_code[:800] + "\n...\n"
        
        response += """
=== FRONTEND APP.JS ===
"""
        
        # Add sample frontend code
        if 'frontend/src/App.js' in generated_code:
            app_code = generated_code['frontend/src/App.js']
            response += app_code[:800] + "\n...\n"
        
        response += f"""

=== BACKEND PACKAGE.JSON ===
"""
        
        # Add package.json content
        if 'backend/package.json' in generated_code:
            import json
            package_json = generated_code['backend/package.json']
            response += json.dumps(package_json, indent=2) + "\n"
        
        response += f"""

NEXT STEPS:
1. Extract the ZIP file from: {zip_path}
2. Install dependencies: npm install (in both backend and frontend folders)
3. Set up MongoDB database
4. Update .env file with your configuration
5. Start backend: npm run dev (in backend folder)
6. Start frontend: npm start (in frontend folder)

Your complete MERN stack application is ready to use!
"""
        
        return response
        
    except Exception as e:
        return f"Error processing PDF: {str(e)}"

root_agent = Agent(
    model='gemini-2.5-flash',
    name='research_paper_agent',
    description='An agent that extracts content from research papers and generates MERN stack applications.',
    instruction='''You are a research paper analysis agent with a specific conversation flow:

1. When user says "hi" or greets you, respond: "Please upload your research paper in the form of PDF."

2. When user uploads a PDF, respond: "Please specify the programming language you want to use for the MERN stack implementation."

3. When user specifies a programming language, automatically:
   - Extract the PDF content
   - Analyze the content to identify key concepts and features
   - Generate a complete MERN stack project structure
   - Create all necessary code files (backend and frontend)
   - Display the abstract and key insights from the PDF
   - Show the project structure
   - Display code implementations separately
   - Create a downloadable ZIP file with all files
   - Provide the local directory path for the ZIP file

Follow this exact conversation flow. Be conversational and helpful.
''',
)
