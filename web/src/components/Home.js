import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Home.css';

function Home() {
  return (
    <div className="home-container">
      <div className="hero-section">
        <h1 className="hero-title">Welcome to <span className="text-primary">EduRPG</span></h1>
        <p className="hero-subtitle">Learn and grow through interactive educational challenges!</p>
        <div className="hero-actions">
          <Link to="/combat" className="btn">Start Learning</Link>
          <Link to="/profile" className="btn btn-outline mx-2">View Profile</Link>
        </div>
      </div>
      
      <div className="dashboard-cards">
        <div className="card primary">
          <div className="card-icon">🏆</div>
          <h2>Combat Challenges</h2>
          <p>Test your knowledge in combat-style quizzes with increasing difficulty levels. Answer correctly to defeat enemies and earn experience points!</p>
          <Link to="/combat" className="btn">Start Combat</Link>
        </div>
        
        <div className="card secondary">
          <div className="card-icon">📊</div>
          <h2>Your Progress</h2>
          <p>Track your learning journey with detailed statistics. See your growth over time and identify areas for improvement.</p>
          <Link to="/profile" className="btn btn-secondary">View Profile</Link>
        </div>
        
        <div className="card warning">
          <div className="card-icon">🏅</div>
          <h2>Leaderboard</h2>
          <p>See how you rank against others in the EduRPG community. Compete for the top spot and earn special achievements!</p>
          <Link to="/leaderboard" className="btn">View Leaderboard</Link>
        </div>
      </div>
      
      <div className="features-section mt-5">
        <h2 className="text-center mb-4">Why Choose EduRPG?</h2>
        <div className="features-grid">
          <div className="feature-item">
            <div className="feature-icon">🎮</div>
            <h3>Gamified Learning</h3>
            <p>Turn studying into an adventure with our RPG-style learning system</p>
          </div>
          <div className="feature-item">
            <div className="feature-icon">📱</div>
            <h3>Learn Anywhere</h3>
            <p>Access your educational quests from any device, anytime</p>
          </div>
          <div className="feature-item">
            <div className="feature-icon">🚀</div>
            <h3>Track Progress</h3>
            <p>Watch your skills and knowledge grow in real-time</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;