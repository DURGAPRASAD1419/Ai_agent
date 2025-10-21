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

    def generate_code_for_technology(self, concepts, project_name, technology):
        """Generate code based on the specified technology stack"""
        try:
            if technology == "MERN Stack":
                return self.generate_mern_code(concepts, project_name)
            elif technology == "MEAN Stack":
                return self.generate_mean_code(concepts, project_name)
            elif technology == "LAMP Stack":
                return self.generate_lamp_code(concepts, project_name)
            elif technology == "Django Stack":
                return self.generate_django_code(concepts, project_name)
            elif technology == "Spring Boot Stack":
                return self.generate_spring_boot_code(concepts, project_name)
            elif technology == "Laravel Stack":
                return self.generate_laravel_code(concepts, project_name)
            elif technology == "Flask Stack":
                return self.generate_flask_code(concepts, project_name)
            elif technology == "Ruby on Rails Stack":
                return self.generate_rails_code(concepts, project_name)
            else:
                # Default to MERN if technology not recognized
                return self.generate_mern_code(concepts, project_name)
        except Exception as e:
            return {"error": f"Error generating {technology} code: {str(e)}"}

    def generate_mean_code(self, concepts, project_name):
        """Generate MEAN stack code"""
        return {
            "backend/server.js": self._generate_express_server(),
            "backend/package.json": self._generate_backend_package_json(),
            "backend/models/User.js": self._generate_mongodb_model(),
            "backend/routes/api.js": self._generate_express_routes(),
            "backend/config/database.js": self._generate_mongodb_config(),
            "frontend/src/app.component.ts": self._generate_angular_component(),
            "frontend/src/app.component.html": self._generate_angular_template(),
            "frontend/src/app.component.css": self._generate_angular_styles(),
            "frontend/src/app.module.ts": self._generate_angular_module(),
            "frontend/src/app-routing.module.ts": self._generate_angular_routing(),
            "frontend/package.json": self._generate_angular_package_json(),
            "frontend/angular.json": self._generate_angular_config(),
            "frontend/src/index.html": self._generate_angular_index(),
            "README.md": self._generate_readme(concepts, "MEAN Stack")
        }

    def generate_lamp_code(self, concepts, project_name):
        """Generate LAMP stack code"""
        return {
            "index.php": self._generate_php_index(),
            "config/database.php": self._generate_php_database_config(),
            "models/User.php": self._generate_php_model(),
            "README.md": self._generate_readme(concepts, "LAMP Stack")
        }

    def generate_django_code(self, concepts, project_name):
        """Generate Django stack code"""
        return {
            "backend/manage.py": self._generate_django_manage(),
            "backend/settings.py": self._generate_django_settings(),
            "backend/urls.py": self._generate_django_urls(),
            "frontend/src/App.js": self._generate_react_app(),
            "README.md": self._generate_readme(concepts, "Django Stack")
        }

    def generate_spring_boot_code(self, concepts, project_name):
        """Generate Spring Boot stack code"""
        return {
            "backend/src/main/java/com/example/Application.java": self._generate_spring_boot_app(),
            "backend/pom.xml": self._generate_maven_pom(),
            "frontend/src/App.js": self._generate_react_app(),
            "README.md": self._generate_readme(concepts, "Spring Boot Stack")
        }

    def generate_laravel_code(self, concepts, project_name):
        """Generate Laravel stack code"""
        return {
            "backend/routes/web.php": self._generate_laravel_routes(),
            "backend/app/Http/Controllers/ApiController.php": self._generate_laravel_controller(),
            "frontend/src/App.vue": self._generate_vue_app(),
            "README.md": self._generate_readme(concepts, "Laravel Stack")
        }

    def generate_flask_code(self, concepts, project_name):
        """Generate Flask stack code"""
        return {
            "backend/app.py": self._generate_flask_app(),
            "backend/requirements.txt": self._generate_flask_requirements(),
            "frontend/src/App.js": self._generate_react_app(),
            "README.md": self._generate_readme(concepts, "Flask Stack")
        }

    def generate_rails_code(self, concepts, project_name):
        """Generate Ruby on Rails stack code"""
        return {
            "backend/config/routes.rb": self._generate_rails_routes(),
            "backend/app/controllers/application_controller.rb": self._generate_rails_controller(),
            "frontend/src/App.js": self._generate_react_app(),
            "README.md": self._generate_readme(concepts, "Ruby on Rails Stack")
        }

    def _generate_angular_component(self):
        """Generate Angular component"""
        return '''import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'research-app';
}'''

    def _generate_angular_package_json(self):
        """Generate Angular package.json"""
        return {
            "name": "research-app-frontend",
            "version": "1.0.0",
            "dependencies": {
                "@angular/core": "^17.0.0",
                "@angular/common": "^17.0.0",
                "@angular/router": "^17.0.0"
            }
        }

    def _generate_php_index(self):
        """Generate PHP index file"""
        return '''<?php
require_once 'config/database.php';

// Simple API endpoint
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    header('Content-Type: application/json');
    echo json_encode(['message' => 'Research App API']);
}
?>'''

    def _generate_php_database_config(self):
        """Generate PHP database config"""
        return '''<?php
$host = 'localhost';
$dbname = 'research_app';
$username = 'root';
$password = '';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}
?>'''

    def _generate_php_model(self):
        """Generate PHP model"""
        return '''<?php
class User {
    private $pdo;
    
    public function __construct($pdo) {
        $this->pdo = $pdo;
    }
    
    public function getAll() {
        $stmt = $this->pdo->query("SELECT * FROM users");
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
}
?>'''

    def _generate_django_manage(self):
        """Generate Django manage.py"""
        return '''#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "research_app.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)'''

    def _generate_django_settings(self):
        """Generate Django settings"""
        return '''import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'research_app.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'research_app',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
'''

    def _generate_django_urls(self):
        """Generate Django URLs"""
        return '''from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_view(request):
    return JsonResponse({'message': 'Research App API'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_view),
]'''

    def _generate_spring_boot_app(self):
        """Generate Spring Boot application"""
        return '''package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class Application {
    
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
    
    @GetMapping("/api")
    public String api() {
        return "Research App API";
    }
}'''

    def _generate_maven_pom(self):
        """Generate Maven pom.xml"""
        return '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>research-app</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
    
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.0.0</version>
    </parent>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
    </dependencies>
