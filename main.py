import json, re, telegram_send, buy, colors
from pyrogram import Client, filters
from threading import Thread

with open("config.json", "r") as jsonfile:
    config = json.load(jsonfile)

app = Client("my_account",config["API_ID"],config["API_HASH"])

currently_active = input("How many active trades do you currently have?")

with open("active.txt", "w") as file:
    file.write(currently_active)
    


print(colors.Green+"""
        ____   _____  _____   _______ ____  _  ________ _   _   _______ _____            _____ _  ________ _____  
 |  _ \ / ____|/ ____| |__   __/ __ \| |/ /  ____| \ | | |__   __|  __ \     /\   / ____| |/ /  ____|  __ \ 
 | |_) | (___ | |         | | | |  | | ' /| |__  |  \| |    | |  | |__) |   /  \ | |    | ' /| |__  | |__) |
 |  _ < \___ \| |         | | | |  | |  < |  __| | . ` |    | |  |  _  /   / /\ \| |    |  < |  __| |  _  / 
 | |_) |____) | |____     | | | |__| | . \| |____| |\  |    | |  | | \ \  / ____ \ |____| . \| |____| | \ \ 
 |____/|_____/ \_____|    |_|  \____/|_|\_\______|_| \_|    |_|  |_|  \_\/_/    \_\_____|_|\_\______|_|  \_\
                                                                                                            
                                                                                                            """
)
print(colors.Green+"Started Listening...")

@app.on_message()
async def newMessage(client, message):
    newMessage = message["text"]
    if config["TELEGRAM_REQUIRED_MESSAGE"] in newMessage:
        print(colors.Green+"New Telegram Pump Found...")
        print(newMessage)
        with open("active.txt", "r") as file:
            active = int(file.read())
        if active >= config["AMOUNT_ACTIVE_TRADES"]:
            print(colors.Red+"ERROR... Too many active trades")
        else:
            address = newMessage.split("0x")[1][:40]
            address = "0x" + address
            print(f"Address: {address}")
            newThread = Thread(target=buy.buy,args=(address,)).start()

app.run()