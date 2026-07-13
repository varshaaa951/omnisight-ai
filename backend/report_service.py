import httpx
import json
from typing import List, Dict, Any

# Target host Ollama port (works seamlessly whether Ollama runs natively or in Docker)
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3" # Ensure you have pulled this via 'ollama pull llama3' or change to 'phi3'

async def generate_executive_summary(raw_data: List[Dict[str, Any]], user_query: str) -> str:
    """
    Takes raw analytics JSON data from a database result set and 
    uses Ollama to synthesize a 3-sentence high-impact corporate executive narrative.
    """
    if not raw_data:
        return "No operational data available for the requested parameter window."

    # Format data for clear parsing context
    data_snapshot = json.dumps(raw_data, indent=2, default=str)
    
    system_prompt = (
        "You are an expert corporate data analyst. Your job is to analyze raw database result tuples "
        "and synthesize them into an elite, executive-level narrative summary.\n"
        "Strict Guidelines:\n"
        "- Provide exactly 3 concise, impactful sentences.\n"
        "- Focus entirely on high-level business trends, key spikes, or notable drops.\n"
        "- Do NOT use technical terminology like 'SQL', 'database', 'rows', 'table', or 'query'.\n"
        "- Do NOT hallucinate data points; rely strictly on the numbers provided.\n"
        "- Output ONLY the narrative text block. Do not include conversational intros, headers, or filler notes."
    )
    
    user_prompt = f"Original User Query: {user_query}\n\nRaw Analytical Data:\n{data_snapshot}"
    
    payload = {
        "model": MODEL_NAME,
        "prompt": f"{system_prompt}\n\n{user_prompt}",
        "stream": False,
        "options": {
            "temperature": 0.1  # Keeps the model mathematically rigid and factual
        }
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            return response.json().get("response", "").strip()
    except Exception as e:
        print(f"[Ollama Error] Could not connect or retrieve inference: {e}")
        return "Executive summary generation is temporarily offline due to upstream inference engine latency."