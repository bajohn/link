import { Component, OnInit, Input } from '@angular/core';
import { AdContractTemplate } from '../../interfaces'
import { faFileSignature } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-contract-offer',
  templateUrl: './contract-offer.component.html',
  styleUrls: ['./contract-offer.component.css']
})
export class ContractOfferComponent implements OnInit {
  faFileSignature = faFileSignature;
  @Input() adTemplate: AdContractTemplate;
  @Input() defaultAccount: string;
  constructor() { }

  ngOnInit(): void {
  }

  createContract() {

  }

  allowCreate() {
    return this.defaultAccount !== this.adTemplate.owner;
  }

}
