import { useState } from 'react';
import './SignupScreen.css';

export default function SignupScreen({ onBack }) {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  const [passwordMatch, setPasswordMatch] = useState(true);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    if (name === 'password' || name === 'confirmPassword') {
      const newPassword = name === 'password' ? value : formData.password;
      const newConfirm = name === 'confirmPassword' ? value : formData.confirmPassword;
      setPasswordMatch(newPassword === newConfirm);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!passwordMatch) return;

    try {
      const response = await fetch("http://localhost:8000/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
          username: formData.username,
          first_name: formData.firstName,
          last_name: formData.lastName,
        }),
      });

      if (response.ok) {
        alert("Account created successfully!");
        onBack();
      } else {
        const data = await response.json();
        if (data.detail === "Email already registered") {
          alert("An account with that email already exists.");
        } else {
          alert("Signup failed. Please try again.");
        }
      }
    } catch (err) {
      alert("Server error. Please try again later.");
      console.error(err);
    }
  };

  return (
    <div className="signup-container">
      <h1 className="title">SocioMap</h1>
      <h2 className="subtitle">Sign up</h2>

      <form className="signup-form" onSubmit={handleSubmit}>
        <div className="column">
          <div className="form-row">
            <label>First Name</label>
            <input name="firstName" value={formData.firstName} onChange={handleChange} required />
          </div>
          <div className="form-row">
            <label>Last Name</label>
            <input name="lastName" value={formData.lastName} onChange={handleChange} required />
          </div>
          <div className="form-row">
            <label>Username</label>
            <input name="username" value={formData.username} onChange={handleChange} required />
          </div>
        </div>

        <div className="column">
          <div className="form-row">
            <label>Email</label>
            <input name="email" type="email" value={formData.email} onChange={handleChange} required />
          </div>
          <div className="form-row">
            <label>Password</label>
            <input name="password" type="password" value={formData.password} onChange={handleChange} required />
          </div>
          <div className="form-row">
            <label>Confirm Password</label>
            <input name="confirmPassword" type="password" value={formData.confirmPassword} onChange={handleChange} required />
          </div>
        </div>

        {!passwordMatch && (
          <p style={{ color: 'red', marginTop: '-0.5rem', width: '100%' }}>
            Passwords do not match
          </p>
        )}

        <div className="form-buttons">
          <button type="submit" disabled={!passwordMatch}>Create Account</button>
          <button type="button" onClick={onBack}>Back</button>
        </div>
      </form>
    </div>
  );
}