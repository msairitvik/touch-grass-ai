import React, { useState, useEffect } from 'react';
import { 
  CheckCircle2, 
  X, 
  MapPin, 
  Clock, 
  ExternalLink 
} from 'lucide-react';

export default function ScreenFreeSession({ session, onComplete, onCancel }) {
  const [elapsedSeconds, setElapsedSeconds] = useState(0);

  useEffect(() => {
    const startTime = session.startedAt || Date.now();
    const updateElapsed = () => {
      const diff = Math.max(0, Math.floor((Date.now() - startTime) / 1000));
      setElapsedSeconds(diff);
    };

    updateElapsed();
    const interval = setInterval(updateElapsed, 1000);
    return () => clearInterval(interval);
  }, [session.startedAt]);

  const formatTimer = (totalSecs) => {
    const mins = Math.floor(totalSecs / 60);
    const secs = totalSecs % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  const activity = session.activity || session;
  const elapsedMinutes = Math.max(1, Math.round(elapsedSeconds / 60));

  return (
    <div className="session-fullscreen-wrapper">
      <div className="session-zen-card">
        {/* Soft pulse indicator */}
        <div className="zen-live-indicator">
          <span className="zen-pulse-dot" />
          <span>Screen-Free Session In Progress</span>
        </div>

        <h1 className="zen-activity-title">{activity.title}</h1>

        <div className="zen-meta-row">
          <span>{activity.estimated_minutes} min planned</span>
          <span>&bull;</span>
          <span>{activity.category?.replace('_', ' ')}</span>
        </div>

        {/* Clear phone-away reassurance */}
        <div className="zen-phone-prompt">
          <div className="zen-phone-icon">📴</div>
          <div className="zen-phone-text">
            <h3>Lock your phone and step away.</h3>
            <p>
              You do <strong>not</strong> need to keep this tab open or count the seconds. The physical world is waiting. When you return, click the button below to log your experience.
            </p>
          </div>
        </div>

        {/* Destination if present */}
        {activity.location_info && activity.location_info.name && (
          <div className="zen-destination-callout">
            <MapPin size={16} />
            <span>Destination: <strong>{activity.location_info.name}</strong></span>
          </div>
        )}

        {/* Action Steps */}
        <div className="zen-steps-card">
          <h2 className="zen-steps-title">Action Steps</h2>
          <ol className="zen-steps-list">
            {(activity.steps || []).map((step, idx) => (
              <li key={idx} className="zen-step-item">
                <span className="zen-step-num">{idx + 1}</span>
                <span className="zen-step-text">{step}</span>
              </li>
            ))}
          </ol>
        </div>

        {/* Elapsed Timer Counter */}
        <div className="zen-timer-wrap">
          <span className="zen-timer-label">Elapsed Offline Time</span>
          <div className="zen-timer-display">{formatTimer(elapsedSeconds)}</div>
        </div>

        {/* Action Buttons */}
        <div className="zen-actions-row">
          <button 
            type="button" 
            className="zen-complete-button"
            onClick={() => onComplete(elapsedMinutes)}
          >
            <CheckCircle2 size={18} />
            <span>I'm Back &bull; Complete Session</span>
          </button>
          
          <button 
            type="button" 
            className="zen-cancel-button"
            onClick={onCancel}
          >
            <X size={15} />
            <span>Cancel Session</span>
          </button>
        </div>
      </div>
    </div>
  );
}
