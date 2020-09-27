import { TestBed } from '@angular/core/testing';

import { AdbountyApiService } from './adbounty-api.service';

describe('AdbountyApiService', () => {
  let service: AdbountyApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AdbountyApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
