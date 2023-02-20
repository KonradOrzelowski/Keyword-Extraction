import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';

import { DataService } from './data.service';

import { HttpClientModule } from '@angular/common/http';
import { PageNetworkGraphComponent } from './page-network-graph/page-network-graph.component';
import { PageFootballerDetailsComponent } from './page-footballer-details/page-footballer-details.component';
import { AppRoutingModule } from './app-routing.module';

@NgModule({
  declarations: [
    AppComponent,
    PageNetworkGraphComponent,
    PageFootballerDetailsComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule
  ],
  providers: [DataService], // add the DataService to the providers array
  bootstrap: [AppComponent]
})
export class AppModule { }
