import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from mine_predictor import predict_mines, render_board

logging.basicConfig(level=logging.INFO)

# Dictionary to store per-user seed
user_seeds = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔐 Please enter your unhashed server seed:")
    return

async def handle_seed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    server_seed = update.message.text.strip()
    user_seeds[user_id] = server_seed

    # Show inline keyboard for mine count
    keyboard = [[InlineKeyboardButton(f"{i} Mines", callback_data=str(i))] for i in range(1, 7)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🧮 Select number of mines:", reply_markup=reply_markup)

async def handle_mine_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    mine_count = int(query.data)
    server_seed = user_seeds.get(user_id)

    # Show loading message
    await query.edit_message_text("🔄 Predicting mines, please wait...")

    # Predict mines
    mines = predict_mines(server_seed, mine_count)
    board = render_board(mines)

    await context.bot.send_message(chat_id=query.message.chat_id, text=f"🎯 Predicted Board with {mine_count} mines:\n\n{board}")

def main():
    import os
    TOKEN = "8223512483:AAGEEBnxiflEq_o63PXpF3pPupb3FQjEMCU"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_seed))
    app.add_handler(CallbackQueryHandler(handle_mine_selection))

    print("✅ Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
