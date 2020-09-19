import json

from web3 import Web3, HTTPProvider
from solc import compile_standard
from sensitive import PRIVATE_KEY, MY_ACCOUNT

'''
Interact with fixed smart contract
made/deployed in web browser.
'''


def main():
    # w3 = Web3(Web3.EthereumTesterProvider())
    w3 = Web3(HTTPProvider(
        'https://kovan.infura.io/v3/f26caa7ebc1e424ab84e48c356e9158d'
    ))
    compiledSol = getCompiledContract()
    print('check')
    abi = json.loads(compiledSol['contracts']['SampleStore.sol']
                     ['SampleStore']['metadata'])['output']['abi']

    bytecode = compiledSol['contracts']['SampleStore.sol']['SampleStore']['evm']['bytecode']['object']

    sampleContract = w3.eth.contract(abi=abi, bytecode=bytecode)

    txHash = txReceipt(w3, sampleContract)

    print(txHash)

    # print(resp['contracts']['SampleStore.sol']['SampleStore']['abi'])

# Binary transaction ID returned b
# def getTransaction(bTx):


def txReceipt(w3, contract):

    tx = contract.constructor().buildTransaction(
        {'nonce': w3.eth.getTransactionCount(MY_ACCOUNT)})

    signed_tx = w3.eth.account.signTransaction(tx, private_key=PRIVATE_KEY)
    hexTxHash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print('tx sent')
    receipt = w3.eth.waitForTransactionReceipt(hexTxHash.hex())
    print('tx receipt found!')
    print(receipt.transactionHash.hex())

    return receipt


# def createContract(w3, compiled_sol):


def getCompiledContract():
    return compile_standard({
        "language": "Solidity",
        "sources": {
            "SampleStore.sol": {
                "content": '''
                pragma solidity ^0.7.1;
                // SPDX-License-Identifier: MIT
                contract SampleStore {

                    uint256 number;

                    function store(uint256 num) public {
                        number = num;
                    }

                    function retrieve() public view returns (uint256){
                        return number;
                    }



                 }
               '''
            }
        },
        "settings":
        {
            "outputSelection": {
                "*": {
                    "*": [
                        "metadata", "evm.bytecode", "evm.bytecode.sourceMap"
                    ]
                }
            }
        }
    })


if __name__ == "__main__":
    main()
