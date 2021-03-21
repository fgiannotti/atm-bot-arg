from flask import Flask, request
import telegram
import re
import time
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

   chat_id = update.message.chat.id
   msg_id = update.message.message_id

   # Telegram understands UTF-8, so encode text for unicode compatibility
   text = update.message.text.encode('utf-8').decode()
   # for debugging purposes only
   print("got text message :", text)
   # the first time you chat with the bot AKA the welcoming message
   if text == "/start":
      # print the welcoming message
      bot_welcome = """
      Welcome to atmFinder bot, this bots helps you find ATMs close to your location.
      """
       # send the welcoming message
      bot.sendChatAction(chat_id=chat_id, action="typing")
      time.sleep(1)
      bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
   elif "/banelco" in text.lower() or "/link" in text.lower():
        #call atm bot find atms
        print("asd")
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