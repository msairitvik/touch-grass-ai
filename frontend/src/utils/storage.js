const ACTIVE_SESSION_KEY = 'touchgrass_active_session';
const COMPLETED_SESSIONS_KEY = 'touchgrass_completed_sessions';

export function getActiveSession() {
  try {
    const raw = localStorage.getItem(ACTIVE_SESSION_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch (e) {
    console.warn('Unable to access localStorage for active session', e);
    return null;
  }
}

export function saveActiveSession(sessionData) {
  try {
    const payload = {
      ...sessionData,
      startedAt: Date.now()
    };
    localStorage.setItem(ACTIVE_SESSION_KEY, JSON.stringify(payload));
    return payload;
  } catch (e) {
    console.warn('Unable to save active session to localStorage', e);
    return sessionData;
  }
}

export function clearActiveSession() {
  try {
    localStorage.removeItem(ACTIVE_SESSION_KEY);
  } catch (e) {
    console.warn('Unable to clear active session', e);
  }
}

export function getCompletedSessions() {
  try {
    const raw = localStorage.getItem(COMPLETED_SESSIONS_KEY);
    if (!raw) return [];
    const list = JSON.parse(raw);
    return Array.isArray(list) ? list : [];
  } catch (e) {
    console.warn('Unable to retrieve completed sessions', e);
    return [];
  }
}

export function addCompletedSession(sessionRecord) {
  try {
    const existing = getCompletedSessions();
    const updated = [
      {
        ...sessionRecord,
        id: 'sess_' + Date.now(),
        recordedAt: new Date().toISOString()
      },
      ...existing
    ];
    localStorage.setItem(COMPLETED_SESSIONS_KEY, JSON.stringify(updated));
    clearActiveSession();
    return updated;
  } catch (e) {
    console.warn('Unable to save completed session', e);
    return [];
  }
}

export function clearAllHistory() {
  try {
    localStorage.removeItem(COMPLETED_SESSIONS_KEY);
    localStorage.removeItem(ACTIVE_SESSION_KEY);
  } catch (e) {
    console.warn('Unable to reset history', e);
  }
}

export function calculateLocalImpact(sessions) {
  const totalMinutes = sessions.reduce((acc, curr) => acc + (Number(curr.selfReportedMinutes) || 0), 0);
  const completed = sessions.filter(s => s.completed);

  const categories = {};
  sessions.forEach(s => {
    const cat = s.category || 'general';
    categories[cat] = (categories[cat] || 0) + 1;
  });

  return {
    totalMinutes,
    completedCount: completed.length,
    totalAttempted: sessions.length,
    categories
  };
}
