ATM-BOT-ARG


The purpose of this bot is to find ATMs near to your position.

The Server that handles the requests is deployed on heroku and uses a postgreSQL as an inventory for the ATMs.

To use the bot: https://t.me/atm_arg_bot 

Steps to use:    (/start also introduces these steps)
    1. Specify Network (we only support "BANELCO" or "LINK") (commands banelco or link are available)
    2. Send your position to the bot, and it will post the closest 3 ATMs around a 500mts radius.

This bot uses webhooks instead of long polling for more efficiency.

Next Steps:
    - Fix folium library to show map with markers
    - Encapsulate app logic into Handlers
    - Network chosen by user is saved forever in a postgresql. This should be done in a noSQL DB with a TTL.
    - To have information about ATMs cash availability i would use a job process (each weekday 8 am) to re-fill all the ATMs.
    - Unit tests

Python version used: 3.9

