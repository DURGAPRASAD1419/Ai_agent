import React, { useState, useEffect } from 'react';
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
