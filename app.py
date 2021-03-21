from flask import Flask, request
import telegram
import re
import time
import atmfinder.dao as dao
from atmfinder.models import ATM
from atmfinder.credentials import bot_token, bot_user_name,URL
global bot
global TOKEN
TOKEN = bot_token

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
   # retrieve the message in JSON and then transform it to Telegram object
   update = telegram.Update.de_json(request.get_json(force=True), bot)
   print(update)
   message = None
   if update.edited_message:
         message = update.edited_message
   else:
         message = update.message
        
   chat_id = message.chat.id
   msg_id = message.message_id

   # Telegram understands UTF-8, so encode text for unicode compatibility
   text = message.text
   try:
      text = message.text.encode('utf-8').decode()
   except Exception as e:
      print("[ERROR] enconding text message err",text)

   print("got text msg",text)

   # for debugging purposes only
   # the first time you chat with the bot AKA the welcoming message


   # HANDLER FOR LOCATION
   if not message.text:
      if message.location:
         network = dao.getNetworkChosenForUser(message.chat.id)
         records = dao.SearchByNetwork(message.location.latitude,message.location.longitude, network)
         print(records)
         bot.sendMessage(chat_id=chat_id, text="buscamos cositas", reply_to_message_id=msg_id)
         return 'ok'
      else:
         bot.sendMessage(chat_id=chat_id, text="no text or location given...", reply_to_message_id=msg_id)

   #INITIAL HANDLER
   if text == "/start":
      bot_welcome = """
      Welcome to atmFinder bot, this bots helps you find ATMs close to your location.
      """
       # send the welcoming message
      bot.sendChatAction(chat_id=chat_id, action="typing")
      time.sleep(1)
      bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
   elif "banelco" in text.lower():
      print(message)
      dao.setNetworkChosenForUser("BANELCO",chat_id)
      return 'ok'
   elif "link" in text.lower():
      print(message)
      dao.setNetworkChosenForUser("LINK",chat_id)
      return 'ok'

   else:
      try:
           # clear the message we got from any non alphabets
           text = re.sub(r"\W", "_", text)
           print(text)
           # create the api link for the avatar based on http://avatars.adorable.io/
           url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
           # reply with a photo to the name the user sent,
           # note that you can send photos by url and telegram will fetch it for you
           bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
      except Exception as e:
           print(e)
           # if things went wrong
           bot.sendMessage(chat_id=chat_id, text="Command not found :)", reply_to_message_id=msg_id)

   return 'ok'

@app.route('/set-webhook', methods=['GET', 'POST'])
def set_webhook():
   webHookURL = '{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN)
   s = bot.setWebhook(webHookURL)
   if s:
      return "webhook setup ok"
   else:
      return "webhook setup failed"

@app.route('/')
def index():
   return '.'


if __name__ == '__main__':
   app.run(threaded=True)