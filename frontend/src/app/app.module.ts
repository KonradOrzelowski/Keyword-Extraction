import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';

import { HttpClientModule } from '@angular/common/http';
import { PageNetworkGraphComponent } from './page-network-graph/page-network-graph.component';
import { PageFootballerDetailsComponent } from './page-footballer-details/page-footballer-details.component';

@NgModule({
  declarations: [
    AppComponent,
    PageNetworkGraphComponent,
    PageFootballerDetailsComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
