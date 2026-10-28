"""Replace the owner's outgoing /card in private chats."""
import asyncio
import getpass
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "config.json"


def credentials():
    if not CONFIG.exists():
        raise ValueError("config.example.json dan config.json yarating va to'ldiring.")
    data = json.loads(CONFIG.read_text())
    api_id = int(data["api_id"])
    api_hash = data["api_hash"]
    if api_id <= 0 or len(api_hash) != 32 or any(c not in "0123456789abcdefABCDEF" for c in api_hash):
        raise ValueError("API ID yoki API hash noto'g'ri.")
    card_number = str(data.get("card_number", "")).strip()
    card_holder = str(data.get("card_holder", "")).strip()
    if not card_number.isdigit() or not 12 <= len(card_number) <= 19 or not card_holder:
        raise ValueError("config.json ichida card_number va card_holder ni kiriting.")
    return api_id, api_hash, f"{card_number}\n{card_holder}"


async def replace_card(event, owner_id, card_text):
    # Restrict to the signed-in user's own, new, plain-text private messages.
    if (not event.is_private or not event.out or event.sender_id != owner_id
            or event.raw_text != "/card" or event.message.fwd_from
            or event.message.via_bot_id or event.message.media):
        return
    await event.edit(card_text, parse_mode=None, link_preview=False)


async def main():
    from telethon import TelegramClient, events, errors

    os.umask(0o077)
    api_id, api_hash, card_text = credentials()
    client = TelegramClient(str(ROOT / "card_account"), api_id, api_hash)
    # Telegram login code and 2FA password are entered locally, never logged.
    await client.start(
        phone=lambda: input("Telegram telefon raqamingiz (+998...): ").strip(),
        code_callback=lambda: getpass.getpass("Telegram tasdiqlash kodi: "),
        password=lambda: getpass.getpass("Telegram 2FA paroli: "),
    )
    try:
        owner = await client.get_me()
        if owner.bot:
            raise ValueError("Bot tokeni emas, shaxsiy akkaunt bilan kiring.")

        @client.on(events.NewMessage(outgoing=True, forwards=False, pattern=r"^/card$"))
        async def on_message(event):
            try:
                await replace_card(event, owner.id, card_text)
            except errors.FloodWaitError as error:
                print(f"Telegram cheklovi: {error.seconds} soniya kuting; /card almashtirilmadi.")
            except errors.RPCError as error:
                print(f"Xabar almashtirilmadi: {type(error).__name__}")

        print("Tayyor. Shaxsiy chatda /card yuboring. To'xtatish: Ctrl+C.")
        await client.run_until_disconnected()
    finally:
        await client.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("To'xtatildi.")
    except (ValueError, KeyError):
        print("Sozlamalar noto'g'ri. config.json ichidagi API ID va API hash ni tekshiring.")
        raise SystemExit(1)
