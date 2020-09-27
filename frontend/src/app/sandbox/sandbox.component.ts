import { Component, OnInit, Inject } from '@angular/core';

import Web3 from 'web3';
import { Contract } from 'web3-eth-contract';
import { WEB3 } from '../WEB3';
import { AbiItem } from 'web3-utils';
const contract = require('truffle-contract');

// import * as sampleStore from '../../../build/contracts/SampleStore.json'
import * as AdBounty from '../../../../build/contracts/AdBounty.json'
import { Router } from '@angular/router';


@Component({
  selector: 'app-root',
  templateUrl: './sandbox.component.html',
  styleUrls: ['./sandbox.component.css']
})
export class SandboxComponent implements OnInit {

  deployedContract: Contract;
  defaultAccount: string;
  isDeployed = false;
  isLoading = false;
  priceFromChain = -1;

  constructor(
    @Inject(WEB3) private web3: Web3,
    private router: Router
  ) {
    this.initAccount();

  }

  async ngOnInit() {

  }

  private async initAccount() {
    const accounts = await this.web3.eth.getAccounts();
    this.defaultAccount = accounts[0];

    const urlSplit = this.router.url.split('/');
    const idx = urlSplit.indexOf('contract');
    if (idx >= 0) {

      const contractAddress = urlSplit[idx + 1];
      const demoContract = AdBounty.abi as AbiItem[]; // explicitly typing, something is wrong with auto-detect

      this.deployedContract = new this.web3.eth.Contract(demoContract, contractAddress);
      this.isDeployed = true;
    }
  }

  async deployContract() {
    this.isLoading = true;
    const demoContract = AdBounty.abi as AbiItem[]; // explicitly typing, something is wrong with auto-detect

    const contract = new this.web3.eth.Contract(demoContract);

    const contractToSend = await contract.deploy({
      data: AdBounty.bytecode,
      arguments: [
        100,
        678,
        '0x47a50df6f06C1837582a28630eF58fC66d1F25D1',
        '0x068528704bAFD8A4B42985Baf87b8877fBea2E35',
        3600,
        'gN-T6NDWQ1g'
      ]
    })
    console.log(contractToSend);
    const deployedContract = await contractToSend.send(
      {
        'from': this.defaultAccount
      }
    );
    console.log('Done deploying');
    console.log(deployedContract);
    this.deployedContract = deployedContract;
    this.isDeployed = true;
    this.isLoading = false;
  }

  async requestUpdatedPrice() {
    this.deployedContract.methods.requestEthereumPrice().send(
      {
        'from': this.defaultAccount
      }
    );
  }

  async checkState() {
    this.isLoading = true;
    const resp = await this.deployedContract.methods.checkState().call(
      {
        'from': this.defaultAccount
      }
    );
    console.log('recorded price');
    console.log(resp);
    this.priceFromChain = resp;
    this.isLoading = false;
  }

  getContractAddress() {
    if (this.isDeployed) {
      const address = this.deployedContract.options.address;
      return `https://kovan.etherscan.io/address/${address}`;
    } else {
      return '';
    }

  }

  async getViewCount() {
    const resp = await fetch('https://h8a4i8udc3.execute-api.us-east-1.amazonaws.com/prod/gN-T6NDWQ1g')
    const respJson = await resp.json();
    console.log(respJson)
  }

}

