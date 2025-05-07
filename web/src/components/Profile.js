import React from 'react';
import { useNavigate } from 'react-router-dom';
import { signOut } from 'firebase/auth';
import { auth } from '../firebase';

function Profile() {
  const navigate = useNavigate();
  
  // Sample user data (in a real app, this would come from Firebase)
  const userData = {
    username: 'LearningHero',
    level: 5,
    xp: 350,
    xpToNextLevel: 500,
    subjects: {
      math: 75,
      english: 60,
      science: 45
    },
    achievements: [
      { id: 1, name: 'First Victory', description: 'Win your first combat' },
      { id: 2, name: 'Guild Member', description: 'Join a study guild' }
    ]
  };
  
  const handleLogout = async () => {
    try {
      await signOut(auth);
      navigate('/');
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };
  
  return (
    <div className="profile-container">
      <h1>Your Profile</h1>
      
      <div className="profile-header">
        <div className="profile-avatar">👤</div>
        <div className="profile-info">
          <h2>{userData.username}</h2>
          <p>Level {userData.level}</p>
          <div className="xp-bar">
            <div 
              className="xp-progress" 
              style={{ width: `${(userData.xp / userData.xpToNextLevel) * 100}%` }}
            ></div>
            <span>{userData.xp} / {userData.xpToNextLevel} XP</span>
          </div>
        </div>
      </div>
      
      <div className="profile-sections">
        <div className="profile-section">
          <h3>Subject Mastery</h3>
          <div className="subject-bars">
            {Object.entries(userData.subjects).map(([subject, mastery]) => (
              <div key={subject} className="subject-bar">
                <span className="subject-name">{subject.charAt(0).toUpperCase() + subject.slice(1)}</span>
                <div className="mastery-bar">
                  <div 
                    className="mastery-progress" 
                    style={{ width: `${mastery}%` }}
                  ></div>
                  <span>{mastery}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
        
        <div className="profile-section">
          <h3>Achievements</h3>
          <div className="achievements-list">
            {userData.achievements.map(achievement => (
              <div key={achievement.id} className="achievement-card">
                <h4>{achievement.name}</h4>
                <p>{achievement.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      <button onClick={handleLogout} className="btn btn-secondary">Logout</button>
    </div>
  );
}

export default Profile;