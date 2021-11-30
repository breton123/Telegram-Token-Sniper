import requests, sell, telegram_send, json, colors

with open("config.json", "r") as jsonfile:
    config = json.load(jsonfile)
    
def trackPrice(address,tx):
    price_data = requests.get("https://deep-index.moralis.io/api/v2/erc20/"+str(address)+"/price?chain=bsc&exchange=PancakeSwapV2",headers={"X-API-Key": "HZjuPqq6ecLUZyBWElxdk0L06zbNhyCeWpvSrKlMeyXyUR5fTFAvnkh0We0ruDuR"})
    coin_info = requests.get("https://api.pancakeswap.info/api/v2/tokens/"+str(address))
    price_string = "{:.25f}".format(float(price_data.json()["usdPrice"]))
    highest = float(price_string)
    starting = float(price_string)
    name = coin_info.json()["data"]["name"]
    symbol = coin_info.json()["data"]["symbol"]
    message = f"Tracking New Token\n{name} / {symbol}\n{address}"
    telegram_send.send(messages=[message])
    print(colors.BOLD+colors.Green+f"STARTED TRACKING {symbol}")
    print(colors.Green+"Bought Price: "+price_string)
    msg_sent = False
    while True:
        try:
            price_data = requests.get("https://deep-index.moralis.io/api/v2/erc20/"+str(address)+"/price?chain=bsc&exchange=PancakeSwapV2",headers={"X-API-Key": "HZjuPqq6ecLUZyBWElxdk0L06zbNhyCeWpvSrKlMeyXyUR5fTFAvnkh0We0ruDuR"})
            price = price_data.json()["usdPrice"]
            if price <= (starting*config["STOP_LOSS"]):
                message = f"{symbol} has hit it's Stop Loss, Selling..."
                if msg_sent == False:
                    print(colors.Red+message)
                    telegram_send.send(messages=[message])
                    msg_sent = True
                sell.sell(address,tx)
            if price > highest:
                highest = price
            if config["TAKE_PROFIT"] == -1:
                if price <= (highest*config["TRAILING_PROFIT"]):
                    message = f"{symbol} has hit it's Trailing Profit, Selling..."
                    if msg_sent == False:
                        print(colors.Green+message)
                        telegram_send.send(messages=[message])
                        msg_sent = True
                    sell.sell(address,tx)
            else:
                if price >= (starting*config["TAKE_PROFIT"]):
                    message = f"{symbol} has hit it's Take Profit, Selling..."
                    if msg_sent == False:
                        print(colors.Green+message)
                        telegram_send.send(messages=[message])
                        msg_sent = True
                    sell.sell(address,tx)
        except Exception as e:
            print(e)
            pass
        
        