from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8452565958:AAGFBsEl9mJit2puDJUTQr9Iqa_IbAY83BQ"

# Ссылка на ваше мини-приложение (замените на вашу)
MINI_APP_URL = "https://ВАШ_САЙТ.netlify.app"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет сообщение с inline-кнопкой (она будет ПОД сообщением)"""
    
    # Создаем inline-кнопку (она НЕ на клавиатуре, а под сообщением)
    keyboard = [
        [InlineKeyboardButton(
            text="📸 Открыть PhotoStockX",
            web_app=WebAppInfo(url=MINI_APP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        "🌟 *PhotoStockX* 🌟\n\n"
        "Добро пожаловать в глобальную экосистему для мгновенной продажи ваших мобильных фотографий!\n\n"
        "🧠 *Нейросеть оценивает ваши кадры* и находит покупателей за считанные секунды.\n\n"
        "👇 Нажмите на кнопку ниже, чтобы открыть приложение"
    )
    
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')

async def webapp_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка данных из мини-приложения"""
    if update.message and update.message.web_app_data:
        import json
        data = json.loads(update.message.web_app_data.data)
        action = data.get('action')
        
        if action == 'photos_submitted':
            await update.message.reply_text(
                "🎉 *Фото отправлены на проверку!*\n\n"
                f"Ваши фото ({data.get('count', 0)} шт.) переданы нейросети.\n"
                "Результаты оценки придут в ближайшее время.\n\n"
                "✨ Подпишитесь на обновления, чтобы не пропустить результаты!",
                parse_mode='Markdown'
            )
        elif action == 'start_selling':
            await update.message.reply_text("🚀 Вы начали продавать! Загрузите фото через приложение.")
        elif action == 'buy_photo':
            await update.message.reply_text("🛍️ Спасибо за интерес! Скоро здесь появится галерея фото.")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_handler))
    
    print("🚀 PhotoStockX бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
