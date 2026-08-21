import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# Läs in ID:n, dela upp vid komma och ta bort eventuella mellanslag
chat_ids_raw = os.getenv("TELEGRAM_CHAT_IDS", "")
TELEGRAM_CHAT_IDS = [cid.strip() for cid in chat_ids_raw.split(",") if cid.strip()]

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_IDS:
    raise RuntimeError("Telegram-inställningar eller chatt-ID:n saknas i .env-filen!")

app = FastAPI()

class Message(BaseModel):
    text: str

@app.post("/send")
def send_to_telegram(msg: Message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    failed_sends = []
    
    # Skicka samma meddelande till alla mottagare i listan
    for chat_id in TELEGRAM_CHAT_IDS:
        payload = {
            "chat_id": chat_id,
            "text": msg.text,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            failed_sends.append(chat_id)
            
    if failed_sends:
        raise HTTPException(
            status_code=500, 
            detail=f"Kunde inte skicka till följande chat_ids: {failed_sends}"
        )
        
    return {"status": "skickat till alla mottagare"}
