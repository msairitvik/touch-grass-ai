import React, { useState } from 'react';
import { CheckCircle2, Clock, X } from 'lucide-react';

export default function CompletionModal({ initialMinutes, activityTitle, category, onSave, onDismiss }) {
  const [actualMinutes, setActualMinutes] = useState(initialMinutes || 25);
  const [completionStatus, setCompletionStatus] = useState('fully');
  const [reflection, setReflection] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const finalMinutes = Math.max(1, Number(actualMinutes) || 1);
    onSave({
      activityTitle,
      category,
      selfReportedMinutes: finalMinutes,
      completed: completionStatus === 'fully' || completionStatus === 'partially',
      completionLevel: completionStatus,
      reflectionNote: reflection.trim() || null
    });
  };

  return (
    <div className="editorial-modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <div className="editorial-modal-card">
        <div className="modal-top-bar">
          <div className="modal-badge-group">
            <span className="modal-leaf-icon">🌿</span>
            <div>
              <h2 id="modal-title" className="modal-heading">Welcome Back</h2>
              <p className="modal-subheading">A calm, voluntary reflection on your offline time.</p>
            </div>
          </div>
          <button 
            type="button" 
            className="modal-dismiss-x" 
            onClick={onDismiss}
            aria-label="Close modal"
          >
            <X size={18} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="modal-form">
          {/* Question 1: Completion */}
          <div className="modal-form-group">
            <label className="modal-group-label">Did you complete the activity?</label>
            <div className="modal-choice-grid">
              <button
                type="button"
                className={`modal-choice-btn ${completionStatus === 'fully' ? 'active' : ''}`}
                onClick={() => setCompletionStatus('fully')}
              >
                <span className="choice-emoji">✨</span>
                <strong>Yes, fully</strong>
                <span>Completed steps</span>
              </button>
              <button
                type="button"
                className={`modal-choice-btn ${completionStatus === 'partially' ? 'active' : ''}`}
                onClick={() => setCompletionStatus('partially')}
              >
                <span className="choice-emoji">🌱</span>
                <strong>Partially</strong>
                <span>Did what felt right</span>
              </button>
              <button
                type="button"
                className={`modal-choice-btn ${completionStatus === 'relaxed' ? 'active' : ''}`}
                onClick={() => setCompletionStatus('relaxed')}
              >
                <span className="choice-emoji">☕</span>
                <strong>Just rested</strong>
                <span>Took an offline breath</span>
              </button>
            </div>
          </div>

          {/* Question 2: Duration */}
          <div className="modal-form-group">
            <label className="modal-group-label">
              <Clock size={16} /> Approximately how many minutes were you away from screens?
            </label>
            <div className="duration-picker-box">
              <button 
                type="button" 
                className="duration-adjust-btn"
                onClick={() => setActualMinutes(Math.max(5, actualMinutes - 5))}
                aria-label="Subtract 5 minutes"
              >
                -5
              </button>
              <input
                type="number"
                min="1"
                max="720"
                className="duration-input"
                value={actualMinutes}
                onChange={(e) => setActualMinutes(Math.max(1, parseInt(e.target.value) || 1))}
              />
              <span className="duration-unit">minutes</span>
              <button 
                type="button" 
                className="duration-adjust-btn"
                onClick={() => setActualMinutes(actualMinutes + 5)}
                aria-label="Add 5 minutes"
              >
                +5
              </button>
            </div>
            <p className="modal-hint">
              This is self-reported by you. We do not track or spy on your device background.
            </p>
          </div>

          {/* Question 3: Optional Reflection */}
          <div className="modal-form-group">
            <label className="modal-group-label">
              What did you notice in the tactile world? (Optional)
            </label>
            <input
              type="text"
              className="editorial-text-input"
              placeholder="e.g. Crisp autumn breeze, scent of damp soil, peaceful quiet street"
              value={reflection}
              onChange={(e) => setReflection(e.target.value)}
            />
          </div>

          {/* Modal Actions */}
          <div className="modal-footer-actions">
            <button type="submit" className="modal-save-btn">
              <CheckCircle2 size={18} />
              <span>Save Offline Experience</span>
            </button>
            <button type="button" className="modal-discard-btn" onClick={onDismiss}>
              Discard Without Saving
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
