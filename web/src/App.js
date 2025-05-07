import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// Components
import Navbar from './components/Navbar';
import Home from './components/Home';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import Combat from './components/Combat';
import Guild from './components/Guild';
import Profile from './components/Profile';

// Firebase
import { auth } from './firebase';
import { onAuthStateChanged } from 'firebase/auth';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading EduRPG...</p>
      </div>
    );
  }

  return (
    <Router>
      <div className="App">
        <Navbar isAuthenticated={!!user} />
        <div className="container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route 
              path="/dashboard" 
              element={user ? <Dashboard user={user} /> : <Login />} 
            />
            <Route 
              path="/combat" 
              element={user ? <Combat user={user} /> : <Login />} 
            />
            <Route 
              path="/guild" 
              element={user ? <Guild user={user} /> : <Login />} 
            />
            <Route 
              path="/profile" 
              element={user ? <Profile user={user} /> : <Login />} 
            />
          </Routes>
        </div>
        <footer className="footer">
          <p>&copy; {new Date().getFullYear()} EduRPG - Educational Role-Playing Game</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;