"""Create an ignored local secret file; never print the session."""
import asyncio
import os

from telethon import TelegramClient
from telethon.sessions import StringSession

from card_userbot import ROOT, credentials


async def main():
    os.umask(0o077)
    api_id, api_hash, _ = credentials()
    client = TelegramClient(str(ROOT / 'card_account'), api_id, api_hash)
    await client.connect()
    try:
        if not await client.is_user_authorized():
            print('Avval start.command orqali akkauntingizga kiring.')
            return
        target = ROOT / 'telegram-session.secret'
        with target.open('w', opener=lambda p, f: os.open(p, f, 0o600)) as file:
            file.write(StringSession.save(client.session))
        os.chmod(target, 0o600)
        print('Sessiya telegram-session.secret fayliga saqlandi. Uni Git yoki chatga yubormang.')
    finally:
        await client.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
