import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getAuth, signOut } from 'firebase/auth';
import '../styles/Navbar.css';
import '../styles/Profile.css';

const Navbar = ({ isAuthenticated }) => {
  const navigate = useNavigate();
  const auth = getAuth();
  const [user, setUser] = useState(null);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((user) => {
      setUser(user);
    });
    return () => unsubscribe();
  }, [auth]);

  const handleLogout = async () => {
    try {
      await signOut(auth);
      navigate('/login');
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  const handleProfileClick = () => {
    setDropdownOpen(!dropdownOpen);
  };

  const getInitial = (name) => {
    return name ? name.charAt(0).toUpperCase() : '?';
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/">EduRPG</Link>
      </div>
      <div className="navbar-menu">
        {isAuthenticated ? (
          <>
            <Link to="/dashboard" className="navbar-item">Dashboard</Link>
            <Link to="/combat" className="navbar-item">Combat</Link>
            <Link to="/guild" className="navbar-item">Guild</Link>
            <div 
              className={`profile-section ${dropdownOpen ? 'active' : ''}`}
              onClick={handleProfileClick}
            >
              <div className="profile-avatar">
                {getInitial(user?.displayName || user?.email)}
              </div>
              <span className="profile-username">
                {user?.displayName || user?.email?.split('@')[0]}
              </span>
              <div className="profile-dropdown">
                <Link to="/profile" className="dropdown-item">View Profile</Link>
                <div onClick={handleLogout} className="dropdown-item">Logout</div>
              </div>
            </div>
          </>
        ) : (
          <>
            <Link to="/login" className="navbar-item">Login</Link>
            <Link to="/register" className="navbar-item">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;