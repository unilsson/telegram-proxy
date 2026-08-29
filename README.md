# Telegram Proxy Service

A small FastAPI service for sending notifications through the Telegram Bot API. It is intended for internal homelab use and keeps the Telegram bot token and chat IDs outside calling applications.

## Features

- **FastAPI backend** with a small JSON API.
- **Multiple Telegram recipients** via a comma-separated list of chat IDs.
- **Environment isolation** for Telegram credentials.
- **OpenAPI specification** generated automatically by FastAPI.
- **Swagger UI** for interactive API documentation and testing.
- Designed to run behind the internal Nginx API proxy at `api.ulnihnw.net`.

## Installation and setup

Clone the repository and enter the directory:

```bash
git clone https://github.com/unilsson/telegram-proxy.git
cd telegram-proxy
```

Create a `.env` file containing the Telegram credentials:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_IDS=123456789,987654321
```

`TELEGRAM_CHAT_IDS` may contain one or more comma-separated chat IDs.

The `.env` file must not be committed to Git. On the production server it should only be readable by the account that owns the application, for example:

```bash
chmod 600 .env
```

## API endpoint

The service exposes one application endpoint:

```text
POST /send
```

JSON body:

```json
{
  "text": "Alert: System temperature high!"
}
```

`text` is required. The same message is sent to all chat IDs configured in `TELEGRAM_CHAT_IDS`.

### Direct local test

When testing directly on the server:

```bash
curl -X POST "http://127.0.0.1:21962/send" \
  -H "Content-Type: application/json" \
  -d '{"text":"Alert: System temperature high!"}'
```

## Internal Nginx API proxy

In the homelab the service is normally accessed through the central internal Nginx API proxy rather than by its host address and port.

Internal URL:

```text
http://api.ulnihnw.net/api/telegram/
```

Nginx routes requests under `/api/telegram/` to the Telegram proxy backend.

The FastAPI application uses a `root_path` because it is exposed behind the Nginx path prefix:

```python
app = FastAPI(
    title="Telegram Proxy",
    description="Internt API för att skicka notifieringar via Telegram",
    version="1.0.0",
    root_path="/api/telegram",
)
```

This allows FastAPI-generated URLs to work correctly even though Nginx removes the `/api/telegram/` prefix before forwarding the request to the backend.

The normal API call from another machine on the LAN is therefore:

```bash
curl -X POST "http://api.ulnihnw.net/api/telegram/send" \
  -H "Content-Type: application/json" \
  -d '{"text":"Test via Nginx API proxy"}'
```

Traffic flow:

```text
Client
  |
  v
http://api.ulnihnw.net/api/telegram/send
  |
  v
Nginx :80
  |
  v
Telegram Proxy backend
  |
  v
Telegram Bot API
```

The internal API proxy is intentionally HTTP-only and is available only on the home network. It is separate from the Nginx TLS reverse-proxy configuration used for other internal services.

## OpenAPI and Swagger UI

FastAPI automatically generates both a machine-readable OpenAPI description and interactive Swagger documentation.

### Swagger UI

Open in a browser:

```text
http://api.ulnihnw.net/api/telegram/docs
```

The Swagger interface shows the available endpoints, request schemas and response types. The `POST /send` endpoint can also be tested directly from the browser using **Try it out**.

### OpenAPI specification

The generated OpenAPI document is available at:

```text
http://api.ulnihnw.net/api/telegram/openapi.json
```

This endpoint can be consumed by tools that understand OpenAPI and provides a machine-readable description of the API.

Directly on the application server the corresponding FastAPI endpoints are:

```text
http://127.0.0.1:21962/docs
http://127.0.0.1:21962/openapi.json
```

## Design principle

Clients should use the stable internal API URL:

```text
http://api.ulnihnw.net/api/telegram/...
```

rather than depending on the physical server address or application port. This allows the service to move to another host or port later without requiring changes in every client that uses it.
