import React, { useState } from 'react';
import { 
  Clock, 
  Users, 
  CloudSun, 
  Compass, 
  MapPin, 
  ShieldAlert, 
  ShieldCheck,
  ArrowRight,
  Sparkles,
  Leaf,
  Smartphone,
  Eye
} from 'lucide-react';

const MOODS = [
  { id: 'stressed', title: 'Stressed & Overstimulated', subtitle: 'Screen fatigue, sensory overload, racing thoughts', icon: '⚡' },
  { id: 'restless', title: 'Restless & Energetic', subtitle: 'Built-up physical energy needing real kinetic release', icon: '🏃' },
  { id: 'bored', title: 'Sluggish & Bored', subtitle: 'Numb doomscrolling, craving genuine novel texture', icon: '🪫' },
  { id: 'curious', title: 'Curious & Exploratory', subtitle: 'Open to discovering unseen details in your area', icon: '🔍' },
  { id: 'calm', title: 'Calm & Reflective', subtitle: 'Seeking gentle presence, quiet breathing, and open sky', icon: '🍃' }
];

const TIME_OPTIONS = [15, 30, 45, 60, 90, 120];

const SOCIAL_OPTIONS = [
  { id: 'alone', label: 'Just Me (Solo)', icon: '🧘' },
  { id: 'with_friend', label: 'With a Friend', icon: '👥' },
  { id: 'group', label: 'Small Group', icon: '🏕️' }
];

const WEATHER_OPTIONS = [
  { id: 'pleasant', label: 'Pleasant & Mild', icon: '🌤️' },
  { id: 'extreme_heat', label: 'Extreme Heat (>35°C / 95°F)', icon: '🔥' },
  { id: 'stormy', label: 'Stormy / Heavy Rain', icon: '⛈️' },
  { id: 'chilly', label: 'Cool / Overcast', icon: '🧣' }
];

const TIME_OF_DAY_OPTIONS = [
  { id: 'morning', label: 'Morning' },
  { id: 'afternoon', label: 'Afternoon' },
  { id: 'evening', label: 'Evening' },
  { id: 'late_night', label: 'Late Night' }
];

const INTEREST_OPTIONS = [
  'Walking & Nature',
  'Physical Movement',
  'Tactile Paper & Sketching',
  'Quiet Reading & Books',
  'Botanical Observation',
  'Mindful Tea & Senses'
];

