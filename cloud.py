"""Non-interactive cloud entry point. Secrets are runtime variables only."""
import asyncio
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from telethon import TelegramClient, events, errors
from telethon.sessions import StringSession

from card_userbot import replace_card


async def main():
    required = ('API_ID', 'API_HASH', 'CARD_NUMBER', 'CARD_HOLDER', 'TELEGRAM_SESSION')
    if any(not os.environ.get(key) for key in required):
        raise ValueError('Required runtime secrets are missing.')
    client = TelegramClient(StringSession(os.environ['TELEGRAM_SESSION']),
                            int(os.environ['API_ID']), os.environ['API_HASH'])
    card_text = os.environ['CARD_NUMBER'] + '\n' + os.environ['CARD_HOLDER']
    await client.connect()
    try:
        if not await client.is_user_authorized():
            raise ValueError('Session is not authorized. Create a session locally first.')
        owner = await client.get_me()
        if owner.bot:
            raise ValueError('A personal account session is required.')

        @client.on(events.NewMessage(outgoing=True, forwards=False, pattern=r'^/card$'))
        async def handle(event):
            try:
                await replace_card(event, owner.id, card_text)
            except errors.RPCError as error:
                print('Message edit failed:', type(error).__name__, flush=True)

        class Health(BaseHTTPRequestHandler):
            def do_GET(self):
                ready = client.is_connected()
                body = json.dumps({'status': 'ready' if ready else 'disconnected'}).encode()
                self.send_response(200 if ready else 503)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(('0.0.0.0', int(os.environ.get('PORT', '8000'))), Health)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        print('Telegram connected; card helper ready.', flush=True)
        try:
            await client.run_until_disconnected()
        finally:
            server.shutdown()
            server.server_close()
    finally:
        await client.disconnect()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (ValueError, KeyError):
        print('Cloud configuration or Telegram authorization is invalid.', flush=True)
        raise SystemExit(1)
