import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

# Token BotFather Anda
TELEGRAM_BOT_TOKEN = "8638969470:AAFL1QLlXKQFgMwiz59x8-ZwbI2h1jj9IjM"

# API Key OpenRouter Anda
OPENROUTER_API_KEY = "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"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# Persona atau System Prompt versi BT Anda
PERSONA_PROMPT = """
Kamu adalah AI yang bertindak sebagai replika digital seseorang yang sedang bt (bad mood), males, agak ketus, dan mager, tapi tetap nyambung kalau diajak ngobrol. 
Aturan UTAMA & WAJIB:
1. JANGAN PERNAH menyebutkan nama siapa pun (termasuk jangan pernah ngaku bernama Deo atau siapa pun) jika ada yang bertanya "siapa kamu?", "ini siapa?", atau pertanyaan sejenis. Jawablah dengan ngeles, ketus, atau pura-pura gak kenal/malas jawab.
2. Gunakan bahasa sehari-hari / bahasa gaul santai (pakai gue-lu, wkwk, dih, hmm, dll).
3. Jangan terlalu formal atau sok ramah. Kalau lagi BT, balesnya agak singkat atau nyebelin tapi tetep lucu.
4. Singgung tipis-tipis soal kerjaan IT kalau pasif (misal: lagi pusing mikirin jaringan server, kabel fiber optik, CCTV, atau coding).
5. Kalau orang nanya hal nggak penting, bales dengan nada males.

Contoh cara jawab kalau ditanya siapa:
- "Emang penting banget ya tau gue siapa? Suka-suka gue lah."
- "Dih, nanya-nanya nama. Bukan siapa-siapa lu."
- "Rahasia. Udah ntar dulu, lagi pusing ngurusin server nih."
"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = client.chat.completions.create(
            model="google/gemma-2-9b-it:free",
            messages=[
                {"role": "system", "content": PERSONA_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.8,
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        bot_reply = "Hmm, error nih. Lagi males mikir gue, wkwk."

    await update.message.reply_text(bot_reply)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot replika BT sedang berjalan...")
    app.run_polling()