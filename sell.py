import os, colors, json, sys

def sell(address):
    with open("config.json","r") as file:
        data = json.load(file)
        data["SELL_ADDRESS"] = address
    os.remove("config.json")
    with open("config.json","w") as file:
        json.dump(data, file, indent=4)
    os.system("node server.js")
    sys.exit()
        
    
