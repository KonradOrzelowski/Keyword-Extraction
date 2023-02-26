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

  constructor(private route: ActivatedRoute, private http: HttpClient, private dataService: DataService) { }

  async ngOnInit() {
    console.log('++++++++++++++++++');
    this.data = this.dataService.getData(); 
    
    this.similar_footballers_insta  = await this.fetch_http_endpoint(`http://127.0.0.1:5000/similarity/insta/${this.data}`);
    this.similar_footballers_sofifa = await this.fetch_http_endpoint(`http://127.0.0.1:5000/similarity/sofifa/${this.data}`);

    this.similar_footballers_insta  = this.string2array(this.similar_footballers_insta);
    this.similar_footballers_sofifa = this.string2array(this.similar_footballers_sofifa);

    console.log(this.data);
    console.log(this.similar_footballers_insta);
    console.log(this.similar_footballers_sofifa);
    console.log('++++++++++++++++++');
    


  }
  string2array(inputString: string) {
    try {
      inputString = inputString.replace(/"/g, '');
      const regex = /["{](.*?)[:](.*?)[,}]/g;
      const matches = inputString.matchAll(regex);

      const dataDictArray = Array.from(matches, match => ({ 'Name': match[1], 'Score': parseFloat(match[2]) }));
      return dataDictArray;
    } catch (error) {
      console.error(error);
      return [];
    }
  }
  
  async fetch_http_endpoint(url: string) {
    const response = await this.http.get(url).toPromise();
    return response;
  }
}
