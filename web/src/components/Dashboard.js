import React from 'react';
import { Link } from 'react-router-dom';

function Dashboard() {
  return (
    <div className="dashboard-container">
      <h1>Your Adventure Dashboard</h1>
      <div className="dashboard">
        <div className="dashboard-card">
          <h2>Combat Arena</h2>
          <p>Test your knowledge in educational battles</p>
          <Link to="/combat" className="btn btn-primary">Enter Arena</Link>
        </div>
        <div className="dashboard-card">
          <h2>Study Guild</h2>
          <p>Join study groups and take on quests</p>
          <Link to="/guild" className="btn btn-primary">Visit Guild</Link>
        </div>
        <div className="dashboard-card">
          <h2>Your Profile</h2>
          <p>View your stats and achievements</p>
          <Link to="/profile" className="btn btn-primary">View Profile</Link>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;