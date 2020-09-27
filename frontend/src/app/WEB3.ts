import { Component, OnInit, Inject, InjectionToken } from '@angular/core';

import Web3 from 'web3';

`
- Create a singleton Web3 provider
- Provide at root of this app
- Hit .enable(), which requests the user's approval to link Metamask with this app.
`

export const WEB3 = new InjectionToken<Web3>('web3', {
  providedIn: 'root',
  factory: () => {
    try {
      const provider = ('ethereum' in window) ? window['ethereum'] : Web3.givenProvider;
      console.log('provider');
      console.log(provider);
      provider.enable();
      return new Web3(provider);
    } catch (err) {
      //throw new Error('Non-Ethereum browser detected. You should consider trying Mist or MetaMask!');
      return new Web3('');
    }
  }
});
