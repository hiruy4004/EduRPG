import React, { useState } from 'react';

function Guild() {
  const [activeTab, setActiveTab] = useState('quests');
  
  // Sample data (in a real app, these would come from a database)
  const quests = [
    { id: 1, title: 'Algebra Adventure', description: 'Complete 5 algebra problems', reward: '50 XP', difficulty: 'Easy' },
    { id: 2, title: 'Grammar Guardian', description: 'Identify 10 grammar mistakes', reward: '75 XP', difficulty: 'Medium' },
    { id: 3, title: 'Science Seeker', description: 'Answer 3 advanced science questions', reward: '100 XP', difficulty: 'Hard' }
  ];
  
  const guilds = [
    { id: 1, name: 'Math Masters', members: 24, focus: 'Mathematics' },
    { id: 2, name: 'Literature League', members: 18, focus: 'English & Literature' },
    { id: 3, name: 'Science Squad', members: 21, focus: 'Sciences' }
  ];
  
  return (
    <div className="guild-container">
      <h1>Study Guild Hall</h1>
      
      <div className="guild-tabs">
        <button 
          className={activeTab === 'quests' ? 'active' : ''}
          onClick={() => setActiveTab('quests')}
        >
          Available Quests
        </button>
        <button 
          className={activeTab === 'guilds' ? 'active' : ''}
          onClick={() => setActiveTab('guilds')}
        >
          Study Guilds
        </button>
      </div>
      
      {activeTab === 'quests' ? (
        <div className="quests-container">
          <h2>Available Quests</h2>
          <div className="quests-list">
            {quests.map(quest => (
              <div key={quest.id} className="quest-card">
                <h3>{quest.title}</h3>
                <p>{quest.description}</p>
                <div className="quest-details">
                  <span className="quest-reward">Reward: {quest.reward}</span>
                  <span className="quest-difficulty">Difficulty: {quest.difficulty}</span>
                </div>
                <button className="btn btn-primary">Accept Quest</button>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="guilds-container">
          <h2>Study Guilds</h2>
          <div className="guilds-list">
            {guilds.map(guild => (
              <div key={guild.id} className="guild-card">
                <h3>{guild.name}</h3>
                <p>Focus: {guild.focus}</p>
                <p>Members: {guild.members}</p>
                <button className="btn btn-primary">Join Guild</button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default Guild;