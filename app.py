from flask import Flask, request
import telegram
import re
import time
import folium
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
      print("[WARN] enconding text message failed",text)
   print("got text msg",text)

   # for debugging purposes only
   # the first time you chat with the bot AKA the welcoming message


   # HANDLER FOR LOCATION
   if not message.text:
      if message.location:
         ok,network = dao.get_network_chosen_for_user(message.chat.id)
         #NETWORK NOT FOUND
         if not ok:
            print("[ERROR] location found but no network has been chosen.")
            bot.send_message(chat_id=chat_id, text="Please set up network first.", reply_to_message_id=msg_id)
            return 'ok'
         #NETWORK FOUND, SEARCH ATMs
         fullStr = ""
         try:
            records = dao.search_by_network(message.location.latitude,message.location.longitude, network)
            fullStr = 'Bank list: \n' + ' '.join([atm.name +" " + atm.address + " a " + str(int(atm.current_distance)) + "mts \n\n" for atm in records])
            if len(records) == 0:
               fullStr += "Nothing found."
            else:
               m = folium.Map(location=[message.latitue, message.longitude])
               tooltip = "Click me!"

               folium.Marker(
                  [records[0].lat,records[0].long], popup=records[0].address, tooltip=tooltip
               ).add_to(m)
               
               bot.send_photo(chat_id=chat_id, photo=m._to_png())
         except Exception as e:
            fullStr = "Something wrong happened looking for atms. Please try again" 

         bot.send_message(chat_id=chat_id, text=fullStr, reply_to_message_id=msg_id)
         return 'ok'
      else:
         bot.send_message(chat_id=chat_id, text="no text or location given...", reply_to_message_id=msg_id)
         return 'ok'

   #INITIAL HANDLER
   if text == "/start":
      bot_welcome = """
      Welcome to atmFinder bot, this bots helps you find ATMs close to your location.
      """
      bot.sendChatAction(chat_id=chat_id, action="typing")
      time.sleep(2)
      bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
      return 'ok'

   elif "banelco" in text.lower():
      print(message)
      try:
         dao.set_network_chosen_for_user("LINK",chat_id)
      except Exception:
         bot.sendMessage(chat_id=chat_id, text="Network save failed. Please try again.", reply_to_message_id=msg_id)
         return 'ok'
      bot.sendMessage(chat_id=chat_id, text="Network saved OK. Send me your location please.", reply_to_message_id=msg_id)
      return 'ok'

   elif "link" in text.lower():
      print(message)
      try:
         dao.set_network_chosen_for_user("LINK",chat_id)
      except Exception:
         bot.sendMessage(chat_id=chat_id, text="Network save failed. Please try again.", reply_to_message_id=msg_id)
         return 'ok'
      bot.sendMessage(chat_id=chat_id, text="Network saved OK. Send me your location please.", reply_to_message_id=msg_id)
      return 'ok'

   elif "/network" in text.lower():
      _, network = dao.get_network_chosen_for_user(chat_id)
      bot.send_message(chat_id=chat_id, text="Network found: "+network, reply_to_message_id=msg_id)
      return 'ok'

   else:
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