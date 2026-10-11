import json
import logging
import time
from typing import Optional, Dict, Any, Tuple
import httpx
from app.config import settings
from app.models.schemas import CheckInRequest, Activity

logger = logging.getLogger("touchgrass.gemma")

async def is_ollama_model_ready(base_url: str, model_name: str) -> Tuple[bool, str]:
    """
    Checks if Ollama is responsive and if the requested Gemma model is downloaded.
    Returns (is_ready, reason_message).
    """
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f"{base_url.rstrip('/')}/api/tags")
            if resp.status_code != 200:
                return False, f"Ollama HTTP {resp.status_code}"
            
            data = resp.json()
            models = data.get("models", [])
            installed_names = [m.get("name", "") for m in models]
            
            # Match model name or model name prefix (e.g. gemma2:2b or gemma2:2b-instruct)
            target = model_name.lower().strip()
            for name in installed_names:
                n_lower = name.lower()
                if n_lower == target or n_lower.startswith(f"{target}:") or f":{target}" in n_lower:
                    return True, f"Gemma model '{model_name}' is installed and active."

            return False, f"Model '{model_name}' is not installed in Ollama. (Installed: {', '.join(installed_names) or 'none'})"
    except httpx.ConnectError:
        return False, "Ollama service is not reachable on localhost:11434"
    except Exception as e:
        return False, f"Ollama health check error: {str(e)}"

def build_gemma_prompt(request: CheckInRequest, primary_base: Activity, backup_base: Activity, applied_rules: list) -> str:
    """
    Constructs a grounded, safety-constrained prompt for Gemma 2.
    """
    safety_context = "\n".join([f"- {r}" for r in applied_rules]) if applied_rules else "Safe and mild conditions."
    interests_str = ", ".join(request.interests) if request.interests else "general outdoor tactile exploration"

    prompt = f"""You are Touch Grass AI, an assistant that helps people unplug from screens into the physical world.
Personalize two tactile offline activities for this user context:

Context:
- Mood: {request.mood}
- Time: {request.free_time_minutes} minutes
- Social: {request.social_context}
- Interests: {interests_str}
- Weather: {request.weather_condition}
- Time of Day: {request.time_of_day or 'daytime'}

Non-Negotiable Safety Rules:
{safety_context}

Baseline Activities:
Primary candidate: {primary_base.title} ({primary_base.category})
Backup candidate: {backup_base.title} ({backup_base.category})

Instructions:
1. Make titles inviting, tactile, and screen-free (no photos, no apps).
2. Write a warm 1-2 sentence 'why_recommended' explaining how it grounds their mood.
3. Provide 3-4 physical steps to step away from screens.
4. If extreme heat: indoor cool spaces only. If storms: indoor sheltered only. If late-night solo: safe home wind-down only.

Output ONLY a valid JSON object matching this schema:
{{
  "primary": {{
    "title": "Tactile title",
    "why_recommended": "Why this grounds you...",
    "steps": ["Step 1", "Step 2", "Step 3"]
  }},
  "backup": {{
    "title": "Alternative title",
    "why_recommended": "Why this grounds you...",
    "steps": ["Step 1", "Step 2", "Step 3"]
  }}
}}"""
    return prompt

async def personalize_with_gemma(
    request: CheckInRequest, 
    primary_base: Activity, 
    backup_base: Activity, 
    applied_rules: list
) -> Tuple[Optional[Dict[str, Any]], str, str]:
    """
    Invokes the local Gemma model via Ollama to personalize activities.
    Returns (result_dict, status_code, status_note).
    Ensures adequate timeout for local CPU/GPU execution without hanging.
    """
    base_url = settings.OLLAMA_BASE_URL.rstrip('/')
    model_name = settings.GEMMA_MODEL
    timeout_secs = settings.OLLAMA_TIMEOUT

    # 1. Quick check if model is ready
    ready, reason = await is_ollama_model_ready(base_url, model_name)
    if not ready:
        logger.info(f"Ollama/Gemma not ready: {reason}")
        return None, "fallback_model_missing", reason

    prompt = build_gemma_prompt(request, primary_base, backup_base, applied_rules)

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.3,
            "top_p": 0.9,
            "num_predict": 280
        }
    }

    t0 = time.time()
    logger.info(f"Calling Ollama model '{model_name}' (timeout: {timeout_secs}s)...")

    try:
        async with httpx.AsyncClient(timeout=timeout_secs) as client:
            resp = await client.post(f"{base_url}/api/generate", json=payload)
            elapsed = time.time() - t0

            if resp.status_code != 200:
                logger.warning(f"Ollama generate returned status {resp.status_code}")
                return None, "fallback_ollama_error", f"Ollama HTTP {resp.status_code}"

            result = resp.json()
            raw_text = result.get("response", "").strip()
            if not raw_text:
                return None, "fallback_empty_response", "Ollama returned an empty response string."

            data = json.loads(raw_text)

            # Strict schema validation
            if not isinstance(data, dict) or "primary" not in data or "backup" not in data:
                return None, "fallback_invalid_schema", "Output missing 'primary' or 'backup' keys."
            
            p = data["primary"]
            b = data["backup"]
            if not isinstance(p, dict) or not isinstance(b, dict):
                return None, "fallback_invalid_schema", "Primary or backup is not an object."
            if not p.get("title") or not p.get("why_recommended") or not isinstance(p.get("steps"), list):
                return None, "fallback_invalid_schema", "Primary missing title, why_recommended, or steps list."
            if not b.get("title") or not b.get("why_recommended") or not isinstance(b.get("steps"), list):
                return None, "fallback_invalid_schema", "Backup missing title, why_recommended, or steps list."

            logger.info(f"Gemma inference succeeded in {elapsed:.2f}s!")
            return data, "active_gemma_local", f"Personalized by Gemma 2 (2B) via local Ollama in {elapsed:.1f}s."

    except httpx.TimeoutException:
        logger.warning(f"Gemma inference timed out after {timeout_secs}s. Falling back to deterministic engine.")
        return None, "fallback_timeout", f"Local Gemma 2 (2B) took longer than {int(timeout_secs)}s to generate. Served with deterministic safety engine."
    except json.JSONDecodeError as jde:
        logger.warning(f"Gemma output could not be parsed as JSON: {jde}")
        return None, "fallback_invalid_json", "Model output was not valid JSON; safely fell back to deterministic engine."
    except Exception as e:
        logger.warning(f"Gemma inference exception: {str(e)}")
        return None, "fallback_exception", f"Inference error ({str(e)}); safely fell back to deterministic engine."
