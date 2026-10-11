import React, { useState } from 'react';
import { 
  ShieldCheck, 
  ShieldAlert, 
  Clock, 
  MapPin, 
  RotateCcw, 
  Smartphone, 
  ExternalLink,
  Sparkles,
  Compass,
  ArrowRight
} from 'lucide-react';

export default function RecommendationView({ recommendations, onReset, onStartSession }) {
  const [activePrimary, setActivePrimary] = useState(recommendations.primary_activity);
  const [activeBackup, setActiveBackup] = useState(recommendations.backup_activity);

  const swapActivities = () => {
    const temp = activePrimary;
    setActivePrimary(activeBackup);
    setActiveBackup(temp);
  };

  const hasSafetyRules = recommendations.applied_safety_rules && recommendations.applied_safety_rules.length > 0;

  return (
    <div className="recommendation-layout">
      {/* Top Breadcrumb & Return */}
      <div className="recommendation-top-bar">
        <button type="button" className="editorial-back-link" onClick={onReset}>
          <RotateCcw size={15} />
          <span>Adjust Check-In Preferences</span>
        </button>

        {/* Unobtrusive AI Provenance Badge */}
        <div className="ai-provenance-tag">
          {recommendations.ai_personalized ? (
            <span className="badge-ai-active">
              <Sparkles size={13} />
              <span>Personalized by Gemma 2 (2B)</span>
            </span>
          ) : (
            <span className="badge-ai-fallback" title={recommendations.ai_note}>
              <span>Deterministic Safety Engine</span>
            </span>
          )}
        </div>
      </div>

      {/* Safety Alert (Visible & Restrained) */}
      {hasSafetyRules && (
        <div className="safety-alert-editorial">
          <div className="safety-alert-badge">
            <ShieldAlert size={18} />
            <strong>Physical Safety Protection Active</strong>
          </div>
          <p className="safety-alert-text">
            Environmental rules strictly adapted this activity to ensure personal wellbeing:
          </p>
          <ul className="safety-alert-bullets">
            {recommendations.applied_safety_rules.map((rule, idx) => (
              <li key={idx}>{rule}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Hero Primary Activity Card */}
      <article className="hero-activity-card">
        <div className="card-kicker-row">
          <span className="kicker-label">Recommended Offline Experience</span>
          <div className="meta-pills-row">
            <span className="editorial-meta-pill">
              <Clock size={14} />
              <span>{activePrimary.estimated_minutes} minutes</span>
            </span>
            <span className="editorial-meta-pill category">
              {activePrimary.category.replace('_', ' ')}
            </span>
          </div>
        </div>

        <h1 className="hero-activity-title">{activePrimary.title}</h1>
        <p className="hero-activity-why">{activePrimary.why_recommended}</p>

        {/* Safety Note if present */}
        {activePrimary.safety_notes && (
          <div className="activity-inline-safety">
            <ShieldAlert size={16} />
            <span>{activePrimary.safety_notes}</span>
          </div>
        )}

        {/* Genuine OpenStreetMap Place */}
        {activePrimary.location_info && activePrimary.location_info.is_genuine_osm && (
          <div className="editorial-place-card">
            <div className="place-card-header">
              <div className="place-icon-wrap">
                <MapPin size={18} />
              </div>
              <div>
                <strong className="place-name">{activePrimary.location_info.name}</strong>
                <span className="place-tag">Verified Public Space &bull; OpenStreetMap</span>
              </div>
            </div>
            {activePrimary.location_info.address && (
              <p className="place-address">{activePrimary.location_info.address}</p>
            )}
            <p className="place-disclaimer">{activePrimary.location_info.note}</p>
            {activePrimary.location_info.osm_url && (
              <a 
                href={activePrimary.location_info.osm_url} 
                target="_blank" 
                rel="noreferrer" 
                className="place-osm-link"
              >
                <span>View on OpenStreetMap</span>
                <ExternalLink size={12} />
              </a>
            )}
          </div>
        )}

        {/* Action Steps */}
        <div className="editorial-steps-section">
          <h2 className="steps-heading">Real-World Action Plan</h2>
          <ol className="editorial-steps-list">
            {activePrimary.steps.map((step, idx) => (
              <li key={idx} className="step-item">
                <span className="step-number">{String(idx + 1).padStart(2, '0')}</span>
                <span className="step-content">{step}</span>
              </li>
            ))}
          </ol>
        </div>

        {/* Prominent Start Session Action */}
        <div className="hero-action-footer">
          <button 
            type="button" 
            className="start-session-hero-btn"
            onClick={() => onStartSession(activePrimary)}
          >
            <Smartphone size={20} />
            <span>Start Screen-Free Session (Put Phone Away)</span>
          </button>
          <p className="start-reassurance">
            A minimal screen will open. Lock your phone or place it face-down when ready.
          </p>
        </div>
      </article>

      {/* Alternative Backup Card */}
      <section className="backup-activity-card">
        <div className="backup-card-content">
          <span className="backup-eyebrow">Alternative Option</span>
          <h2 className="backup-title">{activeBackup.title}</h2>
          <p className="backup-why">{activeBackup.why_recommended}</p>
          <div className="backup-meta">
            <Clock size={13} /> {activeBackup.estimated_minutes} mins &bull; {activeBackup.category.replace('_', ' ')}
          </div>
        </div>
        <button 
          type="button" 
          className="backup-switch-btn"
          onClick={swapActivities}
        >
          <span>Switch to this experience</span>
          <ArrowRight size={14} />
        </button>
      </section>
    </div>
  );
}
