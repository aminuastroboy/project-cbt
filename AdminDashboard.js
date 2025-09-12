import React, { useEffect, useState } from 'react';

const API = "http://127.0.0.1:8000";

function AdminDashboard() {
  const [users, setUsers] = useState({});

  useEffect(()=>{
    fetch(API + "/admin/users/")
      .then(res=>res.json())
      .then(data=>setUsers(data));
  }, []);

  return (
    <div>
      <h2>Admin Dashboard</h2>
      <h3>Registered Users</h3>
      <ul>
        {Object.keys(users.users || {}).map(email=>(
          <li key={email}>{email} - {users.users[email].name}</li>
        ))}
      </ul>

      <h3>Results</h3>
      <ul>
        {Object.keys(users.results || {}).map(email=>(
          <li key={email}>{email} - Score: {users.results[email].score}</li>
        ))}
      </ul>
    </div>
  );
}

export default AdminDashboard;
