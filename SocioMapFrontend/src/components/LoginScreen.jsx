import { useState } from 'react';
import './LoginScreen.css';

export default function LoginScreen({ onBack, onLoginSuccess }) {
  const [formData, setFormData] = useState({
    identifier: '',
    password: '',
  });

  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {

      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email_or_username: formData.identifier,
          password: formData.password
        })
      });

      if (response.ok) {
        onLoginSuccess(); // send user to "map screen coming soon"
      } else {
        setError('Incorrect credentials');
      }
    } catch (err) {
      console.error(err);
      setError('Server error. Please try again.');
    }
  };

  return (
    <div className="login-container">
      <h1 className="title">SocioMap</h1>
      <h2 className="subtitle">Login</h2>

      <form className="login-form" onSubmit={handleSubmit}>
        <div className="form-row">
          <label>Email / Username</label>
          <input
            name="identifier"
            value={formData.identifier}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-row">
          <label>Password</label>
          <input
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        {error && <p style={{ color: 'red' }}>{error}</p>}

        <div className="form-buttons">
          <button type="submit">Log In</button>
          <button type="button" onClick={onBack}>Back</button>
        </div>
      </form>
    </div>
  );
}