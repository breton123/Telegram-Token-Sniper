from web3 import Web3
import time, abi, json, telegram_send, sys, colors, colors, requests

with open("config.json", "r") as jsonfile:
    config = json.load(jsonfile)

def sell(address,tx):
    web3 = Web3(Web3.WebsocketProvider(config["BSC_NODE"]))
    sender_address = config["WALLET_ADDRESS"]
    spend = web3.toChecksumAddress("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")
    balance = web3.eth.get_balance(sender_address)
    contract_id = web3.toChecksumAddress(address)
    sellTokenContract = web3.eth.contract(contract_id, abi=abi.sellabi)
    contract = web3.eth.contract(address=config["PANCAKE_ROUTER_ADDRESS"], abi=abi.panabi)
    balance = sellTokenContract.functions.balanceOf(sender_address).call()
    symbol = sellTokenContract.functions.symbol().call()
    tokenValue = web3.toWei(balance, 'ether')
    tokenValue2 = web3.fromWei(tokenValue, 'ether')
    nonce = web3.eth.get_transaction_count(sender_address)
    nonce = nonce + 1
    approve = sellTokenContract.functions.approve(config["PANCAKE_ROUTER_ADDRESS"], balance).buildTransaction({
        'from': sender_address,
        'gas': config["GAS_AMOUNT"],
        'gasPrice': web3.toWei(config["GAS_PRICE"], 'gwei'),
        'nonce': int(nonce),
        })
    signed_txn = web3.eth.account.sign_transaction(approve, private_key=config["WALLET_PRIVATE"])
    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    nonce = nonce + 1
    while True:
        try:
            pancakeswap2_txn = contract.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
                int(tokenValue2),int(config["SLIPPAGE"]), 
                [contract_id,spend],
                str(sender_address),
                (int(time.time()) + 10000)
            ).buildTransaction({
                'from': sender_address,
                'gas': config["GAS_AMOUNT"],
                'gasPrice': web3.toWei(config["GAS_PRICE"], 'gwei'),
                'nonce': int(nonce),
            })
            signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=config["WALLET_PRIVATE"])
            tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            break
        except Exception as e:
            nonce = nonce + 1
            print(e)
    print(colors.Green+f"Successfully Sold {symbol}")
    print(colors.Green+"TX Token: " +str(web3.toHex(tx_token)))
    telegram_send.send(messages=[f"Successfully Sold {symbol}"+"\nTX Token: "+ str(web3.toHex(tx_token))])
    with open("active.txt", "r") as file:
            active = int(file.read())
    active = active - 1
    with open("active.txt", "w") as file:
            file.write(str(active))
            
            
    sys.exit()