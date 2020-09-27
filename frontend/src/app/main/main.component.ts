import { Component, OnInit, Inject } from '@angular/core';
import Web3 from 'web3';
import { Contract } from 'web3-eth-contract';
import { WEB3 } from '../WEB3';
import { AbiItem } from 'web3-utils';
import { AdbountyApiService } from '../services/adbounty-api.service';
import { AdontractTemplate } from '../interfaces'
import { FormControl, Validators } from '@angular/forms';
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

  loadingMyAds = true;
  myAdTemplates = [];
  addingNewOffering = false;
  newOffering: AdontractTemplate = {
    name: '',
    description: '',
    validityDays: 0,
    validitySec: 0,
    payment: 0,
    threshold: 0

  };
  offeringSubmitError = '';



  constructor(
    @Inject(WEB3) private web3: Web3,
    private api: AdbountyApiService
  ) { }

  async ngOnInit() {
    this.initAccount();
    this.loadMyAds();
  }

  async initAccount() {
    this.loadingEmail = true;
    const accounts = await this.web3.eth.getAccounts();
    this.defaultAccount = accounts[0];
    const endpoint = 'user/' + this.defaultAccount;
    const resp = await fetch(this.api.apiUrl(endpoint));
    const respJson = await resp.json();
    this.contactEmail = respJson['contactEmail'];
    this.error = !respJson['success'];
    this.loadingEmail = false;
  }

  async loadMyAds() {
    this.loadingMyAds = true;
    const accounts = await this.web3.eth.getAccounts();
    this.defaultAccount = accounts[0];
    const endpoint = 'contract-template-owned/' + this.defaultAccount;
    const resp = await fetch(this.api.apiUrl(endpoint));
    const respJson = await resp.json();
    this.myAdTemplates = respJson['templates'];
    this.error = !respJson['success'];
    this.loadingMyAds = false;
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

  toggleAddOffering() {
    this.addingNewOffering = !this.addingNewOffering;
    console.log(this.newOffering);
  }

  validityConvert(inputDays: number) {
    this.newOffering.validitySec = inputDays * 3600 * 24;
  }

  submitOffering() {
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

    }
  }

}
