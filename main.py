from web3 import Web3, HTTPProvider
from sensitive import private_key
def main():
    # w3 = Web3(Web3.EthereumTesterProvider())
    w3 = Web3(HTTPProvider(
        'https://ropsten.infura.io/v3/50365d67b0b5445e8eef86ca07e49976'
    ))

    abi = getAbi()
    contractAddress = '0x63b23019Ff45EDa920c84BC89f5448843e85CC95'
    myContract = w3.eth.contract(
    address=contractAddress,
    abi=abi
    )

    resp = myContract.functions.store(3).call()
    print('called')
    print(resp)
    resp = myContract.functions.retrieve().call()
    print('called')
    print(resp)

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