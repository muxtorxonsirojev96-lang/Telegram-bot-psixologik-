import telebot
import requests

TELEGRAM_BOT_TOKEN = os.getenv"8893165963:AAFC-128vT5Z4N5SplPb_bJKDpaoxLtytHs"
GEMINI_API_KEY = os.getenv"AQ.Ab8RN6I68xPnMo7pVEMebDJsF2WkGOAAhqcSEVoRzIDmiDVzqA"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

SYSTEM_PROMPT = """Siz iliq, samimiy va tushunuvchan psixologik yordam beruvchi suhbatdoshsiz. Amaliy psixologiya va islomiy qadriyatlarga (sabr, shukr, tavakkul) asoslanib maslahat berasiz.

QOIDALAR:

1. TIL: Faqat o'zbek tilida, tabiiy va jonli tilda gapiring. Rasmiy yoki sun'iy ohangda yozmang - xuddi yaqin, mehribon do'st bilan gaplashayotgandek yozing.

2. UZUNLIK: Javobingiz qisqa va samimiy bo'lsin - 3-4 jumla atrofida. Lekin jumlalar har doim TO'LIQ va tushunarli bo'lishi shart, hech qachon o'rtada kesilib qolmasin.

3. SUHBAT OQIMI:
- Avval foydalanuvchining his-tuyg'usini chin dildan tushunganingizni bildiring.
- Keyin qisqa, amaliy va samimiy maslahat yoki tasalli bering.
- Suhbatni davom ettirish uchun mavzuga oid, shaxsiy va qiziqarli savol bering.

4. USLUB: Robot yoki shablon kabi emas, balki jonli inson kabi yozing. Takrorlanma iboralardan saqlaning.

5. Ingliz tili, yulduzcha, ro'yxat belgilari yoki boshqa formatlash belgilari umuman ishlatilmasin - faqat oddiy, tabiiy matn."""

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Assalomu alaykum! Men sizga ma'naviy va psixologik qo'llab-quvvatlash beruvchi AI assistentman.\n\nO'zingizni qanday his qilayotganingiz haqida yozishingiz mumkin.")

@bot.message_handler(func=lambda m: True)
def chat(m):
    bot.send_chat_action(m.chat.id, 'typing')
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent"
    headers = {"x-goog-api-key": GEMINI_API_KEY, "Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}\n\nFoydalanuvchi: {m.text}"}]}],
        "generationConfig": {
            "maxOutputTokens": 1024,
            "temperature": 0.9,
            "thinkingConfig": {"thinkingLevel": "minimal"}
        }
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=20).json()
        print(r)
        if "candidates" in r and len(r["candidates"]) > 0:
            text = r["candidates"][0]["content"]["parts"][0]["text"].strip()
            if len(text) > 3000:
                text = text[:3000]
            bot.reply_to(m, text)
        else:
            bot.reply_to(m, "Kechirasiz, hozir javob bera olmadim. Birozdan so'ng qayta urinib ko'ring.")
    except Exception as e:
        bot.reply_to(m, "Vaqtinchalik uzilish bo'ldi, qayta urinib ko'ring.")

bot.infinity_polling()
