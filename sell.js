Web3 = require('web3');
PancakeRouterABI = require('./contractABI').PancakeRouterABI;
PancakeRouterAddress = require('./contractABI').PancakeRouterAddress;
NewTokenABI = require('./contractABI').NewTokenABI;
config = require('./config.json');

const walletAddress = config.WALLET_ADDRESS;
const privateKey = config.WALLET_PRIVATE;
const sellTokenAddress = config.SELL_ADDRESS;
const gasPrice = config.GAS_PRICE;
const gasLimit = config.GAS_AMOUNT;
const slippage = config.SLIPPAGE;
const WSS_URL = config.BSC_NODE;


var web3 = new Web3(new Web3.providers.WebsocketProvider(WSS_URL));

Sell = async function() {
    let tokenContract = new web3.eth.Contract(NewTokenABI, sellTokenAddress);
    let pancakeContract = new web3.eth.Contract(PancakeRouterABI, PancakeRouterAddress);
    let bnbAddress = '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c';
    let path = [sellTokenAddress, bnbAddress];
    let GasPrice = Math.pow(10, 9) * gasPrice;
    let deadline = 2000000000;
    let amount = '115792089237316195423570985008687907853269984665640564039457584007913129639935';
    let transactionApprove = tokenContract.methods.approve(
        PancakeRouterAddress,
        amount
    );
    const optionsApprove = {
        from: walletAddress, 
        to: sellTokenAddress, 
        gas: gasLimit, 
        data: transactionApprove.encodeABI()
    };
    try {
        var signedTransaction = await web3.eth.accounts.signTransaction(optionsApprove, privateKey);
        try {
            let receipt = await web3.eth.sendSignedTransaction(signedTransaction.rawTransaction);
            console.log("Coin has been Approved");
            console.log("TX Hash: "+receipt.transactionHash);
        } catch (err) {
            console.log(err);
        }
    } catch (err) {
        console.log(err);
    }
    let balance = await tokenContract.methods.balanceOf(walletAddress).call()
    let transaction = pancakeContract.methods.swapExactTokensForETHSupportingFeeOnTransferTokens(
        balance,
        0,
        path,
        walletAddress,
        deadline
    );
    const options = {
        from: walletAddress, 
        to: PancakeRouterAddress, 
        gas: gasLimit, 
        gasPrice: GasPrice,
        data: transaction.encodeABI() 
    }
    try {
        var signedTransaction = await web3.eth.accounts.signTransaction(options, privateKey);
        try {
            let receipt = await web3.eth.sendSignedTransaction(signedTransaction.rawTransaction);
            console.log("Sold")
            console.log("TX Hash: "+receipt.transactionHash);
            process.exit(1)
        } catch (err) {
            console.log(err);
        }
    } catch (err) {
        console.log(err);
    }    
};

Sell();