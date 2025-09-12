import React, { useState } from 'react';
import Verify from './Verify';
import AdminDashboard from './AdminDashboard';
import AdminLogin from './AdminLogin';

const API = "http://127.0.0.1:8000";

function App() {
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [message, setMessage] = useState("");
  const [page, setPage] = useState("home");
  const [adminToken, setAdminToken] = useState(localStorage.getItem('adminToken'));

  const register = async () => {
    const formData = new FormData();
    formData.append("email", email);
    formData.append("name", name);
    const res = await fetch(API + "/register/", {method:"POST", body: formData});
    const data = await res.json();
    setMessage(data.message);
  };

  const submitExam = async () => {
    const formData = new FormData();
    formData.append("email", email);
    formData.append("score", 5);
    const res = await fetch(API + "/exam/submit/", {method:"POST", body: formData});
    const data = await res.json();
    setMessage(data.message);
  };

  return (
    <div style={{padding:20}}>
      <h1>CBT with Biometric (Mock)</h1>
      <nav>
        <button onClick={()=>setPage('home')}>Home</button>
        <button onClick={()=>setPage('verify')}>Verify</button>
        <button onClick={()=>setPage('adminLogin')}>Admin Login</button>
        <button onClick={()=>setPage('admin')}>Admin Dashboard</button>
      </nav>

      {page === 'home' && (
        <div>
          <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} /><br/>
          <input placeholder="Name" value={name} onChange={e=>setName(e.target.value)} /><br/>
          <button onClick={register}>Register</button>
          <button onClick={submitExam}>Submit Exam</button>
          <p>{message}</p>
        </div>
      )}

      {page === 'verify' && <Verify email={email} />}

      {page === 'adminLogin' && <AdminLogin onSuccess={(token)=>{ localStorage.setItem('adminToken', token); setAdminToken(token); setPage('admin'); }} />}

      {page === 'admin' && <AdminDashboard token={adminToken} />}
    </div>
  );
}

export default App;
