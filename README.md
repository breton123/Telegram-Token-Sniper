# Telegram Token Sniper

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)


## Features

- Scans your whole telegram account for a specific message
- Buys automatically within 3 seconds
- Tracks price live
- Sells with a Take Profit / Trailing Take Profit / Stop Loss
- Sends updates through telegram

This bot was made with python and some javascript for selling. It needs minimal setup through the config file. All config variables are explain below.

## Config

- API_ID - Your API ID from telegram
- API_HASH - Your API HASH from telegram
- PHONE_NUMBER - The phone number linked to your telegram account
- WALLET_ADDRESS - The address of the wallet the bot will use to buy and sell
- WALLET_PRIVATE - The private key to your wallet
- BSC_NODE - The Node that will connect you to your blockchain. Must be wss. Semi-Private nodes will perform much better than public nodes. I recommend QuickNode or Infura
- TELEGRAM_REQUIRED_MESSAGE - The message the bot will look for in messages to signal a buy. Currently set as the first pump for CMC and CG fastest alerts
- BUY_AMOUNT - The amount of each coin your purchasing in BNB
- GAS_PRICE - The gas price for the transactions in gwei
- GAS_AMOUNT - The gas limit for the transactions
- AMOUNT_ACTIVE_TRADES - The amount of coins the bot will be able to hold and track at one time. After the coin is bought this will increase and will decrease when it is sold.
- SLIPPAGE - The amount the price can deviate during a transaction and still go through. This may need to increase or decrease depending on how volatile the coin is
- TAKE_PROFIT - The amount the price will increase before it sells. Set to -1 if you want to use the Trailing Profit Instead
- TRAILING_PROFIT - The amount the coin must drop from the highest point before it sells. Must be a value below 1 (example 0.95 for 5%)
- STOP_LOSS - The amount the coin needs to drop from its starting price before it sells. Wont be needed if a trailing profit is used
- SELL_ADDRESS - This doesn't matter. The bot will automatically update this variable when it goes to sell the coin

## Modules Used

This bot only uses 4 external modules to work

- [Pyrogram](https://docs.pyrogram.org/) - A module to listen to your telegram account. Used instead of telethon
- [Telegram-Send](https://pythonhosted.org/telegram-send/) - A module to send your account updates about the bot. Must be configured in console before it can be used with telegram-send --configure
- [Web3](https://web3py.readthedocs.io/en/stable/) - A module to connect to the blockchain to send and receive information. Needs a BSC Node to work
- [Requests](https://docs.python-requests.org/en/latest/) - A module to manage API requests

## API's Used

This bot only uses 3 API's to work

- [Telegram](https://core.telegram.org/) - This is needed to listen to your telegram account
- [Moralis](https://moralis.io/) - A Web3 based API system used for getting the live coin price
- [PancakeSwap](https://github.com/pancakeswap/pancake-info-api) - A public API that is used for getting the coin information such as it's Name and Symbol


## Installation

This bot requires [Node.js](https://nodejs.org/) v10+ and [Python](https://www.python.org/) v3.8+

Install the dependencies using requirements.txt

```sh
pip install -r requirements.txt
```

Get your Telegram API Keys:

```sh
https://my.telegram.org/apps
Enter your API_ID and API_HASH in config.json
```

Start the Bot:

```sh
Open run.bat or main.py
```


## Starting from Scratch

Setup a MetaMask Wallet and Connect it to BSC Mainnet:

```sh
https://www.youtube.com/watch?v=HVH6wpaHcDI
```

Deposit BNB into the Wallet (0.022 minimum recommended)

```sh
Binance - https://www.binance.com/en
MoonPay - https://www.moonpay.com/buy/bnb
```
## Upcoming Features

- Liquidity Sniper
- Remote Telegram Commands

This Bot is fully open source feel free to edit it as you wish. I would love feedback and any improvements anyone makes!

Donations - 0x6560a53D09234E8ACe6B53f4f9810713B9e6b4FB







   [node.js]: <http://nodejs.org>
