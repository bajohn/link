import { Component, OnInit, Input } from '@angular/core';
import { AdContractTemplate } from '../../interfaces'
import { faPause, faFileSignature, faShip, faPlay, faQuestion } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-contract-offer',
  templateUrl: './contract-offer.component.html',
  styleUrls: ['./contract-offer.component.css']
})
export class ContractOfferComponent implements OnInit {
  faFileSignature = faFileSignature;
  @Input() adTemplate: AdContractTemplate;
  constructor() { }

  ngOnInit(): void {
  }

}
