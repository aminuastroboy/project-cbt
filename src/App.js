import React, { useState } from 'react';
import Webcam from 'react-webcam';

function App() {
  const [page, setPage] = useState('home');
  const [users, setUsers] = useState(() => JSON.parse(localStorage.getItem('users') || '[]'));
  const [currentUser, setCurrentUser] = useState(null);
  const [admin, setAdmin] = useState(false);
  const [examScore, setExamScore] = useState(null);

  const webcamRef = React.useRef(null);

  const saveUsers = (data) => {
    setUsers(data);
    localStorage.setItem('users', JSON.stringify(data));
  };

  const registerUser = (name) => {
    const screenshot = webcamRef.current.getScreenshot();
    const newUser = { name, face: screenshot, results: [] };
    const updated = [...users, newUser];
    saveUsers(updated);
    alert('Registered successfully!');
    setPage('home');
  };

  const verifyUser = (name) => {
    const screenshot = webcamRef.current.getScreenshot();
    const user = users.find(u => u.name === name);
    if (user && user.face === screenshot) {
      setCurrentUser(user);
      setPage('exam');
    } else {
      alert('Verification failed');
    }
  };

  const takeExam = () => {
    const score = Math.floor(Math.random() * 100);
    setExamScore(score);
    const updated = users.map(u => u.name === currentUser.name ? { ...u, results: [...u.results, score] } : u);
    saveUsers(updated);
  };

  const loginAdmin = (user, pass) => {
    if (user === 'admin' && pass === 'admin123') {
      setAdmin(true);
      setPage('dashboard');
    } else alert('Invalid admin credentials');
  };

  return (
    <div className="container">
      {page === 'home' && (
        <>
          <h2>Welcome to CBT</h2>
          <button onClick={() => setPage('register')}>Register</button>
          <button onClick={() => setPage('verify')}>Login & Verify</button>
          <button onClick={() => setPage('admin')}>Admin</button>
        </>
      )}

      {page === 'register' && (
        <>
          <h2>Register</h2>
          <Webcam ref={webcamRef} screenshotFormat="image/jpeg" />
          <input type="text" placeholder="Enter Name" id="regName" />
          <button onClick={() => registerUser(document.getElementById('regName').value)}>Register</button>
          <button onClick={() => setPage('home')}>Back</button>
        </>
      )}

      {page === 'verify' && (
        <>
          <h2>Verify</h2>
          <Webcam ref={webcamRef} screenshotFormat="image/jpeg" />
          <input type="text" placeholder="Enter Name" id="verName" />
          <button onClick={() => verifyUser(document.getElementById('verName').value)}>Verify</button>
          <button onClick={() => setPage('home')}>Back</button>
        </>
      )}

      {page === 'exam' && (
        <>
          <h2>Exam Page</h2>
          <p>Hello {currentUser?.name}, ready?</p>
          <button onClick={takeExam}>Submit Exam</button>
          {examScore !== null && <p>Your Score: {examScore}</p>}
          <button onClick={() => setPage('home')}>Back</button>
        </>
      )}

      {page === 'admin' && (
        <>
          <h2>Admin Login</h2>
          <input type="text" placeholder="Username" id="adminUser" />
          <input type="password" placeholder="Password" id="adminPass" />
          <button onClick={() => loginAdmin(document.getElementById('adminUser').value, document.getElementById('adminPass').value)}>Login</button>
          <button onClick={() => setPage('home')}>Back</button>
        </>
      )}

      {page === 'dashboard' && admin && (
        <>
          <h2>Admin Dashboard</h2>
          <ul>
            {users.map((u, i) => (
              <li key={i}>{u.name} - Results: {u.results.join(', ')}</li>
            ))}
          </ul>
          <button onClick={() => setPage('home')}>Back</button>
        </>
      )}
    </div>
  );
}

export default App;
