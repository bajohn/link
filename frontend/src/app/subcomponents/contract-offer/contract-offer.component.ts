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
  selector: 'app-contract-offer',
  templateUrl: './contract-offer.component.html',
  styleUrls: ['./contract-offer.component.css']
})
export class ContractOfferComponent implements OnInit {
  faFileSignature = faFileSignature;
  @Input() adTemplate: AdContractTemplate;
  @Input() defaultAccount: string;

  showYoutubeField = false;
  isDeploying = false;
  youtubeId = '';
  youtubeIdValid = true;

  constructor(
    @Inject(WEB3) private web3: Web3,
    private api: AdbountyApiService) { }

  ngOnInit(): void {
  }

  createContractToggle() {
    this.showYoutubeField = !this.showYoutubeField
  }

  async contractToChain() {
    this.youtubeIdValid = true;

    const endpoint = 'youtube-views/' + this.youtubeId;
    const url = this.api.apiUrl(endpoint)
    const resp = await fetch(url);
    const respJson = await resp.json();
    console.log(respJson);
    this.youtubeIdValid = respJson['success'];

    if (this.youtubeIdValid) {
      // Finally, submit to blockchain
      //Setting to variables from Solidity for clarity
      this.isDeploying = true;
      const viewThreshold = this.adTemplate.threshold;
      const paymentAmount = this.adTemplate.payment;
      const buyer = this.adTemplate.owner;
      const seller = this.defaultAccount;
      const durationSec = this.adTemplate.validitySec;
      const youtubeUrl = url;

      const adBountyContract = AdBountyCompiled.abi as AbiItem[]; // explicitly typing, something is wrong with auto-detect

      const rawContract = new this.web3.eth.Contract(adBountyContract);

      const contractToSend = await rawContract.deploy({
        data: AdBountyCompiled.bytecode,
        arguments: [
          viewThreshold,
          paymentAmount,
          buyer,
          seller,
          durationSec,
          youtubeUrl
        ]
      });

      const deployedContract = await contractToSend.send(
        {
          'from': this.defaultAccount
        }
      );
      console.log('Done deploying');
      console.log(deployedContract);
      const address = deployedContract.options.address;
      //const address = '0x4b6d5509f014Eabc4a55aa67D6380E85760929f3';
      // const deployedContract = this.contractFromAddress(address);
      const foundParams = await this.contractParams(deployedContract);

      this.contractToBackend(foundParams.buyer, address);
      this.contractToBackend(foundParams.seller, address);
      this.isDeploying = false;
    }

  }

  allowCreate() {
    return this.defaultAccount !== this.adTemplate.owner;
  }

  contractFromAddress(address: string): Contract {
    const demoContract = AdBountyCompiled.abi as AbiItem[]; // explicitly typing, something is wrong with auto-detect

    return new this.web3.eth.Contract(demoContract, address);
  }

  async contractParams(contract: Contract) {
    const state = await contract.methods.getState().call();
    const buyer = await contract.methods.getBuyer().call();
    const seller = await contract.methods.getSeller().call();

    console.log(state);
    return {
      state,
      buyer,
      seller
    }
  }

  async contractToBackend(userAddress, contractAddress) {
    const endpoint = 'contract/' + userAddress;
    const resp = await fetch(this.api.apiUrl(endpoint), {
      method: 'POST',
      'body': JSON.stringify({
        contractAddress: contractAddress
      })
    });
    console.log(resp);
  }

  async validate() {

  }



}
