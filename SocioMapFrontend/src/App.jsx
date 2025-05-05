import { useState } from 'react';
import HomeScreen from './components/HomeScreen';
import SignupScreen from './components/SignupScreen';
import LoginScreen from './components/LoginScreen';
import MapScreen from './components/MapScreen';
import './App.css';

function App() {
  const [screen, setScreen] = useState('home');

  const goToHome = () => setScreen('home');
  const goToSignup = () => setScreen('signup');
  const goToLogin = () => setScreen('login');
  const goToMap = () => setScreen('map');

  return (
    <>
      {screen === 'home' && (
        <HomeScreen onLogin={goToLogin} onSignup={goToSignup} />
      )}
      {screen === 'signup' && (
        <SignupScreen onBack={goToHome} />
      )}
      {screen === 'login' && (
        <LoginScreen
          onBack={() => setScreen('home')}
          onLoginSuccess={() => setScreen('map')}
        />
      )}
      {screen === 'map' && (
        <MapScreen />
      )}
    </>
  );
}

export default App;