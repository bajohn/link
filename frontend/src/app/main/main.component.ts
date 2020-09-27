import { Component, OnInit, Inject } from '@angular/core';
import Web3 from 'web3';
import { Contract } from 'web3-eth-contract';
import { WEB3 } from '../WEB3';
import { AbiItem } from 'web3-utils';
import { AdbountyApiService } from '../services/adbounty-api.service';
import { AdContractTemplate } from '../interfaces'
import { FormControl, Validators } from '@angular/forms';
import { isNull } from 'util';
@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  defaultAccount = '';
  contactEmail = '';
  formEmail = '';
  loadingEmail = true;
  editEmail = false;
  error = false;
  isKovan = true;
  hasMetaMask = true;

  loadingMyAds = true;
  loadingAvailableAds = true;
  loadingContractsConnected = true;

  myAdTemplates: AdContractTemplate[] = [];
  availableAdTemplates: AdContractTemplate[] = [];
  addingNewOffering = false;
  newOffering: AdContractTemplate = {
    name: '',
    description: '',
    validityDays: 0,
    validitySec: 0,
    payment: 0,
    threshold: 0

  };
  offeringSubmitError = '';
  contractsConnected: string[] = []



  constructor(
    @Inject(WEB3) private web3: Web3,
    private api: AdbountyApiService
  ) {
    this.hasMetaMask = !isNull(web3.givenProvider);
  }

  metamaskValid() {
    return this.isKovan && this.hasMetaMask;
  }

  async ngOnInit() {
    await this.initAccount();
    if (this.metamaskValid()) {
      this.loadMyAds();
      this.loadAdsAvailable();
      this.loadContractsConnected();
    }
  }

  async initAccount() {
    this.loadingEmail = true;
    const accounts = await this.web3.eth.getAccounts();
    this.defaultAccount = accounts[0];
    const endpoint = 'user/' + this.defaultAccount;
    const resp = await fetch(this.api.apiUrl(endpoint));
    const respJson = await resp.json();
    this.contactEmail = respJson['contactEmail'];
    const network = await this.web3.eth.net.getNetworkType()
    this.isKovan = network === 'kovan';
    this.error = !respJson['success'];
    this.loadingEmail = false;

    //debug
    const debug = await this.web3.eth.getBalance(this.defaultAccount);
    console.log(debug);
  }

  async loadMyAds() {
    this.loadingMyAds = true;
    const endpoint = 'contract-template-owned/' + this.defaultAccount;
    const resp = await fetch(this.api.apiUrl(endpoint));
    const respJson = await resp.json();
    this.myAdTemplates = respJson['templates'];
    this.error = !respJson['success'];
    this.loadingMyAds = false;
  }

  async loadAdsAvailable() {
    this.loadingAvailableAds = true;
    const endpoint = 'contract-template-available/' + this.defaultAccount;
    const resp = await fetch(this.api.apiUrl(endpoint));
    const respJson = await resp.json();
    this.availableAdTemplates = respJson['templates'];
    this.error = !respJson['success'];
    this.loadingAvailableAds = false;
  }

  async loadContractsConnected() {
    this.loadingContractsConnected = true;
    const endpoint = 'contract/' + this.defaultAccount;
    const resp = await fetch(this.api.apiUrl(endpoint));
    const respJson = await resp.json();
    this.contractsConnected = respJson['contracts'];
    this.error = !respJson['success'];
    this.loadingContractsConnected = false;
  }

  askForEmail() {
    return this.contactEmail.length === 0 && !this.loadingEmail || this.editEmail;
  }

  showWelcome() {
    return this.contactEmail.length > 0 && !this.loadingEmail && !this.editEmail;
  }

  async submitEmail() {
    this.loadingEmail = true;
    const endpoint = 'user/' + this.defaultAccount;
    const resp = await fetch(this.api.apiUrl(endpoint), {
      method: 'POST',
      'body': JSON.stringify({
        contactEmail: this.formEmail
      })
    });
    const respJson = await resp.json();
    this.contactEmail = respJson['contactEmail'] as string;
    this.error = !respJson['success'];
    this.loadingEmail = false;
  }

  checkKey(event: KeyboardEvent) {
    if (event.key === 'Enter') {
      this.submitEmail();
    }
  }

  toggleAdOffering() {
    this.addingNewOffering = !this.addingNewOffering;
    console.log(this.newOffering);
  }

  validityConvert(inputDays: number) {
    this.newOffering.validitySec = inputDays * 3600 * 24;
  }

  submitOfferingClick() {
    this.offeringSubmitError = '';
    const name = this.newOffering.name;
    if (name.length === 0) {
      this.offeringSubmitError = 'Name is required.'
    }
    const description = this.newOffering.description;
    if (description.length === 0) {
      this.offeringSubmitError = 'Description is required.'
    }
    const validitySec = this.newOffering.validitySec;
    if (isNaN(Number(validitySec)) || validitySec <= 0) {
      this.offeringSubmitError = 'Non-zero validity is required.'
    }
    const payment = this.newOffering.payment;
    if (isNaN(Number(payment)) || payment <= 0) {
      this.offeringSubmitError = 'Non-zero payment is required.'
    }
    const threshold = this.newOffering.threshold;
    if (isNaN(Number(threshold)) || threshold <= 0) {
      this.offeringSubmitError = 'Non-zero threshold is required.'
    }

    if (this.offeringSubmitError.length === 0) {
      this.doOfferingSubmit();
    }
  }

  async doOfferingSubmit() {
    this.loadingMyAds = true;
    const endpoint = 'contract-template/' + this.defaultAccount;
    const resp = await fetch(this.api.apiUrl(endpoint), {
      method: 'POST',
      'body': JSON.stringify({
        name: this.newOffering.name,
        description: this.newOffering.description,
        validitySec: this.newOffering.validitySec,
        payment: this.newOffering.payment,
        threshold: this.newOffering.threshold,
      })
    });
    const respJson = await resp.json();
    this.myAdTemplates = respJson['templates'];
    this.error = !respJson['success'];
    this.loadMyAds();
    this.addingNewOffering = false;
  }

}
