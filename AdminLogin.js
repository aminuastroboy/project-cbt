import React, { useState } from 'react';
const API = "http://127.0.0.1:8000";

function AdminLogin({onSuccess}) {
  const [user, setUser] = useState('');
  const [pass, setPass] = useState('');
  const [msg, setMsg] = useState('');

  const login = async () => {
    const form = new FormData();
    form.append('username', user);
    form.append('password', pass);
    const res = await fetch(API + '/admin/login', {method:'POST', body: form});
    const j = await res.json();
    if(j.status === 'success'){
      setMsg('Login successful');
      onSuccess(j.token);
    } else {
      setMsg(j.message || 'Login failed');
    }
  };

  return (
    <div>
      <h2>Admin Login</h2>
      <input placeholder="Username" value={user} onChange={e=>setUser(e.target.value)} /><br/>
      <input placeholder="Password" type="password" value={pass} onChange={e=>setPass(e.target.value)} /><br/>
      <button onClick={login}>Login</button>
      <p>{msg}</p>
    </div>
  );
}

export default AdminLogin;
