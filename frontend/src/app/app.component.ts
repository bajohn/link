import { Component, OnInit, Inject } from '@angular/core';

import Web3 from 'web3';
import { WEB3 } from './WEB3';
import { AbiItem } from 'web3-utils';
const contract = require('truffle-contract');

import * as sampleStore from '../../../build/contracts/SampleStore.json'


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  constructor(@Inject(WEB3) private web3: Web3) { }


  async ngOnInit() {


    const storeContract = sampleStore.abi as AbiItem[]; // explicitly typing, something is wrong with auto-detect

    const contract = new this.web3.eth.Contract(storeContract);
    console.log(contract);
    console.log(contract.methods);

  }

  private async getAccounts() {
    this.web3.eth.getAccounts(console.log)
    const balance = await this.web3.eth.getBalance('0x068528704bAFD8A4B42985Baf87b8877fBea2E35');
    console.log(balance);
    return balance;
  }

}

