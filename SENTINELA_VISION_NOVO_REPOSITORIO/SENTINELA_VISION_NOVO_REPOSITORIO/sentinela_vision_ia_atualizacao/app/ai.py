"""Integrações opcionais. Nunca apresenta resultados gerados como diagnóstico certificado."""
import os, base64
import httpx
from fastapi import HTTPException

API_URL = "https://api.openai.com/v1/chat/completions"

def enabled():
    return bool(os.getenv("OPENAI_API_KEY"))

async def ask_ai(system: str, user: str, image: bytes | None = None, mime: str = "image/jpeg") -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise HTTPException(503, "IA externa não configurada: defina OPENAI_API_KEY no servidor")
    content = [{"type": "text", "text": user}]
    if image is not None:
        content.append({"type":"image_url", "image_url":{"url":f"data:{mime};base64,{base64.b64encode(image).decode()}"}})
    body = {"model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"), "messages": [
        {"role":"system","content":system}, {"role":"user","content":content}], "max_tokens": 900}
    try:
        async with httpx.AsyncClient(timeout=65) as client:
            response = await client.post(API_URL, json=body, headers={"Authorization":f"Bearer {key}"})
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except (httpx.HTTPError, KeyError, IndexError, TypeError) as exc:
        raise HTTPException(502, "Falha no provedor de IA; confira credenciais, acesso ao modelo e conectividade") from exc
