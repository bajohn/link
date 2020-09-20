import json

from web3 import Web3, HTTPProvider
from solc import compile_standard
from sensitive import PRIVATE_KEY, MY_ACCOUNT

'''
Interact with fixed smart contract
made/deployed in web browser.
Set value in constructor and read.
'''


def main():
    # w3 = Web3(Web3.EthereumTesterProvider())
    w3 = Web3(HTTPProvider(
        'https://kovan.infura.io/v3/f26caa7ebc1e424ab84e48c356e9158d'
    ))
    compiledSol = compiledContract()
    print('check')
    abi = json.loads(compiledSol['contracts']['SampleStore.sol']
                     ['SampleStore']['metadata'])['output']['abi']

    bytecode = compiledSol['contracts']['SampleStore.sol']['SampleStore']['evm']['bytecode']['object']

    localContract = w3.eth.contract(abi=abi, bytecode=bytecode)

    receipt = newContractReceipt(w3, localContract)
    contractHash = receipt['contractHash']
    print('Contract hash')
    print(contractHash)
    deployedContract = w3.eth.contract(
        address=contractHash,
        abi=abi
    )
    deployedNum = deployedContract.functions.retrieve().call()
    print('deployed num')
    print(deployedNum)

    # print(resp['contracts']['SampleStore.sol']['SampleStore']['abi'])


def newContractReceipt(w3, contract):
    '''
    Create the contract
    Return the txHash and address of the new contract
    '''
    tx = contract.constructor(12).buildTransaction(
        {'nonce': w3.eth.getTransactionCount(MY_ACCOUNT)})

    signed_tx = w3.eth.account.signTransaction(tx, private_key=PRIVATE_KEY)
    hexTxHash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print('tx sent')
    receipt = w3.eth.waitForTransactionReceipt(hexTxHash.hex())
    print('tx receipt found!')

    return dict(
        txHash=receipt.transactionHash.hex(),
        contractHash=receipt.contractAddress
    )


# def createContract(w3, compiled_sol):


def compiledContract():
    '''
    Compile a hardcoded contract, return compiled binary
    '''

    return compile_standard({
        "language": "Solidity",
        "sources": {
            "SampleStore.sol": {
                "content": '''
                pragma solidity ^0.7.1;
                // SPDX-License-Identifier: MIT
                contract SampleStore {

                    uint256 number;
                    constructor(uint256 _number) {
                        number = _number;
                    }
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
