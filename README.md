# Keyword-Extraction

## Init 
### How to activate backend
``` 
backend\.venv\scripts\activate
flask --app backend\app_flask.py run
```

### How to activate frontend
```
cd frontend
ng serve --open 
```

### How to activate notebook
```
python -m venv projectname
source projectname/bin/activate
pip install ipykernel
ipython kernel install --user --name=projectname
```

## How to add multiple pages

### How to add second page to angular app
1. Create a new component using the Angular CLI by running the following command in your terminal:
```
ng generate component second-page
```
2. Open the app.module.ts file in your src/app directory and import the new component by adding the following line at the top of the file:
``` TypeScript
import { SecondPageComponent } from './second-page/second-page.component';
```
3. Add the new component to the declarations array in the @NgModule decorator:
``` TypeScript
@NgModule({
  declarations: [
    AppComponent,
    SecondPageComponent // <-- Add this line
  ],
  imports: [
    // ...
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
```

4. Create a new route for the new component by opening the app-routing.module.ts file in your src/app directory.
Import the new component and add a new route to the Routes array, like so:
``` TypeScript
import { SecondPageComponent } from './second-page/second-page.component';

const routes: Routes = [
  { path: '', component: AppComponent },
  { path: 'second-page', component: SecondPageComponent } // <-- Add this line
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
```

### Pass data between various pages
1. Create a new service using the Angular CLI by running the following command in your terminal:
```
ng generate service data
```
2. Content of the file data.service.ts file in src/app directory:

    The following example illustrates the creation of a new service named DataService, which contains a private property named myData that stores the data. Additionally, two methods are created to enable the setting and retrieving of the data. The setData() method is utilized for setting the data from the home page, while the getData() method is utilized for retrieving the data in the second page component.

``` TypeScript
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private myData: string;

  constructor() { }

  setData(data: string) {
    this.myData = data;
  }

  getData() {
    return this.myData;
  }
}

```

3. In the page-network-graph.component.ts file, import the DataService service and use it to set the data.

``` TypeScript
import { DataService } from 'src/app/data.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-page-network-graph',
  templateUrl: './page-network-graph.component.html',
  styleUrls: ['./page-network-graph.component.css']
})
export class PageNetworkGraphComponent {

   constructor(private dataService: DataService, ...) {}
   
```

4. Create functions which send data

``` TypeScript
    text_and_node.on("click", (d) => {
      
      // Save data in DataService
      this.sendData(d.target.__data__.id);
      // Move to second page
      this.router.navigate(['/details/:data'], { queryParams: { id: d.target.__data__.id } });
    });
```

5. In the second-page.component.ts file, import the DataService service and use it to retrieve the data:
``` TypeScript
import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';

@Component({
  selector: 'app-second-page',
  templateUrl: './second-page.component.html',
  styleUrls: ['./second-page.component.css']
})
export class SecondPageComponent implements OnInit {
  data: string;

  constructor(private dataService: DataService) { }

  ngOnInit() {
    this.data = this.dataService.getData();
  }
}

```

6. Finally, display the value of the data in the second-page.component.html file
``` HTML
<p>The data passed from the home page is: {{ data }}</p>
```

<!--
py -m pip install --upgrade pip
pip install pandas, numpy, networkx, matplotlib, keybert, sentence-transformers, keyphrase-vectorizers, instaloader, ipykernel
pip install sqlalchemy==1.4


https://bobbyhadz.com/blog/node-await-is-only-valid-in-async-function

-->

