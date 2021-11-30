import json, re, telegram_send, buy, colors, asyncio
from telethon import TelegramClient, events, sync
from threading import Thread

with open("config.json", "r") as jsonfile:
    config = json.load(jsonfile)
    
currently_active = input("How many active trades do you currently have?")

with open("active.txt", "w") as file:
    file.write(currently_active)
    
client = TelegramClient('Sniper', config["API_ID"], config["API_HASH"])


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

@client.on(events.NewMessage(chats=config["TELEGRAM_CHANNELS"][0]))
async def newMessageListener(event):
    newMessage = str(event.message.message)
    if config["TELEGRAM_REQUIRED_MESSAGE"] in newMessage:
        print(colors.Green+"New Telegram Pump Found...")
        with open("active.txt", "r") as file:
            active = int(file.read())
        if active >= config["AMOUNT_ACTIVE_TRADES"]:
            print(colors.Red+"ERROR... Too many active trades")
        else:
            address = re.sub(r'[\W_]+', '', newMessage)
            address = address.split("Address")[1][:42]
            newThread = Thread(target=buy.buy,args=(address,)).start()
client.start()
client.run_until_disconnected()


    