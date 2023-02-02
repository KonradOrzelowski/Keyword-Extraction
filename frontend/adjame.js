import * as d3 from 'https://d3js.org/d3.v6.min.js';

// Your adjacency matrix code here

// Example adjacency matrix
var adjacencyMatrix = [  [0, 1, 1, 0],
  [1, 0, 1, 1],
  [1, 1, 0, 1],
  [0, 1, 1, 0]
];

var nodes = [];
for (var i = 0; i < adjacencyMatrix.length; i++) {
  nodes.push({
    id: i,
    x: Math.random() * 500,
    y: Math.random() * 500
  });
}

var edges = [];
for (var i = 0; i < adjacencyMatrix.length; i++) {
  for (var j = 0; j < adjacencyMatrix[i].length; j++) {
    if (adjacencyMatrix[i][j] === 1) {
      edges.push({
        source: i,
        target: j
      });
    }
  }
}

var svg = d3.select("#graph-container")
  .append("svg")
  .attr("width", 500)
  .attr("height", 500);

var edgeSelection = svg.selectAll("line")
  .data(edges)
  .enter()
  .append("line")
  .attr("x1", function(d) { return nodes[d.source].x; })
  .attr("y1", function(d) { return nodes[d.source].y; })
  .attr("x2", function(d) { return nodes[d.target].x; })
  .attr("y2", function(d) { return nodes[d.target].y; })
  .attr("stroke", "black");

var nodeSelection = svg.selectAll("circle")
  .data(nodes)
  .enter()
  .append("circle")
  .attr("cx", function(d) { return d.x; })
  .attr("cy", function(d) { return d.y; })
  .attr("r", 5)
  .attr("fill", "blue");
