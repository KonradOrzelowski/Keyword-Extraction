import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { PageNetworkGraphComponent } from './page-network-graph/page-network-graph.component';
import { PageFootballerDetailsComponent } from './page-footballer-details/page-footballer-details.component';

const routes: Routes = [
  {  path: 'details', component: PageFootballerDetailsComponent },
  { path: '', component: PageNetworkGraphComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }