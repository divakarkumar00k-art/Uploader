import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Environment variables se token aur channel id lenge
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# /start command handle karega
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        message_id = context.args[0]
        try:
            await context.bot.copy_message(
                chat_id=update.effective_chat.id,
                from_chat_id=CHANNEL_ID,
                message_id=int(message_id)
            )
        except:
            await update.message.reply_text("❌ File not found.")
    else:
        await update.message.reply_text("📁 Send me any file to get a shareable link.")

# Jab koi file bheje
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # File ko private channel me copy karo
    msg = await update.message.copy(chat_id=CHANNEL_ID)
    message_id = msg.message_id

    # Bot username nikalo
    bot_username = (await context.bot.get_me()).username

    # Deep link generate karo
    link = f"https://t.me/{bot_username}?start={message_id}"

    await update.message.reply_text(f"✅ Your Link:\n{link}")

# App build karo
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_file))

print("Bot is running...")
app.run_polling()
