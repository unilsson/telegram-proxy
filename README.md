# Telegram Proxy Service

A lightweight FastAPI microservice that relays system alerts and notifications directly to a Telegram chat using a Bot API. Designed for homelab automation and monitoring.

## Features
* **FastAPI Backend:** Lightweight and modern asynchronous framework.
* **Secure Token Management:** Uses environment variables (`.env`) for Bot Tokens and Chat IDs.
* **Production-Ready:** Configured to run locally via systemd.

## Installation & Setup

1. Clone the repository and navigate into the folder:
   ```bash
   git clone https://github.com/YOUR_USERNAME/telegram-proxy.git
   cd telegram-proxy
   ```

2. Create a `.env` file with your Telegram credentials:
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```

## API Usage

Send a POST request to `/send`:

```bash
curl -X POST "http://127.0.0.1:21962/send" \
     -H "Content-Type: application/json" \
     -d '{"text": "Alert: System temperature high!"}'