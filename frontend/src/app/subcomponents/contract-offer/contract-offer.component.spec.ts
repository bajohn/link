import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ContractOfferComponent } from './contract-offer.component';

describe('ContractOfferComponent', () => {
  let component: ContractOfferComponent;
  let fixture: ComponentFixture<ContractOfferComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ContractOfferComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ContractOfferComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
