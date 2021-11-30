from web3 import Web3
import time, abi, json, track_price, telegram_send, colors

with open("config.json", "r") as jsonfile:
    config = json.load(jsonfile)

def buy(address):
    web3 = Web3(Web3.WebsocketProvider(config["BSC_NODE"]))
    panRouterContractAddress = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
    sender_address = config["WALLET_ADDRESS"]
    tokenToBuy = web3.toChecksumAddress(address)           
    spend = web3.toChecksumAddress("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")  
    contract = web3.eth.contract(address=panRouterContractAddress, abi=abi.panabi)
    nonce = web3.eth.get_transaction_count(sender_address)
    pancakeswap2_txn = contract.functions.swapExactETHForTokens(
    0,
    [spend,tokenToBuy],
    sender_address,
    (int(time.time()) + 10000)
    ).buildTransaction({
    'from': sender_address,
    'value': web3.toWei(config["BUY_AMOUNT"],'ether'),#This is the Token(BNB) amount you want to Swap from
    'gas': config["GAS_AMOUNT"],
    'gasPrice': web3.toWei(config["GAS_PRICE"],'gwei'),
    'nonce': nonce,
    })
    signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=config["WALLET_PRIVATE"])
    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(colors.ENDC+colors.Green+f"Coin has been bought {address}")
    print(colors.Green+"TX Token: "+str(web3.toHex(tx_token)))
    telegram_send.send(messages=["Coin Has Been Bought: "+address+"\nTX Token: "+ str(web3.toHex(tx_token))])
    with open("active.txt", "r") as file:
            active = int(file.read())
    active = active + 1
    with open("active.txt", "w") as file:
            file.write(str(active))
    track_price.trackPrice(address,web3.toHex(tx_token))
    
