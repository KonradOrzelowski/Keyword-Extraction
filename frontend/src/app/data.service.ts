import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private myData: string = 'No data in data service';

  constructor() { }

  setData(data: string) {
    this.myData = data;
  }

  getData() {
    return this.myData;
  }
}
