import './HomeScreen.css';

export default function HomeScreen({ onLogin, onSignup }) {
  return (
    <div className="home-container">
      <h1 className="title">SocioMap</h1>
      <div className="button-group">
        <button onClick={onLogin}>Login</button>
        <button onClick={onSignup}>Sign up</button>
        <button disabled>Settings</button>
      </div>
    </div>
  );
}