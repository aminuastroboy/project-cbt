import React, { useEffect, useState } from 'react';

const API = "http://127.0.0.1:8000";

function AdminDashboard({token}) {
  const [data, setData] = useState(null);
  const [err, setErr] = useState(null);

  useEffect(()=>{
    async function load(){
      try{
        const res = await fetch(API + '/admin/users/', {
          headers: {
            'Authorization': token ? 'Bearer ' + token : ''
          }
        });
        if(!res.ok){
          const txt = await res.text();
          setErr('Error: ' + res.status + ' ' + txt);
          return;
        }
        const j = await res.json();
        setData(j);
      }catch(e){
        setErr(String(e));
      }
    }
    load();
  }, [token]);

  if(err) return <div><h3>Admin Dashboard</h3><p style={{color:'red'}}>{err}</p></div>;
  if(!data) return <div><h3>Admin Dashboard</h3><p>Loading...</p></div>;

  return (
    <div>
      <h3>Admin Dashboard</h3>
      <h4>Registered Users</h4>
      <ul>
        {Object.keys(data.users || {}).map(email=>(
          <li key={email}>{email} - {data.users[email].name}</li>
        ))}
      </ul>
      <h4>Results</h4>
      <ul>
        {Object.keys(data.results || {}).map(email=>(
          <li key={email}>{email} - Score: {data.results[email].score}</li>
        ))}
      </ul>
    </div>
  );
}

export default AdminDashboard;