</project>'''

    def _generate_laravel_routes(self):
        """Generate Laravel routes"""
        return '''<?php
use Illuminate\\Support\\Facades\\Route;

Route::get('/api', function () {
    return response()->json(['message' => 'Research App API']);
});'''

    def _generate_laravel_controller(self):
        """Generate Laravel controller"""
        return '''<?php
namespace App\\Http\\Controllers;

use Illuminate\\Http\\Request;

class ApiController extends Controller
{
    public function index()
    {
        return response()->json(['message' => 'Research App API']);
    }
}'''

    def _generate_vue_app(self):
        """Generate Vue.js app"""
        return '''<template>
  <div id="app">
    <h1>Research App</h1>
    <p>Welcome to your research application!</p>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  text-align: center;
  margin-top: 60px;
}
</style>'''

    def _generate_flask_app(self):
        """Generate Flask app"""
        return '''from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api')
def api():
    return jsonify({'message': 'Research App API'})

if __name__ == '__main__':
    app.run(debug=True)'''

    def _generate_flask_requirements(self):
        """Generate Flask requirements"""
        return '''Flask==2.3.0
Flask-CORS==4.0.0
SQLAlchemy==2.0.0'''

    def _generate_rails_routes(self):
        """Generate Rails routes"""
        return '''Rails.application.routes.draw do
  get 'api', to: 'application#api'
end'''

    def _generate_rails_controller(self):
        """Generate Rails controller"""
        return '''class ApplicationController < ActionController::API
  def api
    render json: { message: 'Research App API' }
  end
end'''

    def _generate_mongodb_model(self):
        """Generate MongoDB model"""
        return '''const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('User', userSchema);'''

    def _generate_express_routes(self):
        """Generate Express routes"""
        return '''const express = require('express');
const router = express.Router();
const User = require('../models/User');

