from web3 import Web3


def sendTransaction(message):
    w3 = Web3(Web3.HTTPProvider(
        'https://ropsten.infura.io/v3/7b183da89a6f42188b9b4b0d07156e49'))
    address = '0x765426B3Cdea7FF9C35b3e007644C57652586FBb'
    privateKey = '0xbd19ac9e5b857859e37998a48c386b5dc2055952989fe4be50193e0a01b9d8a7'
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0, 'ether')
    signedTx = w3.eth.account.signTransaction(dict(
        nonce=nonce,
        gasPrice=gasPrice,
        gas=100000,
        to='0x0000000000000000000000000000000000000000',
        value=value,
        data=message.encode('utf-8')
    ), privateKey)

    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    return txId
