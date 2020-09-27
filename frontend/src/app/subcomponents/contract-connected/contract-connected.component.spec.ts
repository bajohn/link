import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ContractConnectedComponent } from './contract-connected.component';

describe('ContractConnectedComponent', () => {
  let component: ContractConnectedComponent;
  let fixture: ComponentFixture<ContractConnectedComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ContractConnectedComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ContractConnectedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
