import json
import telegram
import telegram.ext

__version__=json.loads(open("version.json").read())["version"]

# The chat where the confessions are sended
vinculed_chat_info=json.loads(open("chat.json").read())
vinculed_chat=vinculed_chat_info["vinculed_chat_id"]
vinculed_chat1=vinculed_chat_info["vinculed_chat_id1"]
vinculed_chat_link=vinculed_chat_info["vinculed_chat_link"]
vinculed_chat_name=vinculed_chat_info["vinculed_chat_name"]

def ban(update, context):
	if update.message.from_user.id not in vinculed_chat_info["admins_allowed"]:
		return
	user_id = update.message.reply_to_message.from_user.id
	context.bot.ban_chat_member(chat_id = vinculed_chat, user_id = user_id)
	vinculed_chat_info["users_banned_forever"].append(user_id)
	with open("chat.json", "w") as file:
		json.dump(vinculed_chat_info, file)

def send_message(update, default, **dict):
    if update.message.from_user.language_code in dict:
        return dict[update.message.from_user.language_code]
    else:
        return dict[default]

# Reply Markup Handlers
def how_confess(update, context):
    if update.message.from_user.id in vinculed_chat_info["users_banned_forever"]:
    	update.message.reply_text(send_message(update, default="es", en="You have been banned forever.", es="Has sido baneado para siempre por MMWVO."))
    	return
    update.message.reply_text(send_message(update, default="es", en="📖 It's easy, just send your confession.", es="📖 Es facil, solo manda tu confesion."))

def about_me(update, context):
    if update.message.from_user.id in vinculed_chat_info["users_banned_forever"]:
    	update.message.reply_text(send_message(update, default="es", en="You have been banned forever.", es="Has sido baneado para siempre por MMWVO."))
    	return
    update.message.reply_text(
        send_message(
            update,
            default="es",
            en="Im an confession bot for channel https://t.me/insane_arg.\r\nVersion_{0}\r\n\r\nMaded by @lucas181,".format(__version__),
            es="Soy un bot de confesiones para el canal https://t.me/insane_arg.\r\nVersion_{0}\r\n\r\nCreado por @lucas181,".format(__version__)
        )
    )

reply_markup_es={"✅ Confiesate": how_confess, "📚 Acerca de...": about_me}
reply_markup_en={"✅ Confess you": how_confess, "📚 About me...": about_me}

def getCorrectMarkup(update):
    if update.message.from_user.language_code=="en":
        return telegram.ReplyKeyboardMarkup([list(reply_markup_en.keys())])
    else:
        return telegram.ReplyKeyboardMarkup([list(reply_markup_es.keys())])

def checkGroup(update):
    if "-" in str(update.message.chat_id):
        return 1
    else:
        return 0

def start(update, context):
    if update.message.from_user.id in vinculed_chat_info["users_banned_forever"]:
    	update.message.reply_text(send_message(update, default="es", en="You have been banned forever.", es="Has sido baneado para siempre por MMWVO."))
    	return
    update.message.reply_text(send_message(update, default="es", en="Welcome to the INSANE anonymous confessions bot", es="Bienvenido al bot de confesiones anonimas INSANE"), reply_markup=getCorrectMarkup(update))
    update.message.reply_text(send_message(update, default="es", en="You must be here <a href='"+vinculed_chat_name+"'>t.me/"+vinculed_chat_link+"</a>", es="Deberias estar aqui! <a href='"+vinculed_chat_name+"'>t.me/"+vinculed_chat_link+"</a>"), parse_mode="html")

def handleMessages(update, context):
    if update.message.from_user.id in vinculed_chat_info["users_banned_forever"]:
    	update.message.reply_text(send_message(update, default="es", en="You have been banned forever.", es="Has sido baneado para siempre por MMWVO."))
    	return
    # Get's if the bot are in a group
    if "-" in str(update.effective_message.chat_id):
        return
    else:
        # Send's the confession to the vinculed chat
        context.bot.send_message(chat_id=vinculed_chat, text=update.message.text + '\n\n @ConfeINSANEbot' )
        text_for_vinculed_chat1 = update.message.text + '\nID del Autor: ' + str(update.message.from_user.id)
        context.bot.send_message(chat_id=vinculed_chat1, text=text_for_vinculed_chat1)
        text_for_vinculed_chat2 = update.message.text + '\n\nAutor: ' + update.message.from_user.first_name + '\n@ del Autor: ' + '@' + update.message.from_user.username
        context.bot.send_message(chat_id=vinculed_chat1, text=text_for_vinculed_chat2)
        update.message.reply_text(send_message(update, default="es", en="🛫 Sended", es="🛫 Enviado"), reply_markup=getCorrectMarkup(update))

