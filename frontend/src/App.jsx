import React, { useState, useEffect } from 'react';
import { fetchHealth, fetchRecommendations } from './api/client';
import CheckInForm from './components/CheckInForm';
import RecommendationView from './components/RecommendationView';
import ScreenFreeSession from './components/ScreenFreeSession';
import CompletionModal from './components/CompletionModal';
import ImpactDashboard from './components/ImpactDashboard';
import { 
  getActiveSession, 
  saveActiveSession, 
  clearActiveSession, 
  getCompletedSessions, 
  addCompletedSession, 
  clearAllHistory 
} from './utils/storage';
import { 
  BarChart3, 
  Compass, 
  AlertCircle, 
  Cpu, 
  ShieldCheck, 
  Sparkles,
  ChevronDown
} from 'lucide-react';
import './App.css';

export default function App() {
  const [health, setHealth] = useState(null);
  const [loadingHealth, setLoadingHealth] = useState(true);
  
  // Views: 'home' | 'session' | 'dashboard'
  const [currentView, setCurrentView] = useState('home');

  // Recommendation & Check-in states
  const [recommendations, setRecommendations] = useState(null);
  const [loadingRecommendations, setLoadingRecommendations] = useState(false);
  const [error, setError] = useState(null);

  // Active session and completed history
  const [activeSession, setActiveSession] = useState(null);
  const [completionPrompt, setCompletionPrompt] = useState(null);
  const [sessionsHistory, setSessionsHistory] = useState([]);
  const [showTechDetails, setShowTechDetails] = useState(false);

  // Check health and resume active session or load history on mount
  useEffect(() => {
    fetchHealth().then(data => {
      setHealth(data);
      setLoadingHealth(false);
    });

    const existingActive = getActiveSession();
    if (existingActive) {
      setActiveSession(existingActive);
      setCurrentView('session');
    }

    setSessionsHistory(getCompletedSessions());
  }, []);

  const handleCheckInSubmit = async (formData) => {
    setLoadingRecommendations(true);
    setError(null);
    try {
      const data = await fetchRecommendations(formData);
      setRecommendations(data);
    } catch (err) {
      setError(err.message || 'Unable to connect to the recommendation engine. Please ensure the backend is running.');
    } finally {
      setLoadingRecommendations(false);
    }
  };

  const handleResetCheckIn = () => {
    setRecommendations(null);
    setError(null);
    setCurrentView('home');
  };

  // Start Screen-Free Session
  const handleStartSession = (activity) => {
    const sessionObj = saveActiveSession({ activity });
    setActiveSession(sessionObj);
    setCurrentView('session');
  };

  // User clicked "I'm Back" on session screen
  const handleSessionCompletePrompt = (elapsedMinutes) => {
    const activity = activeSession?.activity || activeSession;
    setCompletionPrompt({
      initialMinutes: elapsedMinutes || activity?.estimated_minutes || 25,
      activityTitle: activity?.title || 'Screen-Free Grounding',
      category: activity?.category || 'general'
    });
  };

  // User saved the completed session
  const handleSaveCompletedSession = (record) => {
    const updated = addCompletedSession(record);
    setSessionsHistory(updated);
    setActiveSession(null);
    setCompletionPrompt(null);
    setCurrentView('dashboard');
  };

  // User canceled the active session
  const handleCancelSession = () => {
    clearActiveSession();
    setActiveSession(null);
    setCurrentView('home');
  };

  const handleClearHistory = () => {
    clearAllHistory();
    setSessionsHistory([]);
  };

  const isHealthy = health && health.status === 'healthy';
  const isGemmaReady = health && health.ollama_ready;

  return (
    <div className="app-shell">
      {/* Header and Brand Navigation */}
      <header className="app-header">
        <div className="header-inner">
          <div 
            className="brand-identity" 
            onClick={() => { if (currentView !== 'session') setCurrentView('home'); }} 
            role="button"
            tabIndex={0}
            style={{ cursor: currentView !== 'session' ? 'pointer' : 'default' }}
          >
            <div className="brand-logo-mark">🌿</div>
            <div className="brand-copy">
              <span className="brand-title">Touch Grass AI</span>
              <span className="brand-tagline">Less scrolling. More living.</span>
            </div>
          </div>

          <div className="header-nav-cluster">
            {currentView !== 'session' && (
              <nav className="header-nav">
                <button 
                  type="button" 
                  className={`nav-link-btn ${currentView === 'home' ? 'active' : ''}`}
                  onClick={() => setCurrentView('home')}
                >
                  <Compass size={15} />
                  <span>Activity Planner</span>
                </button>
                <button 
                  type="button" 
                  className={`nav-link-btn ${currentView === 'dashboard' ? 'active' : ''}`}
                  onClick={() => setCurrentView('dashboard')}
                >
                  <BarChart3 size={15} />
                  <span>Impact Dashboard</span>
                  {sessionsHistory.length > 0 && (
                    <span className="nav-count-badge">{sessionsHistory.length}</span>
                  )}
                </button>
              </nav>
            )}

            {/* Unobtrusive AI & Server Indicator */}
            <div className="header-status-indicator" title={health?.ollama_model_status || 'Checking system...'}>
              <span className={`status-signal-dot ${isHealthy ? 'active' : 'offline'}`} />
              <span className="status-signal-text">
                {isGemmaReady ? 'Gemma 2B Ready' : (isHealthy ? 'Offline Engine' : 'Connecting')}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="app-main-viewport">
        {/* Error notification banner if any */}
        {error && (
          <div className="editorial-error-banner" role="alert">
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        {/* View 1: Active Screen-Free Session Screen */}
        {currentView === 'session' && activeSession && (
          <ScreenFreeSession 
            session={activeSession}
            onComplete={handleSessionCompletePrompt}
            onCancel={handleCancelSession}
          />
        )}

        {/* View 2: Impact Dashboard */}
        {currentView === 'dashboard' && (
          <ImpactDashboard 
            sessions={sessionsHistory}
            onStartNew={() => setCurrentView('home')}
            onClearHistory={handleClearHistory}
          />
        )}

        {/* View 3: Activity Planner (Form or Results) */}
        {currentView === 'home' && (
          <>
            {!recommendations ? (
              <CheckInForm 
                onSubmit={handleCheckInSubmit} 
                loading={loadingRecommendations} 
              />
            ) : (
              <RecommendationView 
                recommendations={recommendations} 
                onReset={handleResetCheckIn}
                onStartSession={handleStartSession}
              />
            )}
          </>
        )}
      </main>

      {/* Completion Modal */}
      {completionPrompt && (
        <CompletionModal 
          initialMinutes={completionPrompt.initialMinutes}
          activityTitle={completionPrompt.activityTitle}
          category={completionPrompt.category}
          onSave={handleSaveCompletedSession}
          onDismiss={() => setCompletionPrompt(null)}
        />
      )}

      {/* Refined Minimalist Footer */}
      <footer className="app-footer">
        <div className="footer-inner">
          <div className="footer-credits">
            <span>Touch Grass AI &bull; Built with local open-weight Gemma 2 &amp; OpenStreetMap</span>
            <span>Zero streaks, zero notifications, 100% private.</span>
          </div>

          <button 
            type="button" 
            className="footer-toggle-btn"
            onClick={() => setShowTechDetails(!showTechDetails)}
          >
            <span>Architecture &amp; Model Details</span>
            <ChevronDown size={14} style={{ transform: showTechDetails ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s' }} />
          </button>
        </div>

        {/* Collapsible Architecture Details for Judges/Evaluators */}
        {showTechDetails && (
          <div className="footer-tech-drawer">
            <div className="tech-details-grid">
              <div className="tech-item">
                <span className="tech-item-title"><Cpu size={14} /> AI Model</span>
                <span className="tech-item-val">{health?.gemma_model || 'gemma2:2b'} via local Ollama</span>
                <span className="tech-item-sub">{health?.ollama_model_status || 'Ollama integration active'}</span>
              </div>
              <div className="tech-item">
                <span className="tech-item-title"><ShieldCheck size={14} /> Deterministic Safety</span>
                <span className="tech-item-val">Strict Python Rules Active</span>
                <span className="tech-item-sub">Extreme heat, storms, and late-night solo overrides</span>
              </div>
              <div className="tech-item">
                <span className="tech-item-title"><Sparkles size={14} /> Storage &amp; Privacy</span>
                <span className="tech-item-val">Browser localStorage Only</span>
                <span className="tech-item-sub">No user telemetry, tracking, or remote database</span>
              </div>
            </div>
          </div>
        )}
      </footer>
    </div>
  );
}
