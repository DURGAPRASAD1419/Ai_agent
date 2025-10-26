# Performance_Appraisal_System_In_Academics_At_Professional_Institutions - Generated Web Application

## 🚀 Quick Start Guide

This application was automatically generated based on your research paper analysis. Follow these steps to get it running:

### ⚠️ IMPORTANT: Read This First!
**Before running the application, you MUST install all dependencies by running `npm install` in both the backend and frontend directories. The "Cannot find module 'jsonwebtoken'" error occurs because dependencies haven't been installed yet.**

### 🚀 Quick Fix for "Cannot find module 'jsonwebtoken'" Error:
```bash
# Step 1: Extract the ZIP file
# Step 2: Navigate to backend directory
cd backend

# Step 3: Install all dependencies
npm install

# Step 4: Navigate to frontend directory  
cd ../frontend

# Step 5: Install all dependencies
npm install

# Step 6: Go back to root and run the startup script
cd ..
```

### 📋 Prerequisites
- **Node.js** (v16 or higher) - [Download here](https://nodejs.org/)
- **MongoDB** - [Download here](https://www.mongodb.com/try/download/community)
- **Git** (optional) - [Download here](https://git-scm.com/)

### 🛠️ Installation & Setup

#### Option 1: Quick Start (Recommended)
**Windows:**
```bash
# Double-click start-windows.bat or run:
start-windows.bat
```

**Linux/Mac:**
```bash
# Make executable and run:
chmod +x start.sh
./start.sh
```

#### Option 2: Manual Setup

#### 1. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install dependencies
npm install

# Create environment file
cp .env.example .env
# Edit .env file with your MongoDB connection string

# Start the backend server
npm run dev
```
The backend will run on `http://localhost:5000`

#### 2. Frontend Setup
```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start the frontend development server
npm start
```
The frontend will run on `http://localhost:3000`

#### 3. Database Setup
1. Install MongoDB on your system
2. Start MongoDB service
3. Update the `.env` file in the backend directory with your MongoDB connection string:
   ```
   MONGODB_URI=mongodb://localhost:27017/Performance_Appraisal_System_in_Academics_at_Professional_Institutions
   JWT_SECRET=your-super-secret-jwt-key-here
   ```

### 🎯 Application Features
- Analytics & Reporting
- Admin Panel

### 🔧 Technology Stack
- **Frontend**: React.js with modern UI components
- **Backend**: Node.js with Express.js framework
- **Database**: MongoDB for data storage
- **Authentication**: JWT-based user authentication
- **Styling**: Modern CSS with responsive design

### 📡 API Endpoints
- `GET /api/research` - Get all research papers
- `POST /api/research` - Create new research paper
- `GET /api/research/:id` - Get specific research paper
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### 🗂️ Project Structure
```
Performance_Appraisal_System_in_Academics_at_Professional_Institutions/
├── backend/
│   ├── models/          # Database models
│   ├── routes/          # API routes
│   ├── middleware/      # Custom middleware
│   ├── server.js        # Main server file
│   ├── package.json     # Backend dependencies
│   ├── .env             # Environment variables
│   └── .env.example     # Environment template
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── styles/      # CSS files
│   │   └── App.js       # Main React app
│   └── package.json     # Frontend dependencies
├── start-windows.bat    # Windows startup script
├── start.sh            # Linux/Mac startup script
└── README.md           # This file
```

### 🔍 Key Concepts Extracted from Research Paper
- System
- Professor
- Assistant
- Appraisal
- Management
- Issue
- International
- Engineering
- June
- Professional

### 🚨 Troubleshooting

#### Common Issues:
1. **Module 'jsonwebtoken' not found**: Make sure you run `npm install` in the backend directory first! This installs all required dependencies including jsonwebtoken, bcryptjs, mongoose, etc.
2. **Port already in use**: Change the port in `server.js` or kill the process using the port
3. **MongoDB connection failed**: Ensure MongoDB is running and connection string is correct
4. **Dependencies not installed**: Run `npm install` in both backend and frontend directories
5. **CORS errors**: Check that backend is running on the correct port

#### Getting Help:
- Check the console for error messages
- Ensure all prerequisites are installed
- Verify MongoDB is running
- Check network connectivity

### 📝 Development Notes
- The application uses modern ES6+ JavaScript
- All components are functional React components
- Database models use Mongoose ODM
- Authentication is handled with JWT tokens
- The UI is fully responsive and mobile-friendly

### 🎉 Success!
Once both servers are running, open your browser and go to `http://localhost:3000` to see your application in action!

---
*This application was generated by the Research Paper Agent based on your uploaded research paper.*
