# Shaxsiy /card yordamchisi

Shaxsiy Telegram chatida o'zingiz aynan `/card` yuborsangiz, xabar sozlangan karta raqami va egasining ismiga tahrirlanadi. Boshqalarning xabarlari, guruhlar, kanallar, forwardlar va media ishlanmaydi.

## Sozlash

1. https://my.telegram.org → API development tools orqali API ID va API hash oling.
2. `config.example.json` nusxasini `config.json` deb saqlang va o'zingizning API ma'lumotlaringiz, karta raqamingiz va ismingizni kiriting.
3. macOS'da `./start.command` ni ishga tushiring. Yoki virtual muhit yarating, `pip install -r requirements.txt`, keyin `python card_userbot.py` bajaring.
4. Telefon, Telegram kirish kodi va kerak bo'lsa 2FA parolini terminalga kiriting.
5. Saved Messages ichida `/card` bilan sinang.

Kompyuter va internet ishlashi kerak. Ctrl+C bilan to'xtatiladi. Dastur o'chiq paytdagi buyruqlar qayta ishlanmaydi. Xabar avval `/card` ko'rinishida yuborilib, keyin tahrirlanadi.

## Maxfiylik

`config.json`, `.env` va `*.session*` Git'dan chiqarilgan. Session fayli akkauntga kirish huquqini beradi. Uni, API kalitlarini va shaxsiy ma'lumotlarni ulashmang yoki kodga yozmang.

Ulanishni bekor qilish: Telegram → Settings → Devices orqali dastur sessiyasini tugating.
