import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';

import { DataService } from 'src/app/data.service';

@Component({
  selector: 'app-page-footballer-details',
  templateUrl: './page-footballer-details.component.html',
  styleUrls: ['./page-footballer-details.component.css']
})
export class PageFootballerDetailsComponent implements OnInit {
  data: string  = 'sNo data';

  similar_footballers_insta : any;
  similar_footballers_sofifa: any;
  atr_sofifa: any;

  constructor(private route: ActivatedRoute, private http: HttpClient, private dataService: DataService) {
    
  }

  async ngOnInit() {
    console.log('++++++++++++++++++');
    this.data = this.dataService.getData();
  
    const similar_footballers_insta_str:any = await this.fetch_http_endpoint(`http://127.0.0.1:5000/similarity/insta/${this.data}`);
    this.similar_footballers_insta = this.string2array(similar_footballers_insta_str);
  
    const similar_footballers_sofifa_str:any = await this.fetch_http_endpoint(`http://127.0.0.1:5000/similarity/sofifa/${this.data}`);
    this.similar_footballers_sofifa = this.string2array(similar_footballers_sofifa_str);

    this.atr_sofifa  = await this.fetch_http_endpoint(`http://127.0.0.1:5000/atr/sofifa/${this.data}`);
    // object to array
    

    

    // json to array
    //this.atr_sofifa = this.string2array(this.atr_sofifa);
    // console.log();
    // console.log(typeof(this.atr_sofifa));

  }
  
  string2array(str2transform: string) {
    str2transform = str2transform.replace(/"/g, '');
    str2transform = str2transform.replace(/{/g, '');
    str2transform = str2transform.replace(/}/g, '');
  
    const temp_array = str2transform.split(",");
  
    const output = [];
    for (let i = 0; i < temp_array.length; i++){
        const [name, dist] =  temp_array[i].split(":");
        output.push([name, parseFloat(dist)]);
    }
  
    return output;
  }
  
  



  
  async fetch_http_endpoint(url: string) {
    const response = await this.http.get(url).toPromise();
    return response;
  }
}
