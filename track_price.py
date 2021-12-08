import requests, sell, telegram_send, json, colors, sys, time
from datetime import datetime
from threading import Thread

with open("config.json", "r") as jsonfile:
    config = json.load(jsonfile)
    
def trackPrice(address):
    try:
        price_data = requests.get("https://deep-index.moralis.io/api/v2/erc20/"+str(address)+"/price?chain=bsc&exchange=PancakeSwapV2",headers={"X-API-Key": "HZjuPqq6ecLUZyBWElxdk0L06zbNhyCeWpvSrKlMeyXyUR5fTFAvnkh0We0ruDuR"})
        coin_info = requests.get("https://api.pancakeswap.info/api/v2/tokens/"+str(address))
        price_string = "{:.25f}".format(float(price_data.json()["usdPrice"]))
    except:
        print("Error Getting Price Selling Immediately")
        telegram_send.send(messages=["ERROR GETTING PRICE SELLING IMMEDIATELY"])
        newThread = Thread(target=sell.sell,args=(address,)).start()
        sys.exit()
    highest = float(price_string)
    starting = float(price_string)
    name = coin_info.json()["data"]["name"]
    symbol = coin_info.json()["data"]["symbol"]
    now = datetime.now()
    current_time = str(now.strftime("%H:%M:%S"))
    
    message = f"""
<pre>Started Tracking {name} / {symbol}\n
Purchase Time: {current_time}\n
Purchase Price: {price_string}\n
Address: {address}</pre>
        """
    telegram_send.send(messages=[message],parse_mode='html')
    
    print(colors.BOLD+colors.Green+f"STARTED TRACKING {symbol}")
    print(colors.Green+"Bought Price: "+price_string)
    
    msg_sent = False
    while True:
        try:
            price_data = requests.get("https://deep-index.moralis.io/api/v2/erc20/"+str(address)+"/price?chain=bsc&exchange=PancakeSwapV2",headers={"X-API-Key": "HZjuPqq6ecLUZyBWElxdk0L06zbNhyCeWpvSrKlMeyXyUR5fTFAvnkh0We0ruDuR"})
            price = price_data.json()["usdPrice"]
            
            if price <= (starting*config["STOP_LOSS"]):
                newThread = Thread(target=sell.sell,args=(address,)).start()
                if msg_sent == False:
                    multiplier = price / starting
                    percentage = price - starting
                    percentage = str((percentage / starting) * 100)
                    sellAmount = config["BUY_AMOUNT"] * multiplier
                    profit = sellAmount - config["BUY_AMOUNT"]
                    sellAmount = str('{:.10f}'.format(sellAmount))
                    profit = str('{:.10f}'.format(profit))
                    sellAmount = sellAmount.strip("0")
                    profit = profit.strip("0")
                    if "." in sellAmount:
                        sellAmount = "0" + sellAmount
                    if "." in sellAmount:
                        profit = "0" + profit
                    message = f"""
                    <pre>{symbol} has hit it's Stop Loss\n
Percentage Decrease: {percentage}%\n
Money Multiplier: {multiplier}\n
Value: {sellAmount}\n
Loss: {profit}
</pre>
"""
                    print(f"{symbol} has hit it's Stop Loss")
                    print(f"Percentage Decrease: {percentage}")
                    print(f"Money Multiplier: {multiplier}")
                    print(f"Value: {sellAmount}")
                    print(f"Loss: {profit}")
                    telegram_send.send(messages=[message],parse_mode='html')
                    sys.exit()
            if price > highest:
                highest = price
            if config["TAKE_PROFIT"] == -1:
                if price <= (highest*config["TRAILING_PROFIT"]):
                    newThread = Thread(target=sell.sell,args=(address,)).start()
                    if msg_sent == False:
                        multiplier = price / starting
                        percentage = price - starting
                        percentage = str((percentage / starting) * 100)
                        sellAmount = config["BUY_AMOUNT"] * multiplier
                        profit = sellAmount - config["BUY_AMOUNT"]
                        sellAmount = str('{:.10f}'.format(sellAmount))
                        profit = str('{:.10f}'.format(profit))
                        sellAmount = sellAmount.strip("0")
                        profit = profit.strip("0")
                        if "." in sellAmount:
                            sellAmount = "0" + sellAmount
                        if "." in sellAmount:
                            profit = "0" + profit
                        message = f"""
                        <pre>{symbol} has hit it's Trailing Profit\n
Percentage Increase: {percentage}%\n
Money Multiplier: {multiplier}\n
Value: {sellAmount}\n
Profit: {profit}
</pre>
"""
                        print(f"{symbol} has hit it's Trailing Profit")
                        print(f"Percentage Increase: {percentage}")
                        print(f"Money Multiplier: {multiplier}")
                        print(f"Value: {sellAmount}")
                        print(f"Profit: {profit}")
                        telegram_send.send(messages=[message],parse_mode='html')
                        sys.exit()
            else:
                if price >= (starting*config["TAKE_PROFIT"]):
                    newThread = Thread(target=sell.sell,args=(address,)).start()
                    if msg_sent == False:
                        multiplier = price / starting
                        percentage = price - starting
                        percentage = str((percentage / starting) * 100)
                        sellAmount = config["BUY_AMOUNT"] * multiplier
                        profit = sellAmount - config["BUY_AMOUNT"]
                        sellAmount = str('{:.10f}'.format(sellAmount))
                        profit = str('{:.10f}'.format(profit))
                        sellAmount = sellAmount.strip("0")
                        profit = profit.strip("0")
                        if "." in sellAmount:
                            sellAmount = "0" + sellAmount
                        if "." in sellAmount:
                            profit = "0" + profit
                        message = f"""
                        <pre>{symbol} has hit it's Take Profit\n
Percentage Increase: {percentage}%\n
Money Multiplier: {multiplier}\n
Value: {sellAmount}\n
Profit: {profit}
</pre>
"""
                        print(f"{symbol} has hit it's Take Profit")
                        print(f"Percentage Increase: {percentage}")
                        print(f"Money Multiplier: {multiplier}")
                        print(f"Value: {sellAmount}")
                        print(f"Profit: {profit}")
                        telegram_send.send(messages=[message],parse_mode='html')
                        sys.exit()
        except Exception as e:
            print(e)
            pass
        