import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SandboxComponent } from './sandbox/sandbox.component';
import { MainComponent } from './main/main.component';
import { AboutComponent } from './about/about.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';

import { FormsModule } from '@angular/forms';
import { ContractOfferComponent } from './subcomponents/contract-offer/contract-offer.component';
import { ContractConnectedComponent } from './subcomponents/contract-connected/contract-connected.component';

@NgModule({
  declarations: [
    AppComponent,
    SandboxComponent,
    MainComponent,
    AboutComponent,
    ContractOfferComponent,
    ContractConnectedComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatProgressSpinnerModule,
    MatGridListModule,
    MatButtonModule,
    MatInputModule,
    FormsModule,
    MatCardModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