def handleBadCommands(update, context):
    if update.message.from_user.id in vinculed_chat_info["users_banned_forever"]:
    	update.message.reply_text(send_message(update, default="es", en="You have been banned forever.", es="Has sido baneado para siempre por MMWVO."))
    	return
    if checkGroup(update)==1:
        return
    else:
        update.message.reply_text(send_message(update, default="es", en="Invalid Command", es="Comando incorrecto"), reply_markup=getCorrectMarkup(update))

def handleVoice(update, context):
    if update.message.from_user.id in vinculed_chat_info["users_banned_forever"]:
    	update.message.reply_text(send_message(update, default="es", en="You have been banned forever.", es="Has sido baneado para siempre por MMWVO."))
    	return
    if update.message.voice.duration>=300:
        update.message.reply_text(send_message(update, default="es", en="You can only send a voice message of less than five minutes", es="Solo puedes mandar un mensaje de voz de menos de cinco minutos"))
    else:
        context.bot.send_voice(voice=update.message.voice.file_id , chat_id=vinculed_chat, caption="@ConfeINSANEbot")
        context.bot.send_voice(voice=update.message.voice.file_id, chat_id=vinculed_chat1, caption="@ConfeINSANEbot")
        text_for_vinculed_chat2 =  'datos del audio ☝️' + '\n\nID del Autor: ' + str(update.message.from_user.id)
        context.bot.send_message(chat_id=vinculed_chat1, text=text_for_vinculed_chat2)
        text_for_vinculed_chat3 =  'datos del audio ☝️' + '\n\nAutor: ' + update.message.from_user.first_name + '\n@ del Autor: ' + '@' + update.message.from_user.username
        context.bot.send_message(chat_id=vinculed_chat1, text=text_for_vinculed_chat3)

def handleAudio(update, context):
    if update.message.from_user.id in vinculed_chat_info["users_banned_forever"]:
    	update.message.reply_text(send_message(update, default="es", en="You have been banned forever.", es="Has sido baneado para siempre por MMWVO."))
    	return
    if update.message.audio.duration>=300:
        update.message.reply_text(send_message(update, default="es", en="You can only send a voice message of less than five minutes", es="Solo puedes mandar un mensaje de voz de menos de cinco minutos"))
    else:
        context.bot.send_audio(audio=update.message.audio.file_id, chat_id=vinculed_chat, caption=update.message.audio.title+"\r\n\r\n@ConfeINSANEbot")
        context.bot.send_audio(audio=update.message.audio.file_id, chat_id=vinculed_chat1, caption=update.message.audio.title+"\r\n\r\n@ConfeINSANEbot")
        text_for_vinculed_chat2 =  'datos del audio ☝️' + '\n\nID del Autor: ' + str(update.message.from_user.id)
        context.bot.send_message(chat_id=vinculed_chat1, text=text_for_vinculed_chat2)
        text_for_vinculed_chat3 =  'datos del audio ☝️' + '\n\nAutor: ' + update.message.from_user.first_name + '\n@ del Autor: ' + '@' + update.message.from_user.username
        context.bot.send_message(chat_id=vinculed_chat1, text=text_for_vinculed_chat3)


# The bot updater
updater=telegram.ext.Updater(open("token").read().strip("\r\n"))
dispatcher=updater.dispatcher

# An handler for the /start command
dispatcher.add_handler(telegram.ext.CommandHandler("start", start))

dispatcher.add_handler(telegram.ext.CommandHandler("ban", ban))

for i in list(reply_markup_en.keys()):
    dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.regex(i), reply_markup_en[i]))

for i in list(reply_markup_es.keys()):
    dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.regex(i), reply_markup_es[i]))

dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.voice, handleVoice))
dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.audio, handleAudio))


# An handler for the sended confession's
dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handleMessages))

# Start's the bot
updater.start_polling()
print('Bot cargado')
updater.idle()
