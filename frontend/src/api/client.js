const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

export async function fetchHealth() {
  try {
    const res = await fetch(`${BACKEND_URL}/api/health`, {
      headers: { 'Content-Type': 'application/json' }
    });
    if (!res.ok) {
      throw new Error(`Server returned HTTP ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    return {
      status: 'offline',
      error: err.message,
      timestamp: new Date().toISOString()
    };
  }
}

export async function fetchRecommendations(checkInData) {
  try {
    const res = await fetch(`${BACKEND_URL}/api/recommendations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(checkInData)
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || `Server error: HTTP ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    throw err;
  }
}

export { BACKEND_URL };
