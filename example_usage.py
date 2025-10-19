#!/usr/bin/env python3
"""
Example usage of the Research Paper Agent
This demonstrates how to use the agent to process a PDF and generate a MERN stack application
"""

from agent import research_agent
import os

def main():
    """Example usage of the research paper agent"""
    
    # Example PDF path (replace with your actual PDF path)
    pdf_path = "sample_research_paper.pdf"
    
    print("Research Paper Agent - MERN Stack Generator")
    print("=" * 50)
    
    # Step 1: Extract content from PDF
    print("\nStep 1: Extracting content from PDF...")
    if os.path.exists(pdf_path):
        content = research_agent.extract_pdf_content(pdf_path)
        print(f"Content extracted successfully! ({len(content)} characters)")
    else:
        print("PDF file not found. Using sample content for demonstration...")
        content = """
        This is a sample research paper about machine learning applications in healthcare.
        The paper discusses user authentication systems, dashboard analytics, and admin management.
        It covers database design, API development, and modern web technologies.
        The research focuses on creating scalable applications with React frontend and Node.js backend.
        """
    
    # Step 2: Analyze content and generate project structure
    print("\nStep 2: Analyzing content and generating project structure...")
    project_structure, concepts = research_agent.analyze_content_and_generate_structure(content)
    
    print("Extracted Concepts:")
    print(f"   - Keywords: {concepts['keywords'][:5]}...")
    print(f"   - Technical Terms: {concepts['technical_terms']}")
    print(f"   - Features: {concepts['features']}")
    print(f"   - Content Length: {concepts['content_length']} characters")
    
    # Step 3: Generate MERN stack code
    print("\nStep 3: Generating MERN stack code...")
    generated_code = research_agent.generate_mern_code(concepts, "research-app")
    print(f"Generated {len(generated_code)} code files")
    
    # Step 4: Display code structure
    print("\nGenerated Project Structure:")
    for file_path in generated_code.keys():
        print(f"   - {file_path}")
    
    # Step 5: Create ZIP file
    print("\nStep 5: Creating downloadable ZIP file...")
    download_path = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_path, exist_ok=True)
    
    zip_path = research_agent.create_zip_file("research-app", download_path)
    
    if zip_path.startswith("Error"):
        print(f"Error: {zip_path}")
    else:
        print(f"ZIP file created successfully!")
        print(f"Download path: {zip_path}")
        print(f"File size: {os.path.getsize(zip_path)} bytes")
    
    # Step 6: Display sample code content
    print("\nSample Generated Code:")
    print("=" * 30)
    
    # Show backend server.js
    if 'backend/server.js' in generated_code:
        print("\nBackend Server (server.js):")
        print("-" * 25)
        server_code = generated_code['backend/server.js']
        print(server_code[:500] + "..." if len(server_code) > 500 else server_code)
    
    # Show frontend App.js
    if 'frontend/src/App.js' in generated_code:
        print("\nFrontend App (App.js):")
        print("-" * 20)
        app_code = generated_code['frontend/src/App.js']
        print(app_code[:500] + "..." if len(app_code) > 500 else app_code)
    
    print("\nProcess completed successfully!")
    print(f"Your MERN stack project is ready at: {zip_path}")
    print("\nNext Steps:")
    print("1. Extract the ZIP file")
    print("2. Install dependencies: npm install (in both backend and frontend folders)")
    print("3. Set up MongoDB database")
    print("4. Update .env file with your configuration")
    print("5. Start backend: npm run dev (in backend folder)")
    print("6. Start frontend: npm start (in frontend folder)")

if __name__ == "__main__":
    main()
