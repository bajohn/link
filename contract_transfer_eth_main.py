import json

from web3 import Web3, HTTPProvider
from solc import compile_standard
from sensitive import PRIVATE_KEY, MY_ACCOUNT

'''
Send some eth via a deployed contract
to hardcoded addresses
'''


def main():
    # senderAddr = '0x47a50df6f06C1837582a28630eF58fC66d1F25D1'

    receiverAddr = '0x068528704bAFD8A4B42985Baf87b8877fBea2E35'

    w3 = Web3(HTTPProvider(
        'https://kovan.infura.io/v3/f26caa7ebc1e424ab84e48c356e9158d'
    ))
    compiledSol = compiledContract()
    print('check')
    abi = json.loads(compiledSol['contracts']['SampleStore.sol']
                     ['SampleStore']['metadata'])['output']['abi']

    bytecode = compiledSol['contracts']['SampleStore.sol']['SampleStore']['evm']['bytecode']['object']

    localContract = w3.eth.contract(abi=abi, bytecode=bytecode)

    receipt = newContractReceipt(w3, localContract, receiverAddr)
    contractHash = receipt['contractHash']
    print('Contract hash')
    print(contractHash)
    deployedContract = w3.eth.contract(
        address=contractHash,
        abi=abi
    )

    fundHash = fundContractTxHash(w3, contractHash)
    print(fundHash)

    return True
    deployedNum = deployedContract.functions.retrieve().call()
    print('deployed num')
    print(deployedNum)

    # print(resp['contracts']['SampleStore.sol']['SampleStore']['abi'])


def fundContractTxHash(w3, contractHash):
    nonce = w3.eth.getTransactionCount(MY_ACCOUNT)
    print('nonce')
    print(nonce)
    signed_tx = w3.eth.account.signTransaction(dict(
        nonce=nonce,
        gasPrice=w3.eth.gasPrice,
        gas=100000,
        to=contractHash,
        value=12345,
        data=b'',
    ),
        private_key=PRIVATE_KEY
    )

    hexTxHash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print('funding tx sent')
    receipt = w3.eth.waitForTransactionReceipt(hexTxHash.hex())
    print('funding tx receipt found!')
    return receipt.transactionHash.hex()


def newContractReceipt(w3, contract, receiverAddress):
    '''
    Create the contract
    Return the txHash and address of the new contract
    '''
    nonce = w3.eth.getTransactionCount(MY_ACCOUNT)
    print('nonce')
    print(nonce)
    tx = contract.constructor(receiverAddress).buildTransaction(
        {'nonce': nonce})

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

                    address payable receiver;
                    uint256 sendVal;

                    constructor(
                        address payable _receiver
                        ) {
                        receiver = _receiver;
                        sendVal = 10;
                    }
                    function store(uint256 num) public {
                        sendVal = num;
                    }

                    function send() public {
                        receiver.transfer(sendVal);
                    }


                    // fallback function 
                    fallback () external payable {
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