// GET all users
router.get('/users', async (req, res) => {
  try {
    const users = await User.find();
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// POST new user
router.post('/users', async (req, res) => {
  try {
    const user = new User(req.body);
    await user.save();
    res.status(201).json(user);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

module.exports = router;'''

    def _generate_mongodb_config(self):
        """Generate MongoDB configuration"""
        return '''const mongoose = require('mongoose');

const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/research_app', {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log('MongoDB connected successfully');
  } catch (error) {
    console.error('MongoDB connection error:', error);
    process.exit(1);
  }
};

module.exports = connectDB;'''

    def _generate_angular_template(self):
        """Generate Angular template"""
        return '''<div class="app-container">
  <header>
    <h1>{{ title }}</h1>
  </header>
  
  <main>
    <div class="content">
      <p>Welcome to your research application!</p>
      <button (click)="onButtonClick()">Get Started</button>
    </div>
  </main>
  
  <footer>
    <p>&copy; 2024 Research App</p>
  </footer>
</div>'''

    def _generate_angular_styles(self):
        """Generate Angular styles"""
        return '''.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
  text-align: center;
}

main {
  flex: 1;
  padding: 2rem;
  text-align: center;
}

.content {
  max-width: 600px;
  margin: 0 auto;
}

button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

button:hover {
  background-color: #2980b9;
}

footer {
  background-color: #34495e;
  color: white;
  padding: 1rem;
  text-align: center;
}'''

    def _generate_angular_module(self):
        """Generate Angular module"""
        return '''import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }'''

    def _generate_angular_routing(self):
        """Generate Angular routing"""
        return '''import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: AppComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }'''

    def _generate_angular_config(self):
        """Generate Angular configuration"""
        return '''{
  "$schema": "./node_modules/@angular/cli/lib/config/schema.json",
  "version": 1,
  "newProjectRoot": "projects",
  "projects": {
    "research-app": {
      "projectType": "application",
      "schematics": {},
      "root": "",
      "sourceRoot": "src",
      "prefix": "app",
      "architect": {
        "build": {
          "builder": "@angular-devkit/build-angular:browser",
          "options": {
            "outputPath": "dist/research-app",
            "index": "src/index.html",
            "main": "src/main.ts",
            "polyfills": "src/polyfills.ts",
            "tsConfig": "tsconfig.app.json",
            "assets": [
              "src/favicon.ico",
              "src/assets"
            ],
            "styles": [
              "src/styles.css"
            ],
            "scripts": []
          }
        },
        "serve": {
          "builder": "@angular-devkit/build-angular:dev-server",
          "options": {
            "buildTarget": "research-app:build"
          }
        }
      }
    }
  }
}'''

    def _generate_angular_index(self):
        """Generate Angular index.html"""
        return '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Research App</title>
  <base href="/">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" type="image/x-icon" href="favicon.ico">
</head>
<body>
  <app-root></app-root>
</body>
</html>'''

    def _generate_php_controller(self):
        """Generate PHP controller"""
        return '''<?php
class ApiController {
    private $pdo;
    
    public function __construct($pdo) {
        $this->pdo = $pdo;
    }
    
    public function getAllUsers() {
        try {
            $stmt = $this->pdo->query("SELECT * FROM users");
            $users = $stmt->fetchAll(PDO::FETCH_ASSOC);
            return json_encode($users);
        } catch (PDOException $e) {
            return json_encode(['error' => $e->getMessage()]);
        }
    }
    
    public function createUser($data) {
        try {
            $stmt = $this->pdo->prepare("INSERT INTO users (name, email) VALUES (?, ?)");
            $stmt->execute([$data['name'], $data['email']]);
            return json_encode(['success' => true, 'id' => $this->pdo->lastInsertId()]);
        } catch (PDOException $e) {
            return json_encode(['error' => $e->getMessage()]);
        }
    }
}
?>'''

    def _generate_php_layout(self):
        """Generate PHP layout"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo $title ?? 'Research App'; ?></title>
    <link rel="stylesheet" href="public/css/style.css">
</head>
<body>
    <header>
        <nav>
            <h1>Research App</h1>
        </nav>
    </header>
    
    <main>
        <?php echo $content; ?>
    </main>
    
    <footer>
        <p>&copy; 2024 Research App</p>
    </footer>
    
    <script src="public/js/app.js"></script>
</body>
</html>'''

    def _generate_php_home(self):
        """Generate PHP home page"""
        return '''<?php
$title = 'Home - Research App';
$content = '
<div class="hero">
    <h1>Welcome to Research App</h1>
    <p>Your research management solution</p>
    <button onclick="loadData()">Load Data</button>
</div>
<div id="data-container"></div>
';
include 'views/layout.php';
?>'''

    def _generate_php_styles(self):
        """Generate PHP styles"""
        return '''body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
}

header {
    background-color: #2c3e50;
    color: white;
    padding: 1rem;
}

nav h1 {
    margin: 0;
}

.hero {
    text-align: center;
    padding: 4rem 2rem;
    background-color: white;
    margin: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.hero h1 {
    color: #2c3e50;
    margin-bottom: 1rem;
}

.hero p {
    color: #7f8c8d;
    margin-bottom: 2rem;
}

button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
}

button:hover {
    background-color: #2980b9;
}

footer {
    background-color: #34495e;
    color: white;
    text-align: center;
    padding: 1rem;
    margin-top: 2rem;
}'''

    def _generate_php_javascript(self):
        """Generate PHP JavaScript"""
        return '''function loadData() {
    fetch('api.php')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('data-container');
            container.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    console.log('Research App loaded');
});'''

    def _generate_htaccess(self):
        """Generate .htaccess file"""
        return '''RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^api/(.*)$ api.php [QSA,L]

# Enable CORS
Header always set Access-Control-Allow-Origin "*"
Header always set Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS"
Header always set Access-Control-Allow-Headers "Content-Type, Authorization"'''

    def _generate_composer_json(self):
        """Generate composer.json"""
        return '''{
    "name": "research/app",
    "description": "Research Application",
    "type": "project",
    "require": {
        "php": ">=7.4"
    },
    "autoload": {
        "psr-4": {
            "App\\\\": "src/"
        }
    }
}'''

    def _generate_django_models(self):
        """Generate Django models"""
        return '''from django.db import models
from django.contrib.auth.models import User

class ResearchPaper(models.Model):
    title = models.CharField(max_length=200)
    abstract = models.TextField()
    authors = models.CharField(max_length=500)
    publication_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Keyword(models.Model):
    paper = models.ForeignKey(ResearchPaper, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100)
    
    def __str__(self):
        return self.keyword'''

    def _generate_django_views(self):
        """Generate Django views"""
        return '''from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import ResearchPaper, Keyword
import json

def api_view(request):
    return JsonResponse({'message': 'Research App API'})

@csrf_exempt
@require_http_methods(["GET", "POST"])
def papers_api(request):
    if request.method == 'GET':
        papers = ResearchPaper.objects.all()
        data = []
        for paper in papers:
            data.append({
                'id': paper.id,
                'title': paper.title,
                'abstract': paper.abstract,
                'authors': paper.authors,
                'publication_date': paper.publication_date.isoformat()
            })
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        paper = ResearchPaper.objects.create(
            title=data['title'],
            abstract=data['abstract'],
            authors=data['authors'],
            publication_date=data['publication_date']
        )
        return JsonResponse({'id': paper.id, 'message': 'Paper created'})'''

    def _generate_django_admin(self):
        """Generate Django admin"""
        return '''from django.contrib import admin
from .models import ResearchPaper, Keyword

@admin.register(ResearchPaper)
class ResearchPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'publication_date', 'created_at')
    list_filter = ('publication_date', 'created_at')
    search_fields = ('title', 'authors', 'abstract')

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'paper')
    list_filter = ('paper',)
    search_fields = ('keyword',)'''

    def _generate_django_serializers(self):
        """Generate Django serializers"""
        return '''from rest_framework import serializers
from .models import ResearchPaper, Keyword

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['id', 'keyword']

class ResearchPaperSerializer(serializers.ModelSerializer):
    keywords = KeywordSerializer(many=True, read_only=True)
    
    class Meta:
        model = ResearchPaper
        fields = ['id', 'title', 'abstract', 'authors', 'publication_date', 'created_at', 'keywords']'''

    def _generate_django_requirements(self):
        """Generate Django requirements"""
        return '''Django==4.2.0
djangorestframework==3.14.0
django-cors-headers==4.0.0
psycopg2-binary==2.9.5
python-decouple==3.8'''

    def _generate_react_index(self):
        """Generate React index.js"""
        return '''import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);'''

    def _generate_react_header(self):
        """Generate React Header component"""
        return '''import React from 'react';

const Header = () => {
  return (
    <header className="header">
      <div className="container">
        <h1>Research App</h1>
        <nav>
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/papers">Papers</a></li>
            <li><a href="/about">About</a></li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;'''

    def _generate_react_footer(self):
        """Generate React Footer component"""
        return '''import React from 'react';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <p>&copy; 2024 Research App. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;'''

    def _generate_react_package_json(self):
        """Generate React package.json"""
        return '''{
  "name": "research-app-frontend",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "axios": "^1.3.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "devDependencies": {
    "react-scripts": "5.0.1"
  }
}'''

    def _generate_react_html(self):
        """Generate React HTML"""
        return '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="Research Application" />
    <title>Research App</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>'''

    def _generate_spring_controller(self):
        """Generate Spring controller"""
        return '''package com.example.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import java.util.List;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class ApiController {
    
    @GetMapping
    public ResponseEntity<String> api() {
        return ResponseEntity.ok("Research App API");
    }
    
    @GetMapping("/users")
    public ResponseEntity<List<User>> getAllUsers() {
        // Implementation for getting all users
        return ResponseEntity.ok(List.of());
    }
    
    @PostMapping("/users")
    public ResponseEntity<User> createUser(@RequestBody User user) {
        // Implementation for creating user
        return ResponseEntity.ok(user);
    }
}'''

    def _generate_spring_model(self):
        """Generate Spring model"""
        return '''package com.example.model;

import javax.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String name;
    
    @Column(nullable = false, unique = true)
    private String email;
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    // Constructors
    public User() {}
    
    public User(String name, String email) {
        this.name = name;
        this.email = email;
        this.createdAt = LocalDateTime.now();
    }
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}'''

    def _generate_spring_repository(self):
        """Generate Spring repository"""
        return '''package com.example.repository;

import com.example.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);
}'''

    def _generate_spring_service(self):
        """Generate Spring service"""
        return '''package com.example.service;

import com.example.model.User;
import com.example.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Optional;

@Service
public class UserService {
    
    @Autowired
    private UserRepository userRepository;
    
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }
    
    public Optional<User> getUserById(Long id) {
        return userRepository.findById(id);
    }
    
    public User createUser(User user) {
        return userRepository.save(user);
    }
    
    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }
}'''

    def _generate_spring_properties(self):
        """Generate Spring properties"""
        return '''# Database Configuration
spring.datasource.url=jdbc:mysql://localhost:3306/research_app
spring.datasource.username=root
spring.datasource.password=password
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# JPA Configuration
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL8Dialect

# Server Configuration
server.port=8080

# CORS Configuration
spring.web.cors.allowed-origins=*
spring.web.cors.allowed-methods=GET,POST,PUT,DELETE,OPTIONS
spring.web.cors.allowed-headers=*'''

    def _generate_laravel_api_routes(self):
        """Generate Laravel API routes"""
        return '''<?php
use Illuminate\\Support\\Facades\\Route;
use App\\Http\\Controllers\\ApiController;

Route::prefix('api')->group(function () {
    Route::get('/', [ApiController::class, 'index']);
    Route::get('/users', [ApiController::class, 'getUsers']);
    Route::post('/users', [ApiController::class, 'createUser']);
    Route::get('/users/{id}', [ApiController::class, 'getUser']);
    Route::put('/users/{id}', [ApiController::class, 'updateUser']);
    Route::delete('/users/{id}', [ApiController::class, 'deleteUser']);
});'''

    def _generate_laravel_model(self):
        """Generate Laravel model"""
        return '''<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Factories\\HasFactory;
use Illuminate\\Database\\Eloquent\\Model;

class User extends Model
{
    use HasFactory;
    
    protected $fillable = [
        'name',
        'email',
    ];
    
    protected $casts = [
        'created_at' => 'datetime',
        'updated_at' => 'datetime',
    ];
}'''

    def _generate_laravel_middleware(self):
        """Generate Laravel CORS middleware"""
        return '''<?php
namespace App\\Http\\Middleware;

use Closure;
use Illuminate\\Http\\Request;

class Cors
{
    public function handle(Request $request, Closure $next)
    {
        return $next($request)
            ->header('Access-Control-Allow-Origin', '*')
            ->header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
            ->header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    }
}'''

    def _generate_laravel_migration(self):
        """Generate Laravel migration"""
        return '''<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('users', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('email')->unique();
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('users');
    }
};'''

    def _generate_laravel_db_config(self):
        """Generate Laravel database config"""
        return '''<?php
return [
    'default' => env('DB_CONNECTION', 'mysql'),
    'connections' => [
        'mysql' => [
            'driver' => 'mysql',
            'url' => env('DATABASE_URL'),
            'host' => env('DB_HOST', '127.0.0.1'),
            'port' => env('DB_PORT', '3306'),
            'database' => env('DB_DATABASE', 'research_app'),
            'username' => env('DB_USERNAME', 'root'),
            'password' => env('DB_PASSWORD', ''),
            'charset' => 'utf8mb4',
            'collation' => 'utf8mb4_unicode_ci',
        ],
    ],
];'''

    def _generate_laravel_composer(self):
        """Generate Laravel composer.json"""
        return '''{
    "name": "research/app",
    "type": "project",
    "description": "Research Application",
    "require": {
        "php": "^8.0.2",
        "laravel/framework": "^9.19",
        "laravel/sanctum": "^3.0"
    },
    "autoload": {
        "psr-4": {
            "App\\\\": "app/",
            "Database\\\\Factories\\\\": "database/factories/",
            "Database\\\\Seeders\\\\": "database/seeders/"
        }
    }
}'''

    def _generate_vue_main(self):
        """Generate Vue main.js"""
        return '''import { createApp } from 'vue'
import App from './App.vue'
import './style.css'

createApp(App).mount('#app')'''

    def _generate_vue_header(self):
        """Generate Vue Header component"""
        return '''<template>
  <header class="header">
    <div class="container">
      <h1>Research App</h1>
      <nav>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/papers">Papers</a></li>
          <li><a href="/about">About</a></li>
        </ul>
      </nav>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header'
}
</script>

<style scoped>
.header {
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
}

.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

nav ul {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
}

nav li {
  margin-left: 1rem;
}

nav a {
  color: white;
  text-decoration: none;
}
</style>'''

    def _generate_vue_footer(self):
        """Generate Vue Footer component"""
        return '''<template>
  <footer class="footer">
    <div class="container">
      <p>&copy; 2024 Research App. All rights reserved.</p>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
.footer {
  background-color: #34495e;
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: 2rem;
}
</style>'''

    def _generate_vue_package_json(self):
        """Generate Vue package.json"""
        return '''{
  "name": "research-app-frontend",
  "version": "1.0.0",
  "dependencies": {
    "vue": "^3.2.0",
    "vue-router": "^4.1.0",
    "axios": "^1.3.0"
  },
  "devDependencies": {
    "vite": "^4.0.0",
    "@vitejs/plugin-vue": "^4.0.0"
  }
}'''

    def _generate_vue_html(self):
        """Generate Vue HTML"""
        return '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Research App</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>'''

    def _generate_flask_models(self):
        """Generate Flask models"""
        return '''from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }'''

    def _generate_flask_routes(self):
        """Generate Flask routes"""
        return '''from flask import Blueprint, request, jsonify
from .models import User, db

api = Blueprint('api', __name__)

@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@api.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify(user.to_dict())

@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204'''

    def _generate_flask_config(self):
        """Generate Flask config"""
        return '''import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///research_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}'''

    def _generate_flask_run(self):
        """Generate Flask run.py"""
        return '''from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)'''

    def _generate_rails_api_controller(self):
        """Generate Rails API controller"""
        return '''class ApiController < ApplicationController
  def index
    render json: { message: 'Research App API' }
  end
  
  def users
    users = User.all
    render json: users
  end
  
  def create_user
    user = User.new(user_params)
    if user.save
      render json: user, status: :created
    else
      render json: { errors: user.errors }, status: :unprocessable_entity
    end
  end
  
  private
  
  def user_params
    params.require(:user).permit(:name, :email)
  end
end'''

    def _generate_rails_model(self):
        """Generate Rails model"""
        return '''class User < ApplicationRecord
  validates :name, presence: true
  validates :email, presence: true, uniqueness: true, format: { with: URI::MailTo::EMAIL_REGEXP }
  
  scope :recent, -> { order(created_at: :desc) }
  
  def to_json
    {
      id: id,
      name: name,
      email: email,
      created_at: created_at,
      updated_at: updated_at
    }
  end
end'''

    def _generate_rails_users_controller(self):
        """Generate Rails users controller"""
        return '''class UsersController < ApplicationController
  before_action :set_user, only: [:show, :update, :destroy]
  
  def index
    @users = User.all
    render json: @users
  end
  
  def show
    render json: @user
  end
  
  def create
    @user = User.new(user_params)
    if @user.save
      render json: @user, status: :created
    else
      render json: { errors: @user.errors }, status: :unprocessable_entity
    end
  end
  
  def update
    if @user.update(user_params)
      render json: @user
    else
      render json: { errors: @user.errors }, status: :unprocessable_entity
    end
  end
  
  def destroy
    @user.destroy
    head :no_content
  end
  
  private
  
  def set_user
    @user = User.find(params[:id])
  end
  
  def user_params
    params.require(:user).permit(:name, :email)
  end
end'''

    def _generate_rails_application_config(self):
        """Generate Rails application config"""
        return '''require_relative "boot"
require "rails/all"

Bundler.require(*Rails.groups)

module ResearchApp
  class Application < Rails::Application
    config.load_defaults 7.0
    config.api_only = true
    
    # CORS configuration
    config.middleware.insert_before 0, Rack::Cors do
      allow do
        origins '*'
        resource '*', headers: :any, methods: [:get, :post, :put, :patch, :delete, :options, :head]
      end
    end
  end
end'''

    def _generate_rails_database_config(self):
        """Generate Rails database config"""
        return '''default: &default
  adapter: postgresql
  encoding: unicode
  pool: <%= ENV.fetch("RAILS_MAX_THREADS") { 5 } %>

development:
  <<: *default
  database: research_app_development

test:
  <<: *default
  database: research_app_test

production:
  <<: *default
  url: <%= ENV['DATABASE_URL'] %>'''

    def _generate_rails_gemfile(self):
        """Generate Rails Gemfile"""
        return '''source "https://rubygems.org"
git_source(:github) { |repo| "https://github.com/#{repo}.git" }

ruby "3.1.0"

gem "rails", "~> 7.0.0"
gem "pg", "~> 1.1"
gem "puma", "~> 5.0"
gem "bootsnap", ">= 1.4.4", require: false

gem "rack-cors"

group :development, :test do
  gem "byebug", platforms: [:mri, :mingw, :x64_mingw]
end

group :development do
  gem "listen", "~> 3.3"
  gem "spring"
end'''

    def _generate_express_server(self):
        """Generate Express server"""
        return '''const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Database connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/research_app', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
})
.then(() => console.log('MongoDB connected successfully'))
.catch(err => console.log('MongoDB connection error:', err));

// Routes
app.get('/', (req, res) => {
    res.json({ message: 'Research Paper Application API is running!' });
});

// API routes
app.use('/api/auth', require('./routes/auth'));
app.use('/api/users', require('./routes/users'));
app.use('/api/research', require('./routes/research'));

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});'''

    def _generate_backend_package_json(self):
        """Generate backend package.json"""
        return {
            "name": "research-app-backend",
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
                "multer": "^1.4.5-lts.1",
                "pdf-parse": "^1.1.1"
            },
            "devDependencies": {
                "nodemon": "^3.0.1"
            }
        }

    def _generate_angular_package_json(self):
        """Generate Angular package.json"""
        return {
            "name": "research-app-frontend",
            "version": "1.0.0",
            "scripts": {
                "ng": "ng",
                "start": "ng serve",
                "build": "ng build",
                "watch": "ng build --watch --configuration development",
                "test": "ng test"
            },
            "dependencies": {
                "@angular/animations": "^16.0.0",
                "@angular/common": "^16.0.0",
                "@angular/compiler": "^16.0.0",
                "@angular/core": "^16.0.0",
                "@angular/forms": "^16.0.0",
                "@angular/platform-browser": "^16.0.0",
                "@angular/platform-browser-dynamic": "^16.0.0",
                "@angular/router": "^16.0.0",
                "rxjs": "~7.8.0",
                "tslib": "^2.3.0",
                "zone.js": "~0.12.0"
            },
            "devDependencies": {
                "@angular-devkit/build-angular": "^16.0.0",
                "@angular/cli": "~16.0.0",
                "@angular/compiler-cli": "^16.0.0",
                "@types/jasmine": "~4.3.0",
                "jasmine-core": "~4.6.0",
                "karma": "~6.4.0",
                "karma-chrome-launcher": "~3.1.0",
                "karma-coverage": "~2.2.0",
                "karma-jasmine": "~5.1.0",
                "karma-jasmine-html-reporter": "~2.1.0",
                "typescript": "~5.0.2"
            }
        }

    def _generate_maven_pom(self):
        """Generate Maven pom.xml"""
        return '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.1.0</version>
        <relativePath/>
    </parent>
    
    <groupId>com.example</groupId>
    <artifactId>research-app</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
    
    <name>Research App</name>
    <description>Research Application</description>
    
    <properties>
        <java.version>17</java.version>
    </properties>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <scope>runtime</scope>
        </dependency>
    </dependencies>
    
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>'''

    def _generate_flask_app(self):
        """Generate Flask app"""
        return '''from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///research_app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

# Routes
@app.route('/')
def home():
    return jsonify({'message': 'Research App API'})

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)'''

    def _generate_flask_requirements(self):
        """Generate Flask requirements"""
        return '''Flask==2.3.0
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.0.5
python-dotenv==1.0.0'''

    def _generate_laravel_routes(self):
        """Generate Laravel routes"""
        return '''<?php
use Illuminate\\Support\\Facades\\Route;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/api', function () {
    return response()->json(['message' => 'Research App API']);
});'''

    def _generate_laravel_controller(self):
        """Generate Laravel controller"""
        return '''<?php
namespace App\\Http\\Controllers;

use Illuminate\\Http\\Request;

class ApiController extends Controller
{
    public function index()
    {
        return response()->json(['message' => 'Research App API']);
    }
}'''

    def _generate_vue_app(self):
        """Generate Vue app"""
        return '''<template>
  <div id="app">
    <Header />
    <main>
      <h1>Research App</h1>
      <p>Welcome to your research application!</p>
    </main>
    <Footer />
  </div>
</template>

<script>
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    Header,
    Footer
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

main {
  padding: 2rem;
}
</style>'''

    def _generate_readme(self, concepts, technology):
        """Generate README.md"""
        return f'''# Research App - {technology}

## Overview
This is a research paper analysis application built with {technology}.

## Features
- Research paper upload and analysis
- User authentication
- Data visualization
- API endpoints for research data

## Key Concepts
- Keywords: {', '.join(concepts.get('keywords', [])[:5])}
- Technical Terms: {', '.join(concepts.get('technical_terms', [])[:5])}
- Features: {', '.join(concepts.get('features', [])[:5])}

## Installation

### Backend
1. Navigate to backend directory
2. Install dependencies: `npm install` or `pip install -r requirements.txt`
3. Set up environment variables
4. Start the server

### Frontend
1. Navigate to frontend directory
2. Install dependencies: `npm install`
3. Start the development server

## Usage
1. Upload research papers in PDF format
2. View analysis results
3. Explore generated insights

## Technology Stack
{technology}

## Contributing
Feel free to submit issues and enhancement requests.

## License
MIT License'''

    def _generate_react_app(self):
        """Generate React App component"""
        return '''import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import axios from 'axios';
import './App.css';

// Components
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import ResearchPapers from './pages/ResearchPapers';
import UploadPaper from './pages/UploadPaper';
import Login from './pages/Login';
import Register from './pages/Register';

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

export default App;'''

    def _generate_react_index(self):
        """Generate React index.js"""
        return '''import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);'''

    def _generate_react_header(self):
        """Generate React Header component"""
        return '''import React from 'react';

const Header = () => {
  return (
    <header className="header">
      <div className="container">
        <h1>Research App</h1>
        <nav>
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/papers">Papers</a></li>
            <li><a href="/about">About</a></li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;'''

    def _generate_react_footer(self):
        """Generate React Footer component"""
        return '''import React from 'react';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <p>&copy; 2024 Research App. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;'''

    def _generate_react_package_json(self):
        """Generate React package.json"""
        return '''{
  "name": "research-app-frontend",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "axios": "^1.3.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "devDependencies": {
    "react-scripts": "5.0.1"
  }
}'''

    def _generate_react_html(self):
        """Generate React HTML"""
        return '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="Research Application" />
    <title>Research App</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>'''

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
        
        # If PDF file is provided, ask for technology choice
        if pdf_file_path and os.path.exists(pdf_file_path):
            return """Please choose the technology stack you want to use:

🔧 TECHNOLOGY OPTIONS:
1. MERN Stack (MongoDB, Express.js, React.js, Node.js)
2. MEAN Stack (MongoDB, Express.js, Angular, Node.js)
3. LAMP Stack (Linux, Apache, MySQL, PHP)
4. Django Stack (Python, Django, PostgreSQL, React)
5. Spring Boot Stack (Java, Spring Boot, MySQL, React)
6. Laravel Stack (PHP, Laravel, MySQL, Vue.js)
7. Flask Stack (Python, Flask, SQLite, React)
8. Ruby on Rails Stack (Ruby, Rails, PostgreSQL, React)

Please type the number (1-8) or the name of your preferred technology stack."""
        
        # Check if user is specifying technology stack
        technology_keywords = {
            '1': 'MERN Stack', 'mern': 'MERN Stack',
            '2': 'MEAN Stack', 'mean': 'MEAN Stack', 
            '3': 'LAMP Stack', 'lamp': 'LAMP Stack',
            '4': 'Django Stack', 'django': 'Django Stack',
            '5': 'Spring Boot Stack', 'spring boot': 'Spring Boot Stack', 'spring': 'Spring Boot Stack',
            '6': 'Laravel Stack', 'laravel': 'Laravel Stack',
            '7': 'Flask Stack', 'flask': 'Flask Stack',
            '8': 'Ruby on Rails Stack', 'ruby on rails': 'Ruby on Rails Stack', 'rails': 'Ruby on Rails Stack'
        }
        
        user_choice = user_input.lower().strip()
        if user_choice in technology_keywords:
            return process_pdf_with_technology(pdf_file_path, technology_keywords[user_choice])
        
        # For any other input, ask for PDF upload
        return "Please upload your research paper in the form of PDF."
    
    except Exception as e:
        return "Please upload your research paper in the form of PDF."

def process_pdf_with_technology(pdf_path, technology):
    """
    Process a PDF file with specified technology stack and generate application
    """
    try:
        # Step 1: Extract content from PDF
        content = research_agent.extract_pdf_content(pdf_path)
        
        if content.startswith("Error"):
            return f"Error extracting PDF: {content}"
        
        # Step 2: Analyze content and generate structure
        project_structure, concepts = research_agent.analyze_content_and_generate_structure(content)
        
        # Step 3: Generate code with specified technology
        project_name = "research-app"
        generated_code = research_agent.generate_code_for_technology(concepts, project_name, technology)
        
        # Step 4: Create ZIP file in user's Downloads folder
        import os
        
        # Use user's actual Downloads folder
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        os.makedirs(downloads_folder, exist_ok=True)
        
        # Set the generated code in the research agent
        research_agent.generated_code = generated_code
        
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
        
        # Create download information
        zip_filename = os.path.basename(zip_path)
        
        response += f"""

✅ ZIP FILE CREATED SUCCESSFULLY!

📁 ZIP FILE LOCATION: {zip_path}

🔗 DOWNLOAD YOUR ZIP FILE:
The ZIP file has been created and saved to your Downloads folder.

📋 TO ACCESS YOUR ZIP FILE:
1. Open File Explorer
2. Navigate to your Downloads folder: {downloads_folder}
3. Find the file: {zip_filename}
4. Right-click and extract the ZIP file
5. Open the extracted folder
6. Run: npm install
7. Start the application

🎉 Your {technology} project is ready!

💡 TIP: The ZIP file is saved in your Downloads folder for easy access!
"""
        
        return response
    
    except Exception as e:
        return f"Error processing PDF: {str(e)}"

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
        
        # Step 4: Create ZIP file in a universal accessible location
        import os
        import tempfile
        
        # Create ZIP file in a temporary directory that's accessible to all users
        temp_dir = tempfile.gettempdir()
        zip_path = research_agent.create_zip_file(project_name, temp_dir)
        
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

✅ ZIP FILE CREATED SUCCESSFULLY!

📁 ZIP FILE LOCATION: {zip_path}

📋 TO USE THE ZIP FILE:
1. Open File Explorer
2. Navigate to: {temp_dir}
3. Find the file: {os.path.basename(zip_path)}
4. Right-click and extract the ZIP file
5. Open the extracted folder
6. Run: npm install
7. Start the application

🎉 Your MERN stack project is ready!

💡 TIP: The ZIP file is saved in your system's temporary folder, which is accessible to all users.
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

2. When user uploads a PDF, respond with technology options:
"Please choose the technology stack you want to use:

🔧 TECHNOLOGY OPTIONS:
1. MERN Stack (MongoDB, Express.js, React.js, Node.js)
2. MEAN Stack (MongoDB, Express.js, Angular, Node.js)
3. LAMP Stack (Linux, Apache, MySQL, PHP)
4. Django Stack (Python, Django, PostgreSQL, React)
5. Spring Boot Stack (Java, Spring Boot, MySQL, React)
6. Laravel Stack (PHP, Laravel, MySQL, Vue.js)
7. Flask Stack (Python, Flask, SQLite, React)
8. Ruby on Rails Stack (Ruby, Rails, PostgreSQL, React)

Please type the number (1-8) or the name of your preferred technology stack."

3. When user specifies a technology choice, automatically:
   - Extract the PDF content
   - Analyze the content to identify key concepts and features
   - Generate a complete project structure for the chosen technology
   - Create all necessary code files (backend and frontend)
   - Display the abstract and key insights from the PDF
   - Show the project structure
   - Display code implementations separately
   - Create a downloadable ZIP file with all files
   - Provide the local directory path for the ZIP file

Follow this exact conversation flow. Be conversational and helpful.
''',
)
