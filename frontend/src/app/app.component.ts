import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  data: any;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get('http://127.0.0.1:5000').subscribe(data => {
      this.data = data;
      console.log(this.data);
    });


    // for (let i in this.data) {
    //   console.log(i);
    // }
  }
}
