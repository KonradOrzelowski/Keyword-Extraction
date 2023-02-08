


// Get graph "svg" from html with with and height
var svg = d3.select("svg"), width = +svg.attr("width"), height = +svg.attr("height");

// creates a color scale using D3's scaleOrdinal function.
var color = d3.scaleOrdinal(d3.schemeCategory10);

// creates a force simulation with a few forces
// - manyBody which applies a charge to every node which will either attract or repel nodes based on whether they are linked
// - link which applies a force between linked nodes
// - center which applies a force to the center of the graph

/*  The code var simulation = d3.forceSimulation() creates a force simulation in D3.
    A force simulation is a way of modeling the physical forces that govern
    the movement and interactions of objects in a network graph.
*/
var simulation = d3
.forceSimulation().force( "link", d3.forceLink().id(function(d) { return d.id; }).distance(150))
.force("charge", d3.forceManyBody())
.force("center", d3.forceCenter(width / 2, height / 2));


var graph = {
    nodes: [
      { id: "A", x: width / 4, y: height / 2 },
      { id: "B", x: (width / 4) * 3, y: height / 2 },
      { id: "C", x: width / 2, y: (height / 4) * 3 }
    ],
    links: [
      { source: "A", target: "B" },
      { source: "A", target: "C" },
      { source: "B", target: "C" }
    ]
  };


/*
Creates a set of lines that represent the links in the network graph.

 - svg.append("g").attr("class", "links") appends a <g> (group) element to the SVG canvas with the class links.
 - .selectAll("line").data(graph.links) selects all <line> elements and binds them to the data in the graph.links array.
 - .enter().append("line") appends a new <line> element for each data point in graph.links
 - .attr("stroke-width", 2) sets its stroke width to 2 units.

*/

var link = svg.append("g").attr("class", "links")
            .selectAll("line")
            .data(graph.links).enter().append("line")
            .attr("stroke-width", 2);

/*
Creates a set of circles that represent the nodes in the network graph.
 - svg.append("g").attr("class", "nodes") appends a <g> (group) element to the SVG canvas with the class nodes.
 - .selectAll("circle").data(graph.nodes) selects all <circle> elements and binds them to the data in the graph.nodes array.
 - .enter().append("circle")  appends a new <circle> element for each data point in graph.nodes.
 - .attr("r", 10) sets its radius to 10 units
 - .attr("fill", function(d) { return color(d.group); }) sets its fill color using the color scale
                                                         and the group attribute of each node.
 - .call(d3.drag().on("start", dragstarted).on("drag", dragged).on("end", dragended)); is calling
                                                        the D3 drag behavior and registering event handlers for
                                                        the start, drag, and end events.

The drag behavior allows elements to be interactively dragged by the user.
The start, drag, and end events are triggered at the beginning, during, and end of a drag event, respectively.
The dragstarted, dragged, and dragended functions are then called for each node in response to these events.
These functions would typically be used to handle the behavior of the nodes when they are being dragged by the user.
*/
var node = svg.append("g").attr("class", "nodes")
            .selectAll("circle").data(graph.nodes)
            .enter().append("circle")
            .attr("r", 10)
            .attr("fill", function(d) {
                            return color(d.group);})
            .call(d3.drag().on("start", dragstarted)
            .on("drag", dragged).on("end", dragended));


            // node.append("text")
            // .text(function(d) {
            //   return d.id;
            // })
            // .attr("dx", 12)
            // .attr("dy", ".35em")
            // .style("font-size", "10px");


/*
Adding a title element to each node in the graph
and setting the text of the title to the id property of the node data.
The title will be displayed as a tooltip when the user hovers over a node.
*/
node.append("title").text(function(d) {
return d.id;
});
/*
 - sets the nodes for the simulation using simulation.nodes(graph.nodes)
 - registers an event handler for the "tick" event using .on("tick", ticked)

 The tick event is triggered every time the simulation updates its state.
    The ticked function will then be called after each update,
    typically used to update the position of the elements in the graph based on the new state of the simulation.
*/
simulation.nodes(graph.nodes).on("tick", ticked);


/*

- sets the links for the simulation using simulation.force("link").links(graph.links).
    The links represent the connections between nodes in the graph.
*/
simulation.force("link").links(graph.links);



/*
The ticked function is the callback function for the simulation's "tick" event. It's called every time the simulation updates the position of the nodes.

The function updates the position of the nodes by setting the cx and cy attributes of the node elements 
    to the x and y properties of the data objects that correspond to each node.
    It also updates the position of the links by setting the x1, y1, x2, and y2 attributes of the link elements
    to the x and y properties of the source and target data objects that correspond to each link.
*/
function ticked() {

    link.attr("x1", function(d) {
        return d.source.x;
        }).attr("y1", function(d) {
        return d.source.y;
        }).attr("x2", function(d) {
        return d.target.x;
        }).attr("y2", function(d) {
        return d.target.y;
        });

    node.attr("cx", function(d) {
        return d.x;
        }).attr("cy", function(d) {
        return d.y;
        });
}


/*

The dragstarted, dragged, and dragended functions are event listeners for
the drag behavior that is applied to the nodes.

The dragstarted function sets the target alpha to 0.3
    (which affects the strength of the forces in the simulation)
    and sets the fx and fy properties of the data object to the node's current position.
    This fixes the node in place and prevents it from being affected
    by the simulation forces while it's being dragged.

*/
function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();

    d.fx = d.x;
    d.fy = d.y;

}
/*
The dragged function updates the fx and fy properties of the data object
    to the current mouse position during the drag.

*/
function dragged(d) {
    
    d.fx = d3.event.x;
    d.fy = d3.event.y;

}
/*
The dragended function sets the target alpha back to 0
    (to resume the normal strength of the simulation forces)
    and sets the fx and fy properties to null to allow
    the node to be affected by the simulation forces again.

*/
function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);

    d.fx = null;
    d.fy = null;

}
