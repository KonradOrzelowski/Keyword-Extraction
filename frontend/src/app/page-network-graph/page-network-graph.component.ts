import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import * as d3 from 'd3';
import { DataService } from 'src/app/data.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-page-network-graph',
  templateUrl: './page-network-graph.component.html',
  styleUrls: ['./page-network-graph.component.css']
})
export class PageNetworkGraphComponent {
  footballer_cor: any;
  weighted_edges: any;

  constructor(private router: Router, private http: HttpClient, private dataService: DataService) {}



  async ngOnInit() {
  
    // get data from backend
    this.weighted_edges = await this.fetch_http_endpoint('http://127.0.0.1:5000/weighted_edges');

    this.footballer_cor = await this.fetch_http_endpoint('http://127.0.0.1:5000');
    this.footballer_cor = this.transform_data(this.footballer_cor);

    // Initialize the graph
    var svg = d3.select("svg"), width = +svg.attr("width"), height = +svg.attr("height");
    var graph = { nodes: this.footballer_cor, link: this.weighted_edges };
      
    var simulation = this.make_simulation(graph, width, height);
    
    var link = this.make_links(svg, graph);

    var text_and_node = svg.append("g").selectAll("g").data(graph.nodes).enter().append("g");
    var circles = text_and_node.append("circle").attr("r", 10).attr("fill", "red");
    var ctexts = text_and_node.append("text").text(function(d: any) { return d.id; });

    text_and_node.on("click", (d) => {
      this.router.navigate(['/details/:data'], { queryParams: { id: d.target.__data__.id } });
      //console.log(d.target.__data__.id);
      this.sendData(d.target.__data__.id);
      console.log('------------------------');
      console.log(this.dataService.getData());
      console.log('------------------------');
      
    });
      

      simulation.on("tick", function() {
        link.attr("x1", function(d: any) { return d.source.x; })
            .attr("y1", function(d: any) { return d.source.y; })
            .attr("x2", function(d: any) { return d.target.x; })
            .attr("y2", function(d: any) { return d.target.y; });
        text_and_node.attr("transform", function(d: any) { return "translate(" + Math.abs(d.x) + "," + Math.abs(d.y) + ")"; });
            // text_and_node.attr("x", function(d: any) { return Math.abs(d.x); })
            // .attr("y", function(d: any) { return Math.abs(d.y); });
          
      });

  }

  async fetch_http_endpoint(url: string) {
    const response = await this.http.get(url).toPromise();
    return response;
  }

  make_simulation(graph: { nodes: any; link: any; }, width: number, height: number) {
    var simulation = d3.forceSimulation(this.footballer_cor)
    .force("link", d3.forceLink(graph.link).id(function(d: any) { return d.id; }))
    .force("charge", d3.forceManyBody().strength(-25))
    .force("center", d3.forceCenter(width / 2, height / 2));

    return simulation;
  }

  make_links(svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>, graph: { nodes: any; link: any; }) {
    var link = svg.append("g").selectAll("line")
                  .data(graph.link).enter().append("line")
                  .attr("stroke", "black")
                  .attr("x1", function(d: any) { return d.source.x;})
                  .attr("y1", function(d: any) { return d.source.y;})
                  .attr("x2", function(d: any) { return d.target.x;})
                  .attr("y2", function(d: any) { return d.target.y;})
    
    return link;
  }

  make_nodes(svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>, graph: { nodes: any; link: any; }) {
    var node = svg.append("g").selectAll("circle")
              .data(graph.nodes).enter().append("circle")
              .attr("r", 5).attr("fill", "red");

    return node;
  }

  make_text(svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>, graph: { nodes: any; link: any; }) {
    var text = svg.append("g").selectAll("text")
    .data(graph.nodes).enter().append("text")
    .text(function(d: any) { return d.id; })
    return text;
  }


  attach_elements(simulation: any, link: any, node: any, text: any) {
    simulation.on("tick", function() {
      link.attr("x1", function(d: any) { return d.source.x; })
          .attr("y1", function(d: any) { return d.source.y; })
          .attr("x2", function(d: any) { return d.target.x; })
          .attr("y2", function(d: any) { return d.target.y; });


      node.attr("cx", function(d: any) { return Math.abs(d.x); })
          .attr("cy", function(d: any) { return Math.abs(d.y); });

      text.attr("x", function(d: any) { return Math.abs(d.x); })
          .attr("y", function(d: any) { return Math.abs(d.y); });

      
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
  sendData(str2pass: string) {
    this.dataService.setData(str2pass);
  }
}

