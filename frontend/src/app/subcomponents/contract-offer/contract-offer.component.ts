import { Component, OnInit, Input } from '@angular/core';
import { AdContractTemplate } from '../../interfaces'

@Component({
  selector: 'app-contract-offer',
  templateUrl: './contract-offer.component.html',
  styleUrls: ['./contract-offer.component.css']
})
export class ContractOfferComponent implements OnInit {

  @Input() adTemplate: AdContractTemplate;
  constructor() { }

  ngOnInit(): void {
  }

}