export default function CheckInForm({ onSubmit, loading }) {
  const [mood, setMood] = useState('stressed');
  const [freeTime, setFreeTime] = useState(30);
  const [social, setSocial] = useState('alone');
  const [weather, setWeather] = useState('pleasant');
  const [timeOfDay, setTimeOfDay] = useState('afternoon');
  const [interests, setInterests] = useState(['Walking & Nature']);
  const [location, setLocation] = useState('');

  const toggleInterest = (interest) => {
    if (interests.includes(interest)) {
      setInterests(interests.filter(i => i !== interest));
    } else {
      setInterests([...interests, interest]);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      mood,
      free_time_minutes: freeTime,
      social_context: social,
      interests,
      weather_condition: weather,
      time_of_day: timeOfDay,
      location: location.trim() ? location.trim() : null
    });
  };

  return (
    <div className="checkin-container-wide">
      {/* Editorial Hero Banner */}
      <section className="editorial-hero">
        <span className="hero-eyebrow">Digital Wellbeing &bull; Real-World Grounding</span>
        <h1 className="hero-headline">
          Step away from the screen. <br />
          <span className="hero-serif-accent">Rediscover the tactile world.</span>
        </h1>
        <p className="hero-subhead">
          Tell us how you arrive right now. We tailor a single, grounded offline experience with real places, strict physical safety, and instructions to put your phone away.
        </p>
      </section>

      {/* Two-Column Desktop Grid Layout */}
      <div className="checkin-columns-grid">
        {/* Left Column: The Main Form */}
        <div className="checkin-form-column">
          <form className="editorial-form-card" onSubmit={handleSubmit}>
            {/* Section 1: Mood */}
            <div className="form-section">
              <div className="section-header">
                <span className="section-step">01</span>
                <div>
                  <h2 className="section-heading">How are you feeling right now?</h2>
                  <p className="section-subtext">Select the emotional state you wish to reset or nurture.</p>
                </div>
              </div>

              <div className="mood-cards-grid">
                {MOODS.map(m => (
                  <button
                    type="button"
                    key={m.id}
                    className={`editorial-mood-card ${mood === m.id ? 'active' : ''}`}
                    onClick={() => setMood(m.id)}
                  >
                    <div className="mood-card-top">
                      <span className="mood-card-emoji">{m.icon}</span>
                      <div className="selection-radio-indicator" />
                    </div>
                    <strong className="mood-card-title">{m.title}</strong>
                    <p className="mood-card-desc">{m.subtitle}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Section 2: Time & Company */}
            <div className="form-section">
              <div className="section-header">
                <span className="section-step">02</span>
                <div>
                  <h2 className="section-heading">Time & Company</h2>
                  <p className="section-subtext">How long can you unplug, and who is with you?</p>
                </div>
              </div>

              <div className="two-col-grid">
                {/* Time */}
                <div className="field-block">
                  <label className="field-label">
                    <Clock size={16} /> Available Screen-Free Time
                  </label>
                  <div className="pill-group">
                    {TIME_OPTIONS.map(mins => (
                      <button
                        type="button"
                        key={mins}
                        className={`segmented-pill ${freeTime === mins ? 'active' : ''}`}
                        onClick={() => setFreeTime(mins)}
                      >
                        {mins} mins
                      </button>
                    ))}
                  </div>
                </div>

                {/* Company */}
                <div className="field-block">
                  <label className="field-label">
                    <Users size={16} /> Who are you with?
                  </label>
                  <div className="pill-group">
                    {SOCIAL_OPTIONS.map(s => (
                      <button
                        type="button"
                        key={s.id}
                        className={`segmented-pill ${social === s.id ? 'active' : ''}`}
                        onClick={() => setSocial(s.id)}
                      >
                        <span style={{ marginRight: '6px' }}>{s.icon}</span>
                        {s.label}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Section 3: Weather & Time of Day */}
            <div className="form-section">
              <div className="section-header">
                <span className="section-step">03</span>
                <div>
                  <h2 className="section-heading">Context & Safety</h2>
                  <p className="section-subtext">Environmental conditions determine our non-negotiable safety rules.</p>
                </div>
              </div>

              <div className="two-col-grid">
                {/* Weather */}
                <div className="field-block">
                  <label className="field-label">
                    <CloudSun size={16} /> Outside Conditions
                  </label>
                  <div className="pill-group wrap">
                    {WEATHER_OPTIONS.map(w => (
                      <button
                        type="button"
                        key={w.id}
                        className={`segmented-pill ${weather === w.id ? 'active' : ''}`}
                        onClick={() => setWeather(w.id)}
                      >
                        <span style={{ marginRight: '6px' }}>{w.icon}</span>
                        {w.label}
                      </button>
                    ))}
                  </div>
                  {weather === 'extreme_heat' && (
                    <div className="safety-warning-banner">
                      <ShieldAlert size={16} />
                      <span>Extreme heat detected: Outdoor sports will be automatically blocked to prevent heat exhaustion. Cool indoor spaces enforced.</span>
                    </div>
                  )}
                  {weather === 'stormy' && (
                    <div className="safety-warning-banner">
                      <ShieldAlert size={16} />
                      <span>Severe weather detected: Open outdoor spaces and water bodies will be blocked. Sheltered indoor sanctuaries enforced.</span>
                    </div>
                  )}
                </div>

                {/* Time of day */}
                <div className="field-block">
                  <label className="field-label">
                    <Compass size={16} /> Time of Day
                  </label>
                  <div className="pill-group">
                    {TIME_OF_DAY_OPTIONS.map(t => (
                      <button
                        type="button"
                        key={t.id}
                        className={`segmented-pill ${timeOfDay === t.id ? 'active' : ''}`}
                        onClick={() => setTimeOfDay(t.id)}
                      >
                        {t.label}
                      </button>
                    ))}
                  </div>
                  {timeOfDay === 'late_night' && social === 'alone' && (
                    <div className="safety-warning-banner">
                      <ShieldAlert size={16} />
                      <span>Late-night solo safety: Isolated outdoor night walks are blocked. Restful home wind-down or morning plan enforced.</span>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Section 4: Offline Interests */}
            <div className="form-section">
              <div className="section-header">
                <span className="section-step">04</span>
                <div>
                  <h2 className="section-heading">Tactile Interests</h2>
                  <p className="section-subtext">What kind of real-world engagement calls to you today?</p>
                </div>
              </div>

              <div className="tags-flex">
                {INTEREST_OPTIONS.map(tag => (
                  <button
                    type="button"
                    key={tag}
                    className={`tag-toggle ${interests.includes(tag) ? 'active' : ''}`}
                    onClick={() => toggleInterest(tag)}
                  >
                    {tag}
                  </button>
                ))}
              </div>
            </div>

            {/* Section 5: Real Location (Optional) */}
            <div className="form-section">
              <div className="section-header">
                <span className="section-step">05</span>
                <div>
                  <h2 className="section-heading">Location (Optional)</h2>
                  <p className="section-subtext">Ground recommendations in genuine public spaces from OpenStreetMap.</p>
                </div>
              </div>

              <div className="location-input-wrap">
                <div className="input-with-icon">
                  <MapPin size={18} className="field-icon" />
                  <input
                    type="text"
                    className="editorial-text-input"
                    placeholder="e.g. Brooklyn, Seattle, Indiranagar, Oxford (Leave empty if staying home)"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                  />
                </div>
                <p className="field-helper-text">
                  We query real public parks and libraries via OpenStreetMap. We never invent fake live events, opening hours, or crowd sizes.
                </p>
              </div>
            </div>

            {/* Primary CTA */}
            <div className="form-submit-footer">
              <button 
                type="submit" 
                className="editorial-cta-btn" 
                disabled={loading}
              >
                {loading ? (
                  <span className="btn-loading-state">
                    <Sparkles size={18} className="spin-slow" />
                    <span>Crafting Your Grounded Experience...</span>
                  </span>
                ) : (
                  <>
                    <span>Find Your Offline Experience</span>
                    <ArrowRight size={20} />
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Right Column: Visually Rich Companion Sidebar Panel */}
        <aside className="checkin-sidebar-column">
          {/* Card 1: How Touch Grass AI Works */}
          <div className="sidebar-guide-card">
            <div className="sidebar-card-header">
              <Leaf size={20} className="sidebar-icon-leaf" />
              <h3>The Offline Journey</h3>
            </div>
            <p className="sidebar-intro">
              Unlike generic apps that try to keep your attention on a screen, Touch Grass AI is built to return your presence to the physical world.
            </p>

            <div className="journey-timeline">
              <div className="journey-step">
                <span className="journey-bullet">1</span>
                <div>
                  <strong>Check In Honestly</strong>
                  <p>Share your current emotional state. No judgment, just grounding.</p>
                </div>
              </div>

              <div className="journey-step">
                <span className="journey-bullet">2</span>
                <div>
                  <strong>Gemma AI &amp; Real Earth</strong>
                  <p>Local Gemma 2 tailors tactile nuance; genuine OpenStreetMap links provide real public locations.</p>
                </div>
              </div>

              <div className="journey-step">
                <span className="journey-bullet">3</span>
                <div>
                  <strong>Put Your Phone Away</strong>
                  <p>Step away into nature, analog books, or physical craft with zero notification anxiety.</p>
                </div>
              </div>
            </div>
          </div>

          {/* Card 2: Physical Safety Promise */}
          <div className="sidebar-safety-card">
            <div className="sidebar-card-header">
              <ShieldCheck size={20} className="sidebar-icon-shield" />
              <h3>Deterministic Safety Guarantee</h3>
            </div>
            <p className="sidebar-safety-desc">
              Your physical safety is never left to AI hallucination. Strict Python rules intercept unsafe conditions:
            </p>
            <ul className="safety-guarantee-list">
              <li>
                <strong>Extreme Heat:</strong> Direct-sun cardio blocked. Cool indoor spaces enforced.
              </li>
              <li>
                <strong>Severe Storms:</strong> Open water and parks blocked. Sheltered offline sanctuaries enforced.
              </li>
              <li>
                <strong>Late-Night Solo:</strong> Solitary night walks blocked. Peaceful home wind-down enforced.
              </li>
            </ul>
          </div>

          {/* Card 3: 5-4-3-2-1 Sensory Reset Tip */}
          <div className="sidebar-anchor-card">
            <div className="sidebar-card-header">
              <Eye size={18} className="sidebar-icon-eye" />
              <h3>Sensory Grounding Practice</h3>
            </div>
            <p className="sidebar-anchor-text">
              Whenever you feel screen fatigue, pause and notice:
            </p>
            <div className="anchor-counts">
              <span><strong>5</strong> colors in foliage</span>
              <span><strong>4</strong> physical textures</span>
              <span><strong>3</strong> ambient sounds</span>
              <span><strong>2</strong> natural scents</span>
              <span><strong>1</strong> slow deep breath</span>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}
