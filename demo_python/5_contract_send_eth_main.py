import json

from web3 import Web3, HTTPProvider
from solc import compile_standard
from sensitive import PRIVATE_KEY, MY_ACCOUNT

'''
Send some eth via a deployed contract
to hardcoded addresses
'''


def main():

    w3 = Web3(HTTPProvider(
        'https://kovan.infura.io/v3/f26caa7ebc1e424ab84e48c356e9158d'
    ))
    receiverAddr = '0x068528704bAFD8A4B42985Baf87b8877fBea2E35'  # unused here
    account = w3.eth.account.privateKeyToAccount(
        PRIVATE_KEY)  # This signs everything
    w3.eth.defaultAccount = account.address

    compiledSol = compiledContract()

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

    fundHash = fundContractTxHash(w3, deployedContract)

    deployedNum = deployedContract.functions.retrieve().call()
    print('Deposit amount recorded on-chain')
    print(deployedNum)

    print('sending eth to given address')
    nonce = w3.eth.getTransactionCount(MY_ACCOUNT)
    ethSendTx = deployedContract.functions.send().buildTransaction(
        {

            'nonce': nonce
        }
    )
    print(ethSendTx)
    signed_tx = w3.eth.account.signTransaction(
        ethSendTx, private_key=PRIVATE_KEY)
    hexTxHash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print('eth send tx sent')
    receipt = w3.eth.waitForTransactionReceipt(hexTxHash.hex())
    print('eth send receipt found!')
    print(receipt)
    print('done')


def fundContractTxHash(w3, deployedContract):
    nonce = w3.eth.getTransactionCount(MY_ACCOUNT)
    tx = deployedContract.functions.deposit().buildTransaction(
        {
            'value': 88888777,
            'nonce': nonce}
    )

    signed_tx = w3.eth.account.signTransaction(tx, private_key=PRIVATE_KEY)
    hexTxHash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print('fund tx sent')
    receipt = w3.eth.waitForTransactionReceipt(hexTxHash.hex())
    print('fund tx receipt found!')

    return dict(
        txHash=receipt.transactionHash.hex(),
    )


def newContractReceipt(w3, contract, receiverAddress):
    '''
    Create the contract
    Return the txHash and address of the new contract
    '''
    nonce = w3.eth.getTransactionCount(MY_ACCOUNT)
    print('nonce')
    print(nonce)
    tx = contract.constructor(receiverAddress).buildTransaction(
        {
            'nonce': nonce
        }
    )

    signed_tx = w3.eth.account.signTransaction(tx, private_key=PRIVATE_KEY)
    hexTxHash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print('new contract tx sent')
    receipt = w3.eth.waitForTransactionReceipt(hexTxHash.hex())
    print('new contract tx receipt found!')

    return dict(
        txHash=receipt.transactionHash.hex(),
        contractHash=receipt.contractAddress
    )


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

                    address payable public receiver;
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

                    function send() public returns (bool){
                        return receiver.send(9911);
                    }

                    function deposit() public payable {
                        sendVal = uint256(msg.value);
                    }

                    function retrieve() public view returns (uint256){
                        return sendVal;
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
