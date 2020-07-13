from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
import logging
from firebase import firebase
from telegram import InlineQueryResultArticle, InputTextMessageContent

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater=Updater(token='1361442277:AAGvchKc35aElkOd9NPFIBJGCO3s8XzpjQI', use_context=True)
dispatcher=updater.dispatcher

def start(update, context):
	user_says=" ".join(context.args)
	update.message.reply_text("You said: "+user_says)

def echo(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def caps(update, context):
	text_caps=' '.join(context.args).upper()
	context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def inline_caps(update, context):
	query=update.inline_query.query
	if not query:
		return
	results=list()
	results.append(InlineQueryResultArticle(id=query.upper(), title='Caps', input_message_content=InputTextMessageContent(query.upper())))
	context.bot.answer_inline_query(update.inline_query.id, results)


start_handler=CommandHandler('start', start)
dispatcher.add_handler(start_handler)
echo_handler=MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)
caps_handler=CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler);
inline_caps_handler=InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)

updater.start_polling()