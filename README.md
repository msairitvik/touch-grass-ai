# 🌿 Touch Grass AI

> **An AI-powered companion that helps people spend less time on screens and more time experiencing the tactile, physical world.**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-green.svg)](https://fastapi.tiangolo.com/)
[![React + Vite](https://img.shields.io/badge/React-Vite-purple.svg)](https://vitejs.dev/)
[![Ollama Gemma 2](https://img.shields.io/badge/AI-Gemma%202%20(2B)-orange.svg)](https://ollama.com/library/gemma2)
[![OpenStreetMap](https://img.shields.io/badge/Places-OpenStreetMap-brightgreen.svg)](https://www.openstreetmap.org/)
[![No Streaks](https://img.shields.io/badge/Design-Anti--Manipulation-teal.svg)](#privacy--anti-manipulation-philosophy)

---

## 📖 The Problem & Purpose

Most wellness and habit apps suffer from an ironic paradox: **to help you spend less time on your phone, they try to keep you addicted to their app.** They employ dopamine-driven streak counters, push notifications, badges, and endless algorithmic feeds that perpetuate the very digital anxiety they claim to cure.

**Touch Grass AI is intentionally designed to get you off your phone as fast as possible.**

Instead of being a generic AI activity generator, it is a calm, context-aware bridge between your emotional state and the physical world:
1. **Quick Check-In**: Arrive as you are (stressed, restless, bored, curious, calm) with your available minutes and companions.
2. **Deterministic Safety Rules in Python**: Non-negotiable safety guardrails that **never allow an AI prompt or hallucination** to recommend outdoor sports during extreme heat waves, outdoor visits during storms, or solitary walks during late-night hours.
3. **Open-Weight Gemma AI Personalization**: Google's open-weight `gemma2:2b` model personalizes one primary activity and one alternative, grounding them in sensory, screen-free action steps.
4. **Genuine OpenStreetMap Discovery**: Real public parks and libraries discovered on-demand without inventing fake live events, opening hours, or venue safety.
5. **One-Tap "Screen-Free Session"**: A minimal, distraction-free interface telling you to lock your phone and put it facedown. You do not need to keep the app open.
6. **Voluntary Check-In & Honest Impact Dashboard**: Self-reported screen-free minutes and tactile reflections stored locally in your browser. **No streaks, no leaderboards, no guilt.**

---

## 🏗️ System Architecture

```
[ User Browser ]
       │
       ▼
[ React + Vite Frontend ] (Earthy, tactile design system)
       │  • localStorage persistence (Zero central database)
       │  • Distraction-free session timer & completion check-in
       │  • Transparent fallback indicators
       │
       ▼ HTTP / REST
[ FastAPI Backend ]
       │
       ├─► [ Deterministic Safety Engine (Python) ]
       │     • Extreme heat protection (>35°C / 95°F)
       │     • Storm / severe weather protection
       │     • Late-night solo outing safety (10 PM - 5 AM)
       │     • STRICT OVERRIDE: Runs after AI to guarantee physical safety
       │
       ├─► [ Open-Weight Gemma 2 (Local Ollama / Hosted) ]
       │     • gemma2:2b structured JSON inference via Ollama
       │     • Transparent graceful fallback if model is uninstalled/offline
       │
       └─► [ OpenStreetMap Nominatim ]
             • Real public parks, libraries, and nature reserves
             • Queried only when location is provided; never invents fake events
```

---

## 🤖 Open-Weight AI: Gemma 2 (2B)

### Why Google's Gemma 2?
- **Open-Weight Transparency**: Openly accessible weights that can run completely on-device without telemetry or corporate surveillance.
- **Compact & High Quality**: The `2B` parameter variant (`gemma2:2b`) delivers nuanced reasoning with only **~1.63 GB** of disk space and ~2.5 GB of RAM/VRAM, making it ideal for standard consumer laptops.
- **Complete Offline Privacy**: In local mode, your mood, interests, and free time never leave your machine.

### Model Verification & Fallback Logic
The app **never fakes AI inference**. The backend verifies model readiness via Ollama (`http://localhost:11434/api/tags`):
- **When `gemma2:2b` is active**: The UI displays the badge `✨ Personalized by Gemma 2 (2B)` and the API response returns:
  ```json
  "ai_personalized": true,
  "engine": "Gemma 2 2B (Local Ollama)",
  "ai_status": "active_gemma_local",
  "ai_note": "Personalized by Gemma 2 (2B) via local Ollama in 28.5s."
  ```
- **When `gemma2:2b` is unavailable or times out**: The backend automatically serves verified activities from the deterministic safety engine and marks the response:
  ```json
  "ai_personalized": false,
  "engine": "Deterministic Safety Engine",
  "ai_status": "fallback_timeout | fallback_model_missing",
  "ai_note": "Served with verified deterministic engine."
  ```

### How to Verify Live Gemma Inference vs Fallback
1. **In the UI**:
   - When Gemma generates the activity, a badge reading `✨ Personalized by Gemma 2 (2B)` appears directly on the recommendation card.
   - If running in fallback mode, the badge reads `Deterministic Safety Engine`.
2. **In the Backend Terminal / Logs**:
   - The backend logs:
     `Calling Ollama model 'gemma2:2b' (timeout: 45.0s)...`
     `Gemma inference succeeded in 28.5s!`
3. **In the API Response / Browser DevTools**:
   - Check the network tab response for `POST /api/recommendations`:
     `ai_personalized: true`
     `engine: "Gemma 2 2B (Local Ollama)"`
     `ai_status: "active_gemma_local"`

---

## 🛡️ Deterministic Safety Architecture

Real-world safety must never rely on probabilistic large language models. The Python safety engine enforces non-negotiable rules:

| Condition | Detected Risk | Deterministic Python Enforcement |
|---|---|---|
| **Extreme Heat** (`extreme_heat`, `>35°C`) | Heat exhaustion & dehydration | **Strenuous outdoor sports & direct sun blocked.** Enforces indoor air-conditioned cool spaces, shaded rest, and mandatory hydration notes. |
| **Severe Storm** (`stormy`, thunderstorms) | Falling branches, lightning, flash floods | **Open parks and water bodies blocked.** Enforces safe, sheltered indoor offline pastimes (listening to rain, analog sketching, tea ritual). |
| **Late-Night Solo** (`late_night`, 10 PM–5 AM + Solo) | Solitary vulnerability in dark/isolated areas | **Isolated outdoor night walks blocked.** Enforces peaceful home wind-down (stretching, physical journaling, herbal tea) or packing a bag for a morning walk. |

> **Safety Invariant**: Even if Gemma produces a suggestion like *"Go for an outdoor midday run"* during extreme heat, `enforce_deterministic_safety()` intercepts and sanitizes the output before it ever reaches the user.

---

## 🌍 Real Places: Genuine OpenStreetMap Data

- **When location is provided** (e.g., *"Brooklyn"* or *"Indiranagar"*): The backend queries the OpenStreetMap Nominatim API for genuine public spaces (`amenity=library`, `leisure=park`, `leisure=nature_reserve`) and returns direct links to OpenStreetMap.
- **When no location is provided**: The app remains place-agnostic, recommending tactile activities you can do around your home, balcony, or immediate street without making network requests.
- **Absolute Honesty Guarantee**: The app never hallucinates opening hours, live attendance, ticket prices, or venue safety. Explicit disclaimers instruct users to verify daylight and hours independently.

---

## 🔕 Privacy & Anti-Manipulation Philosophy

1. **No Dopamine Streaks**: No consecutive day counters or fire emojis. Missing a day is not a failure.
2. **No Push Notifications**: We will never ping your device to *"bring you back"*. You decide when to step outside.
3. **No Central Database**: Completed sessions and screen-free minutes are stored solely in your browser's `localStorage`.
4. **Self-Reported Transparency**: Minutes are explicitly labeled as *"self-reported"*, recognizing user honesty without intrusive background app tracking.
5. **Full User Autonomy**: A one-click *"Clear Local History"* button immediately purges all saved sessions.

---

## 🚀 Quickstart: Running on Windows 11

### Prerequisites
- **Python 3.10+** (tested on Python 3.14)
- **Node.js 18+** and **npm**
- **Ollama** (optional, for local Gemma inference)

### 1. Download Gemma 2 (Optional, for local AI)
If you have Ollama installed, run:
```powershell
ollama pull gemma2:2b
```
*(Requires ~1.63 GB of disk space. If skipped, the app automatically runs in verified deterministic fallback mode.)*

### 2. Start the FastAPI Backend
Open a terminal:
```powershell
cd "c:\Users\Sai Ritvik\OneDrive\Desktop\touchgrass\backend"
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```
Verify at [http://localhost:8000/api/health](http://localhost:8000/api/health).

### 3. Start the React Frontend
Open a second terminal:
```powershell
cd "c:\Users\Sai Ritvik\OneDrive\Desktop\touchgrass\frontend"
npm.cmd run dev
```
Open your browser at [http://localhost:5173](http://localhost:5173).

---

## 🧪 Automated Testing

The backend includes a comprehensive automated test suite with **20 passing tests**:
```powershell
cd "c:\Users\Sai Ritvik\OneDrive\Desktop\touchgrass\backend"
.\venv\Scripts\pytest -v
```

### Tested Scenarios:
- `test_gemma_personalization_success`: Mocked Ollama JSON response validating AI integration.
- `test_gemma_failure_fallback_to_deterministic`: Graceful degradation when Ollama is unreachable.
- `test_gemma_cannot_override_extreme_heat`: Proves deterministic safety blocks outdoor sports even if AI suggests them.
- `test_gemma_cannot_override_late_night_solo`: Proves isolated night walks are blocked even if AI suggests them.
- `test_extreme_heat_deterministic_safety`: Outdoor sports sanitized to indoor cool spaces.
- `test_stormy_weather_deterministic_safety`: Outdoor spaces sanitized to indoor sheltered sanctuaries.
- `test_late_night_solo_deterministic_safety`: Solitary late-night outings sanitized to home wind-down.
- `test_pleasant_weather_with_friend`: Normal daytime paired recommendations.
- `test_location_absent_does_not_call_osm`: Place-agnostic behavior when location is omitted.
- `test_validate_valid_session`: Valid session duration and notes recording.
- `test_validate_negative_duration_raises_error`: Negative duration rejection.
- `test_validate_empty_title_raises_error`: Empty title validation.
- `test_validate_excessive_duration_clamping`: Clamping durations >24h.
- `test_calculate_impact_metrics_aggregation`: Accurate non-manipulative impact calculations.
- `test_missing_required_mood`: HTTP 422 validation on missing fields.
- `test_invalid_negative_duration`: HTTP 422 validation on durations < 10 mins.
- `test_options_cors_preflight`: Safe CORS preflight negotiation.

### Frontend Production Build:
```powershell
cd "c:\Users\Sai Ritvik\OneDrive\Desktop\touchgrass\frontend"
npm.cmd run build
```
*(Transpiled and bundled in ~1.5s with zero errors).*

---

## ☁️ Deployment Guide (Render)

The project includes an infrastructure blueprint ([`render.yaml`](./render.yaml)) configured for Render's free tier.

### Render Blueprint Configuration
```yaml
services:
  # 1. FastAPI Backend Web Service
  - type: web
    name: touchgrass-backend
    runtime: python
    rootDir: backend
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PORT
        value: 10000
      - key: PYTHON_VERSION
        value: 3.11.9
      - key: CORS_ORIGINS
        value: "*"
      - key: AI_INFERENCE_PROVIDER
        value: fallback
      - key: PLACES_MODE
        value: osm

  # 2. React Frontend Static Site
  - type: web
    name: touchgrass-frontend
    runtime: static
    rootDir: frontend
    buildCommand: npm install && npm run build
    staticPublishPath: dist
    routes:
      - type: rewrite
        source: /*
        destination: /index.html
    envVars:
      - key: VITE_BACKEND_URL
        fromService:
          name: touchgrass-backend
          type: web
          property: host
```

### Deploying to Render Manually:
1. Push repository to GitHub.
2. In the Render Dashboard, click **New + > Blueprint** and select your repository.
3. Render will deploy the Python Web Service and the React Static Site automatically.
4. On cloud Render without local GPU, the backend operates in **transparent deterministic fallback mode** by default, guaranteeing 100% uptime and speed. (Optional: To enable cloud Gemma, set `AI_INFERENCE_PROVIDER=hosted`, `HOSTED_API_BASE_URL`, and `HOSTED_API_KEY` for an OpenAI-compatible Gemma endpoint such as OpenRouter or Groq).

---

## 🎬 2-Minute Hackathon Demo Script

1. **The Hook (15s)**:
   > *"Every wellness app today uses streaks, notifications, and screen time to keep you looking at your phone. We built Touch Grass AI with the opposite goal: to get you off your screen as fast as possible."*

2. **The Check-In (30s)**:
   > *"A user checks in feeling 'Stressed & Overstimulated' with 30 minutes free. Notice the weather options: if we select 'Extreme Heat', our deterministic Python safety engine immediately warns us that outdoor sports will be blocked."*

3. **Deterministic Safety & Gemma (30s)**:
   > *"We submit the check-in. The local Gemma 2 2B model personalizes the activity nuance, but our non-negotiable Python safety rules ensure physical protection. Instead of baking in the sun, it gives us a cool-space library exploration with genuine OpenStreetMap links."*

4. **Screen-Free Mode (30s)**:
   > *"We tap 'Start Screen-Free Session'. The UI strips away all clutter and reminds us: 'Lock your phone. You don't need to keep this tab open.' We go live in the real world."*

5. **Impact Dashboard & Wrap-Up (15s)**:
   > *"When we return, a voluntary check-in asks for our self-reported minutes and sensory reflections. In our Impact Dashboard: no streaks, no guilt, no tracking. Just honest presence in the real world."*

---

## 🔒 Limitations & Ethical Considerations

- **Self-Reported Nature**: The app intentionally avoids invasive device screen-time APIs or location tracking to respect user privacy. Screen-free minutes are self-reported.
- **Daylight & Venue Changes**: OpenStreetMap provides genuine public parks and libraries, but real-time municipal hours, holiday closures, and daylight must always be verified by the user.
- **Not a Medical Crisis Tool**: Touch Grass AI is designed for digital wellbeing and stress grounding; it is not a substitute for clinical psychological or psychiatric care.

---

## 📄 License

MIT License. Crafted for digital wellness and real-world presence.
