import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AdbountyApiService {

  constructor() { }
  apiUrl(endpoint) {
    return 'https://h8a4i8udc3.execute-api.us-east-1.amazonaws.com/prod/' + endpoint;
  }
}
