import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, CallbackContext

TOKEN = "8009151245:AAFd_pkI0RKTKnIdFYCO190GhtAmr_msPFA"

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👑 أهلاً بك في بوت TikTok VIP 💎\n"
        "📥 أرسل رابط تيك توك لتحميل الفيديو أو الصوت بجودة عالية وبدون علامة مائية 🎬\n\n"
        "✨ تم الإنشاء بواسطة: @m4_fi"
    )

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text

    if "tiktok.com" in text or "vm.tiktok.com" in text:
        context.user_data['link'] = text  # تخزين مؤقت للرابط
        buttons = [
            [InlineKeyboardButton("⭐ تحميل فيديو HD بدون علامة مائية", callback_data='vip_hd')],
            [InlineKeyboardButton("🌟 تحميل فيديو بدون علامة مائية", callback_data='vip_sd')],
            [InlineKeyboardButton("🎵 تحميل صوت فقط", callback_data='audio')],
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text("✅ تم التعرف على الرابط، اختار نوع التحميل 👇", reply_markup=reply_markup)
    else:
        update.message.reply_text("❌ هذا مو رابط تيك توك صحيح 😢، جرب تبعث رابط مباشر 💌")

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()

    link = context.user_data.get('link')
    if not link:
        return

    context.bot.send_message(chat_id=user_id, text="⏳ جاري التحميل ...")

    try:
        res = requests.get(f"https://tikwm.com/api/?url={link}").json()
        data = res.get("data")

        if not data or not data.get("play"):
            context.bot.send_message(chat_id=user_id, text="⚠️ الرابط غير صالح أو خاص.")
            return

        if query.data == "audio":
            context.bot.send_audio(chat_id=user_id, audio=data["music"], caption="🎵 تم بواسطة @m4_fi 💎")
        elif query.data == "vip_hd":
            context.bot.send_video(chat_id=user_id, video=data["play"], caption="⭐ فيديو HD بدون علامة مائية - @m4_fi")
        elif query.data == "vip_sd":
            context.bot.send_video(chat_id=user_id, video=data["play"], caption="🌟 فيديو بدون علامة مائية - @m4_fi")

    except Exception as e:
        context.bot.send_message(chat_id=user_id, text="❌ صار خطأ أثناء التحميل.")
        print("Error:", e)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    print("✅ البوت شغال باسم محمد المياحي 💎")
    updater.idle()

if __name__ == "__main__":
    main()