from web3 import Web3, HTTPProvider
from sensitive import PRIVATE_KEY, MY_ACCOUNT, CONTRACT_ADDRESS


def main():
    # w3 = Web3(Web3.EthereumTesterProvider())
    w3 = Web3(HTTPProvider(
        'https://ropsten.infura.io/v3/50365d67b0b5445e8eef86ca07e49976'
    ))

    abi = getAbi()
    contractAddress = CONTRACT_ADDRESS
    myContract = w3.eth.contract(
        address=contractAddress,
        abi=abi
    )
    sendTx(w3, myContract, 50)
    resp = myContract.functions.retrieve().call()
    print('check')
    print(resp)

# Binary transaction ID returned b
# def getTransaction(bTx):


def sendTx(w3, contract, valToSend):

    tx = contract.functions.store(valToSend).buildTransaction(
        {'nonce': w3.eth.getTransactionCount(MY_ACCOUNT)})

    signed_tx = w3.eth.account.signTransaction(tx, private_key=PRIVATE_KEY)
    hexTxHash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print('tx sent')
    receipt = w3.eth.waitForTransactionReceipt(hexTxHash.hex())
    print('tx receipt found!')
    print(receipt)
    return receipt


def getAbi():
    return [
        {
            "inputs": [],
            "name": "retrieve",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "num",
                    "type": "uint256"
                }
            ],
            "name": "store",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]


if __name__ == "__main__":
    main()
