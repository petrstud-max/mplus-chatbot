"""
Mplus Czechia AI Chatbot — webový server.
Používá FastAPI + Groq API (cloud LLM) + znalostní bázi o Mplus Czechia.
"""

import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import uvicorn

# Groq API klíč
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("GROQ_API_KEY="):
                GROQ_API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")

if not GROQ_API_KEY:
    print("⚠️  GROQ_API_KEY není nastaven!")
    print("   Vytvořte soubor .env ve složce mplus_bot/ s obsahem:")
    print('   GROQ_API_KEY=váš_klíč_z_console.groq.com')

client = Groq(api_key=GROQ_API_KEY)

KNOWLEDGE_FILE = Path(__file__).parent / "knowledge.txt"


def get_system_prompt() -> str:
    """Načte knowledge.txt VŽDY znovu — změny se projeví okamžitě bez restartu."""
    knowledge = KNOWLEDGE_FILE.read_text(encoding="utf-8") if KNOWLEDGE_FILE.exists() else ""
    return f"""Jsi přátelský a profesionální zákaznický asistent společnosti Mplus Czechia (dříve Conectart).
Odpovídáš na otázky zákazníků o firmě Mplus Czechia, jejích službách, cenách, pobočkách a kontaktech.

DŮLEŽITÉ PRAVIDLO: Odpovídej VELMI STRUČNĚ — maximálně 2-3 krátké věty. Žádné dlouhé seznamy ani odstavce.
Pokud se zákazník ptá na detail, odpověz krátce a nabídni že můžeš upřesnit.
Odpovídej česky, přesně na základě znalostní báze. Buď milý a profesionální.
Pokud odpověď neznáš, doporuč kontaktovat Mplus Czechia přímo.

=== ZNALOSTNÍ BÁZE ===
{knowledge}
=== KONEC ZNALOSTNÍ BÁZE ===
"""


app = FastAPI(title="Mplus Czechia Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

conversations: dict[str, list] = {}


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    reply: str


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    html_file = Path(__file__).parent / "index.html"
    return HTMLResponse(html_file.read_text(encoding="utf-8"))


@app.get("/widget.js")
async def serve_widget():
    """Servíruj widget skript pro vložení na externí stránky."""
    js_file = Path(__file__).parent / "widget.js"
    return Response(
        content=js_file.read_text(encoding="utf-8"),
        media_type="application/javascript",
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if req.session_id not in conversations:
        conversations[req.session_id] = [
            {"role": "system", "content": get_system_prompt()}
        ]

    messages = conversations[req.session_id]
    messages.append({"role": "user", "content": req.message})

    if len(messages) > 21:
        messages = [messages[0]] + messages[-20:]
        conversations[req.session_id] = messages

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Omlouvám se, došlo k chybě: {e}"

    messages.append({"role": "assistant", "content": reply})
    return ChatResponse(reply=reply)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Mplus Czechia Chatbot startuje na http://localhost:{port}")
    print("   Otevřete tento odkaz v prohlížeči.")
    print("   Pro ukončení stiskněte Ctrl+C\n")
    uvicorn.run(app, host="0.0.0.0", port=port)
