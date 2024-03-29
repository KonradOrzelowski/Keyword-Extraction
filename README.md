# Keyword-Extraction

This is a web application that scrapes posts from Instagram profiles using Instaloader, extracts keywords from each post using KeyBert, and stores the data in MySQL. The application provides a set of HTTP endpoints using Flask, which can be used to retrieve and display the scraped data. The frontend is built using Angular and displays the results in a user-friendly way.

## Backend
The code creates instances of the KeywordExtraction and SofifaScraping classes, get Instagram posts, extracts and encodes keywords from the posts, creates an adjacency matrix based on the cosine similarity of the encoded keywords, generates a networkx graph based on the adjacency matrix, and creates a list of weighted edges to use in the visualization

The Flask app provides the following endpoints:

- GET /: returns a JSON object containing the positions of the nodes in the networkx graph.
- GET /weighted_edges: returns a JSON object containing a list of weighted edges for the networkx graph.
- GET /similarity/insta/<player_name>: returns a JSON object containing the top 5 Instagram profiles most similar to the specified profile.
- GET /similarity/insta/<player_name>/int:number: returns a JSON object containing the top <number> Instagram profiles most similar to the specified profile.
- GET /similarity/sofifa/<player_name>: returns a JSON object containing the top 5 football players most similar to the specified player.
- GET /similarity/sofifa/<player_name>/int:number: returns a JSON object containing the top <number> football players most similar to the specified player.
- GET /atr/sofifa/<player_name>: returns a JSON object containing the attributes of the specified football player.
- GET /content/key_words/<player_name>: returns a JSON object containing the Instagram posts of the specified profile and their associated keywords.

## Features
- Scrapes Instagram posts using Instaloader and stores them in MySQL
- Extracts keywords from each post using KeyBert, a neural network model designed to find keywords in text
- Provides a set of HTTP endpoints using Flask for retrieving and displaying the scraped data
- Displays the results in a user-friendly way using Angular

## Technologies
- Python
- Instaloader
- KeyBert
- Flask
- Angular
- Javascript/Typescript
- MySQL

## Init 
### How to activate backend
```
cd backend
.venv\scripts\activate
flask --app app_flask.py run
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

