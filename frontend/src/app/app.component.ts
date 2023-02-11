import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import * as d3 from 'd3';



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
      
      const footballer_cor = transformData(this.data);

      let firstElements = [];

      for (let node of footballer_cor) {
        firstElements.push(node.id);
      }

      // // place footballer names in red boxes
      // d3.select("#test-d3").selectAll("div").data(firstElements).enter().append("div").text(d => d)
      // .style("background-color", "red").style("padding", "10px").style("margin", "10px")
      // .style("width", "100px");
      var svg = d3.select("svg"), width = +svg.attr("width"), height = +svg.attr("height");
    

      var graph = { nodes: footballer_cor,
                    link: [
                    {'source': "kalvinphillips", 'target': "jarrodbowen"},
                    {'source': "jarrodbowen", 'target': "philfoden"},
                    {'source': "kalvinphillips", 'target': "philfoden"},
                    ] };

      graph.nodes.forEach(function(d: any, i: number) {
        
        d.x = Math.abs(10*footballer_cor[i].x);
        d.y = Math.abs(10*footballer_cor[i].y);

        console.log(d.x);
      });

      var simulation = d3.forceSimulation(footballer_cor)
      .force("link", d3.forceLink(graph.link).id(function(d: any) { return d.id; }))
      .force("charge", d3.forceManyBody().strength(-10))
      .force("center", d3.forceCenter(width / 2, height / 2));
      
      var link = svg.append("g").selectAll("line")
                    .data(graph.link).enter().append("line")
                    .attr("stroke", "black")
                    .attr("x1", function(d: any) { return d.source.x;})
                    .attr("y1", function(d: any) { return d.source.y;})
                    .attr("x2", function(d: any) { return d.target.x;})
                    .attr("y2", function(d: any) { return d.target.y;})
    
      var node = svg.append("g").selectAll("circle")
                    .data(graph.nodes).enter().append("circle")
                    .attr("r", 5).attr("fill", "red");

      simulation.on("tick", function() {
        link.attr("x1", function(d: any) { return d.source.x; })
            .attr("y1", function(d: any) { return d.source.y; })
            .attr("x2", function(d: any) { return d.target.x; })
            .attr("y2", function(d: any) { return d.target.y; });


        node.attr("cx", function(d: any) { return Math.abs(d.x); })
            .attr("cy", function(d: any) { return Math.abs(d.y); });
      });
    console.log(graph.link);      
    });

  }
}

function transformData(data: any[]): any {
  return data.map(item => {
    return {
      id: item.id,
      x: item.x,
      y: item.y
    };
  });
}
async function get_weighted_edges() {
  const response = await fetch('http://127.0.0.1:5000/weighted_edges');
  const data = await response.json();

  // const data = await response.json().then(data => data.__zone_symbol__value);
  // console.log('This data inside fetch');
  // console.log(data);

  // for (let i = 0; i < data.length; i++) {
  //   console.log(data[i]);
  // }
  
  
  return data;
}