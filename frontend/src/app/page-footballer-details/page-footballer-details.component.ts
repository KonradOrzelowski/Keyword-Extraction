import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { DataService } from 'src/app/data.service';

@Component({
  selector: 'app-page-footballer-details',
  templateUrl: './page-footballer-details.component.html',
  styleUrls: ['./page-footballer-details.component.css']
})
export class PageFootballerDetailsComponent implements OnInit {
  data: string  = 'sNo data';

  constructor(private route: ActivatedRoute, private dataService: DataService) { }

  ngOnInit() {
    console.log('++++++++++++++++++');
    this.data = this.dataService.getData(); 
    //console.log(this.dataService.getData());
     // this.data = this.dataService.getData();
     //this.data = this.route.snapshot.paramMap.get('data')!;
      //console.log(this.data);
      console.log('++++++++++++++++++');

  }
}
