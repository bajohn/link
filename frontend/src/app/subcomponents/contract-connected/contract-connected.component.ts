import { Component, OnInit, Input, Inject } from '@angular/core';
import { AdContractTemplate } from '../../interfaces'
import { faFileSignature } from '@fortawesome/free-solid-svg-icons';
import { AdbountyApiService } from 'src/app/services/adbounty-api.service';
import { AbiItem } from 'web3-utils';
import * as AdBountyCompiled from '../../../../../build/contracts/AdBounty.json'
import { Contract } from 'web3-eth-contract';
import { WEB3 } from '../../WEB3';
import Web3 from 'web3';

@Component({
  selector: 'app-contract-connected',
  templateUrl: './contract-connected.component.html',
  styleUrls: ['./contract-connected.component.css']
})
export class ContractConnectedComponent implements OnInit {
  faFileSignature = faFileSignature;
  @Input() contractAddress: string;
  @Input() defaultAccount: string;

  contractInfo = {
    buyer: '',
    seller: '',
    state: '',
    url: ''
  }

  constructor(
    @Inject(WEB3) private web3: Web3,
    private api: AdbountyApiService) { }

  ngOnInit(): void {
    this.render();
  }

  async render() {
    const contract = this.contractFromAddress(this.contractAddress);
    this.contractInfo = await this.contractParams(contract);
  }

  contractFromAddress(address: string): Contract {
    const demoContract = AdBountyCompiled.abi as AbiItem[]; // explicitly typing, something is wrong with auto-detect

    return new this.web3.eth.Contract(demoContract, address);
  }

  parseYoutubeId() {
    const youtubeUrl = this.contractInfo.url;
    if (youtubeUrl.length > 0) {
      const split = youtubeUrl.split('/');
      const videoId = split[split.length - 1];
      return videoId;
    }
    return '';
  }

  async contractParams(contract: Contract) {
    const state = await contract.methods.getState().call();
    const buyer = await contract.methods.getBuyer().call();
    const seller = await contract.methods.getSeller().call();
    const url = await contract.methods.getExternalUrl().call();
    console.log(state);
    return {
      state,
      buyer,
      seller,
      url
    }
  }

  canApprove() {
    console.log(this.contractInfo.buyer)
    console.log(this.defaultAccount)
    return this.contractInfo.buyer === this.defaultAccount;
  }

  doApprove() {
    const contract = this.contractFromAddress(this.contractAddress);
    contract.methods.validate().send(
      {
        'from': this.defaultAccount
      }
    );
  }

  doCheck() {
    const contract = this.contractFromAddress(this.contractAddress);
    contract.methods.requestViewCount().send(
      {
        'from': this.defaultAccount
      }
    );
  }

  isActive() {
    return this.contractInfo.state === 'ACTIVE';
  }

}
