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

## Koyeb

Dockerfile orqali Web Service sifatida deploy qiling, port: `8000`, bitta instance. Free instance mavjud bo'lsa Frankfurt yoki Washington hududini tanlang. Bepul tarif kiruvchi trafik bo'lmasa 1 soatdan keyin uxlaydi: Telegram xabarlari uni uyg'otmaydi. Tashqi doimiy ishlash kafolati yo'q.

Mahalliy akkauntga kirgandan keyin ishlayotgan yordamchini to'xtating va `.venv/bin/python export_session.py` bajaring. Yaratilgan `telegram-session.secret` faylini Git'ga yuklamang. Koyeb Secrets orqali quyidagilarni kiriting va shu nomli runtime environment variables bilan bog'lang:

- `API_ID`, `API_HASH`: shaxsiy API ma'lumotlari.
- `CARD_NUMBER`, `CARD_HOLDER`: karta ma'lumotlari.
- `TELEGRAM_SESSION`: mahalliy secret fayl mazmuni; akkauntga kirish huquqini beradi.

Bulutdagi dastur kod yoki 2FA paroli so'ramaydi. Health endpoint faqat ulanish holatini qaytaradi. Koyeb va mahalliy yordamchini bir vaqtning o'zida ishlatmang. Koyeb'ga ushbu sirlarni uzatishdan oldin akkaunt egasining roziligi kerak.
