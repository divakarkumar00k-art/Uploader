import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        message_id = context.args[0]
        try:
            await context.bot.copy_message(
                chat_id=update.effective_chat.id,
                from_chat_id=CHANNEL_ID,
                message_id=int(message_id)
            )
        except Exception as e:
            await update.message.reply_text(f"Error sending file: {e}")
    else:
        await update.message.reply_text("Send me any file (photo, video, document) to get link.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Channel me copy karo
        msg = await update.message.copy(chat_id=CHANNEL_ID)
        message_id = msg.message_id

        bot_username = (await context.bot.get_me()).username
        link = f"https://t.me/{bot_username}?start={message_id}"

        await update.message.reply_text(f"✅ Your Link:\n{link}")

    except Exception as e:
        await update.message.reply_text(f"Upload error: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

# Important: sirf media files handle karega
app.add_handler(MessageHandler(
    filters.Document.ALL | filters.PHOTO | filters.VIDEO,
    handle_file
))

print("Bot Started Successfully...")
app.run_polling()
