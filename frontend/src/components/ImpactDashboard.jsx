import React, { useState } from 'react';
import { 
  Clock, 
  CheckCircle2, 
  Trash2, 
  ArrowLeft, 
  Calendar,
  Sparkles,
  Layers
} from 'lucide-react';
import { calculateLocalImpact } from '../utils/storage';

export default function ImpactDashboard({ sessions, onStartNew, onClearHistory }) {
  const [confirmClear, setConfirmClear] = useState(false);
  const metrics = calculateLocalImpact(sessions);

  const formatDate = (isoString) => {
    if (!isoString) return 'Earlier today';
    try {
      const d = new Date(isoString);
      return d.toLocaleDateString(undefined, { 
        month: 'short', 
        day: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    } catch {
      return 'Recent';
    }
  };

  return (
    <div className="impact-layout">
      {/* Back button */}
      <div className="impact-top-nav">
        <button type="button" className="editorial-back-link" onClick={onStartNew}>
          <ArrowLeft size={16} />
          <span>Back to Planner</span>
        </button>
      </div>

      {/* Editorial Header */}
      <section className="impact-header-section">
        <span className="hero-eyebrow">Personal Reflection &bull; Client-Side Only</span>
        <h1 className="impact-main-title">Your Real-World Presence</h1>
        <p className="impact-subtext">
          An honest account of your self-reported moments away from screens. Stored exclusively in your browser with zero server telemetry, zero streaks, and zero dopamine manipulation.
        </p>
      </section>

      {/* Metric Cards Grid */}
      <div className="impact-metrics-row">
        <div className="editorial-stat-card">
          <div className="stat-card-icon">
            <Clock size={20} />
          </div>
          <span className="stat-card-number">{metrics.totalMinutes}</span>
          <span className="stat-card-unit">minutes</span>
          <span className="stat-card-label">Self-Reported Screen-Free Time</span>
        </div>

        <div className="editorial-stat-card">
          <div className="stat-card-icon">
            <CheckCircle2 size={20} />
          </div>
          <span className="stat-card-number">{metrics.completedCount}</span>
          <span className="stat-card-unit">sessions</span>
          <span className="stat-card-label">Completed Experiences</span>
        </div>

        <div className="editorial-stat-card">
          <div className="stat-card-icon">
            <Layers size={20} />
          </div>
          <span className="stat-card-number">{Object.keys(metrics.categories).length || 0}</span>
          <span className="stat-card-unit">varieties</span>
          <span className="stat-card-label">Grounding Modalities</span>
        </div>
      </div>

      {/* Philosophy Callout */}
      <div className="anti-streak-callout">
        <div className="callout-symbol">🍃</div>
        <div className="callout-body">
          <strong>Why Touch Grass AI will never track a streak:</strong>
          <p>
            Habit tracking apps often replicate the exact slot-machine dopamine loops that keep us addicted to our phones. You do not owe anyone a streak. Every single quiet minute away from a screen belongs entirely to you.
          </p>
        </div>
      </div>

      {/* History Timeline */}
      <section className="history-block">
        <div className="history-title-row">
          <h2 className="history-heading">Recent Offline History</h2>
          
          {sessions.length > 0 && (
            <div>
              {confirmClear ? (
                <div className="inline-confirm-box">
                  <span>Clear local history?</span>
                  <button 
                    type="button" 
                    className="confirm-btn-yes" 
                    onClick={() => { onClearHistory(); setConfirmClear(false); }}
                  >
                    Delete
                  </button>
                  <button 
                    type="button" 
                    className="confirm-btn-cancel" 
                    onClick={() => setConfirmClear(false)}
                  >
                    Cancel
                  </button>
                </div>
              ) : (
                <button 
                  type="button" 
                  className="clear-history-link"
                  onClick={() => setConfirmClear(true)}
                >
                  <Trash2 size={13} />
                  <span>Clear Local History</span>
                </button>
              )}
            </div>
          )}
        </div>

        {sessions.length === 0 ? (
          <div className="history-empty-state">
            <span className="empty-state-leaf">🌱</span>
            <h3 className="empty-state-title">No offline experiences logged yet</h3>
            <p className="empty-state-desc">
              Whenever you feel ready to take a breather from your displays, start your first session from the planner.
            </p>
            <button type="button" className="editorial-cta-btn empty-action" onClick={onStartNew}>
              <span>Start an Offline Check-In</span>
            </button>
          </div>
        ) : (
          <div className="history-timeline-list">
            {sessions.map((sess) => (
              <article key={sess.id} className="history-timeline-item">
                <div className="history-item-body">
                  <div className="history-item-top">
                    <h3 className="history-item-name">{sess.activityTitle}</h3>
                    <div className="history-item-duration">
                      <strong>{sess.selfReportedMinutes}</strong> mins
                    </div>
                  </div>

                  <div className="history-item-meta">
                    <span className="history-item-date">
                      <Calendar size={12} /> {formatDate(sess.recordedAt)}
                    </span>
                    <span className="history-item-category">
                      {sess.category?.replace('_', ' ')}
                    </span>
                    <span className="history-item-badge">
                      {sess.completed ? '✓ Completed' : 'Rest Break'}
                    </span>
                  </div>

                  {sess.reflectionNote && (
                    <blockquote className="history-item-reflection">
                      &ldquo;{sess.reflectionNote}&rdquo;
                    </blockquote>
                  )}
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
