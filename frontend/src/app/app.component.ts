import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import * as d3 from 'd3';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})




export class AppComponent implements OnInit {
  footballer_cor: any;
  weighted_edges: any;

  constructor(private http: HttpClient) {}

  async ngOnInit() {
  
    // get data from backend
    this.weighted_edges = await this.fetch_http_endpoint('http://127.0.0.1:5000/weighted_edges');

    this.footballer_cor = await this.fetch_http_endpoint('http://127.0.0.1:5000');
    this.footballer_cor = this.transform_data(this.footballer_cor);

    // Initialize the graph
    var svg = d3.select("svg"), width = +svg.attr("width"), height = +svg.attr("height");
    var graph = { nodes: this.footballer_cor, link: this.weighted_edges };

      // graph.nodes.forEach((d: any, i: number) => {
        
      //   d.x = Math.abs(10*this.footballer_cor[i].x);
      //   d.y = Math.abs(10*this.footballer_cor[i].y);

      // });
      
      var simulation = this.make_simulation(graph, width, height);
      
      var link = this.make_links(svg, graph);
    
      var node =this.make_nodes(svg, graph);

      this.attach_nodes_links(simulation, link, node);

  }
  async fetch_http_endpoint(url: string) {
    const response = await this.http.get(url).toPromise();
    return response;
  }

  make_simulation(graph: any, width: number, height: number) {
    var simulation = d3.forceSimulation(this.footballer_cor)
    .force("link", d3.forceLink(graph.link).id(function(d: any) { return d.id; }))
    .force("charge", d3.forceManyBody().strength(-25))
    .force("center", d3.forceCenter(width / 2, height / 2));

    return simulation;
  }

  make_links(svg: any, graph: any) {
    var link = svg.append("g").selectAll("line")
                  .data(graph.link).enter().append("line")
                  .attr("stroke", "black")
                  .attr("x1", function(d: any) { return d.source.x;})
                  .attr("y1", function(d: any) { return d.source.y;})
                  .attr("x2", function(d: any) { return d.target.x;})
                  .attr("y2", function(d: any) { return d.target.y;})
    
    return link;
  }

  make_nodes(svg: any, graph: any) {
    var node = svg.append("g").selectAll("circle")
              .data(graph.nodes).enter().append("circle")
              .attr("r", 5).attr("fill", "red");
    // var node = svg.append("g").selectAll("rect")
    // .data(graph.nodes).enter().append("rect")
    // .attr("width", 10).attr("height", 10)
    // .attr("fill", "red");
              
    var label = svg.append("g").selectAll("text")
              .data(graph.nodes).enter().append("text")
              .text(function(d: any) { return d.id; })
              .attr("text-anchor", "middle")
              .attr("dominant-baseline", "central")
              .attr("x", function(d: any) { return d.x; })
              .attr("y", function(d: any) { return d.y; });

      // console.log(label);
    return node;
  }




  attach_nodes_links(simulation: any, link: any, node: any) {
    simulation.on("tick", function() {
      link.attr("x1", function(d: any) { return d.source.x; })
          .attr("y1", function(d: any) { return d.source.y; })
          .attr("x2", function(d: any) { return d.target.x; })
          .attr("y2", function(d: any) { return d.target.y; });


      node.attr("cx", function(d: any) { return Math.abs(d.x); })
          .attr("cy", function(d: any) { return Math.abs(d.y); });
    });
  }

  transform_data(data: any[]): any {
    return data.map(item => {
      return {
        id: item.id,
        x: item.x,
        y: item.y
      };
    });
  }
}

// function transform_data(data: any[]): any {
//   return data.map(item => {
//     return {
//       id: item.id,
//       x: item.x,
//       y: item.y
//     };
//   });
// }