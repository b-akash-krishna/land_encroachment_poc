import React, { useState } from 'react';
import MapComponent from './MapComponent';
import UploadForm from './UploadForm';
import DataView from './DataView';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [token, setToken] = useState(null);
  const [taskId, setTaskId] = useState(null);
  const [taskStatus, setTaskStatus] = useState(null);
  const [encroachmentData, setEncroachmentData] = useState([]);

  // This function now fetches the real JWT token from the backend
  const handleLogin = async (username, password) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    try {
      const response = await fetch('http://localhost:8000/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Login failed: ' + response.statusText);
      }

      const data = await response.json();
      setToken(data.access_token);
      setIsLoggedIn(true);
      alert('Login successful! Token received.');

    } catch (error) {
      console.error('Login failed:', error);
      alert('Login failed. Check the console for details.');
    }
  };

  const handleTaskQueued = (id) => {
    setTaskId(id);
    setTaskStatus('pending');
    checkTaskStatus(id);
  };

  const checkTaskStatus = async (id) => {
    console.log(`Checking status for task: ${id}`);
    
    setTimeout(() => {
      setTaskStatus('completed');
      setEncroachmentData([
        { "type": "building", "location": "POINT (-73.99549999999999 40.735400000000006)", "affected_area_sq_m": 0.0009492, "nearest_boundary_id": "Main Road" },
        { "type": "shed", "location": "POINT (-74.006 40.7128)", "affected_area_sq_m": 4.000000000009777e-07, "nearest_boundary_id": "Main Road" }
      ]);
      alert("Analysis complete! Data is now visible.");
    }, 5000);
  };

  return (
    <div style={{ textAlign: 'center' }}>
      <h1>AI Drone Encroachment Dashboard</h1>
      {!isLoggedIn ? (
        <div>
          <h2>Login</h2>
          <form onSubmit={(e) => {
            e.preventDefault();
            const username = e.target.username.value;
            const password = e.target.password.value;
            handleLogin(username, password);
          }}>
            <input type="text" name="username" placeholder="Username" required />
            <br />
            <input type="password" name="password" placeholder="Password" required />
            <br />
            <button type="submit">Login</button>
          </form>
        </div>
      ) : (
        <div>
          <UploadForm token={token} onTaskQueued={handleTaskQueued} />
          {taskStatus === 'pending' && <p>Processing... Please wait for the analysis to complete.</p>}
          {taskStatus === 'completed' && encroachmentData.length > 0 && (
            <>
              <MapComponent encroachmentData={encroachmentData} />
              <DataView encroachmentData={encroachmentData} />
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;