function getSpecialtyFlowChart() {
        $.ajax({
            async: true,
            type: 'GET',
            url: SAF.api_url + 'specialty_flow_chart_data' ,
            data: {},
            dataType: 'json',
            success: function (data) {
                $('#specialtyFlowChart').show();
                $('#loaderSpecialtyFlowChart').hide();
                var energy = data;
                $('#specialtyFlowChart').empty();
                if (energy['nodes'].length > 0)
                    drawSpecialtyFlowChart(energy);
                else {
                    $('#specialtyFlowChart').html("&nbsp;&nbsp;No hay datos disponibles.");
                }
            },
            error: function (jqXHR, textStatus, errorThrown, rut) {
                SAF.notify('error', 'Error de conexión.');
            }
        });
    }

function drawSpecialtyFlowChart(array_for_graph1) {
          d3.sankey = function() {
          var sankey = {},
              nodeWidth = 24,
              nodePadding = 8,
              size = [1, 1],
              nodes = [],
              links = [];

          sankey.nodeWidth = function(_) {
            if (!arguments.length) return nodeWidth;
            nodeWidth = +_;
            return sankey;
          };

          sankey.nodePadding = function(_) {
            if (!arguments.length) return nodePadding;
            nodePadding = +_;
            return sankey;
          };

          sankey.nodes = function(_) {
            if (!arguments.length) return nodes;
            nodes = _;
            return sankey;
          };

          sankey.links = function(_) {
            if (!arguments.length) return links;
            links = _;
            return sankey;
          };

          sankey.size = function(_) {
            if (!arguments.length) return size;
            size = _;
            return sankey;
          };

          sankey.layout = function(iterations) {
            computeNodeLinks();
            computeNodeValues();
            computeNodeBreadths();
            computeNodeDepths(iterations);
            computeLinkDepths();
            return sankey;
          };

          sankey.relayout = function() {
            computeLinkDepths();
            return sankey;
          };

          sankey.link = function() {
            var curvature = .5;

            function link(d) {
              var x0 = d.source.x + d.source.dx,
                  x1 = d.target.x,
                  xi = d3.interpolateNumber(x0, x1),
                  x2 = xi(curvature),
                  x3 = xi(1 - curvature),
                  y0 = d.source.y + d.sy + d.dy / 2,
                  y1 = d.target.y + d.ty + d.dy / 2;
              return "M" + x0 + "," + y0
                   + "C" + x2 + "," + y0
                   + " " + x3 + "," + y1
                   + " " + x1 + "," + y1;
            }

            link.curvature = function(_) {
              if (!arguments.length) return curvature;
              curvature = +_;
              return link;
            };

            return link;
          };

          // Populate the sourceLinks and targetLinks for each node.
          // Also, if the source and target are not objects, assume they are indices.
          function computeNodeLinks() {
            nodes.forEach(function(node) {
              node.sourceLinks = [];
              node.targetLinks = [];
            });
            links.forEach(function(link) {
              var source = link.source,
                  target = link.target;
              if (typeof source === "number") source = link.source = nodes[link.source];
              if (typeof target === "number") target = link.target = nodes[link.target];
              source.sourceLinks.push(link);
              target.targetLinks.push(link);
            });
          }

          // Compute the value (size) of each node by summing the associated links.
          function computeNodeValues() {
            nodes.forEach(function(node) {
              node.value = Math.max(
                d3.sum(node.sourceLinks, value),
                d3.sum(node.targetLinks, value)
              );
            });
          }

          // Iteratively assign the breadth (x-position) for each node.
          // Nodes are assigned the maximum breadth of incoming neighbors plus one;
          // nodes with no incoming links are assigned breadth zero, while
          // nodes with no outgoing links are assigned the maximum breadth.
          function computeNodeBreadths() {
            var remainingNodes = nodes,
                nextNodes,
                x = 0;

            while (remainingNodes.length) {
              nextNodes = [];
              remainingNodes.forEach(function(node) {
                node.x = node.xPos;
                node.dx = nodeWidth;
                node.sourceLinks.forEach(function(link) {
                  nextNodes.push(link.target);
                });
              });
              remainingNodes = nextNodes;
              ++x;
            }

            //
            //moveSinksRight(x);
            scaleNodeBreadths((width - nodeWidth) / (x - 1));
          }

          function moveSourcesRight() {
            nodes.forEach(function(node) {
              if (!node.targetLinks.length) {
                node.x = d3.min(node.sourceLinks, function(d) { return d.target.x; }) - 1;
              }
            });
          }

          function moveSinksRight(x) {
            nodes.forEach(function(node) {
              if (!node.sourceLinks.length) {
                node.x = x - 1;
              }
            });
          }

          function scaleNodeBreadths(kx) {
            nodes.forEach(function(node) {
              node.x *= kx;
            });
          }

          function computeNodeDepths(iterations) {
            var nodesByBreadth = d3.nest()
                .key(function(d) { return d.x; })
                .sortKeys(d3.ascending)
                .entries(nodes)
                .map(function(d) { return d.values; });

            //
            initializeNodeDepth();
            resolveCollisions();
            for (var alpha = 1; iterations > 0; --iterations) {
              relaxRightToLeft(alpha *= .99);
              resolveCollisions();
              relaxLeftToRight(alpha);
              resolveCollisions();
            }

            function initializeNodeDepth() {
              var ky = d3.min(nodesByBreadth, function(nodes) {
                return (size[1] - (nodes.length - 1) * nodePadding) / d3.sum(nodes, value);
              });

              nodesByBreadth.forEach(function(nodes) {
                nodes.forEach(function(node, i) {
                  node.y = i;
                  node.dy = node.value * ky;
                });
              });

              links.forEach(function(link) {
                link.dy = link.value * ky;
              });
            }

            function relaxLeftToRight(alpha) {
              nodesByBreadth.forEach(function(nodes, breadth) {
                nodes.forEach(function(node) {
                  if (node.targetLinks.length) {
                    var y = d3.sum(node.targetLinks, weightedSource) / d3.sum(node.targetLinks, value);
                    node.y += (y - center(node)) * alpha;
                  }
                });
              });

              function weightedSource(link) {
                return center(link.source) * link.value;
              }
            }

            function relaxRightToLeft(alpha) {
              nodesByBreadth.slice().reverse().forEach(function(nodes) {
                nodes.forEach(function(node) {
                  if (node.sourceLinks.length) {
                    var y = d3.sum(node.sourceLinks, weightedTarget) / d3.sum(node.sourceLinks, value);
                    node.y += (y - center(node)) * alpha;
                  }
                });
              });

              function weightedTarget(link) {
                return center(link.target) * link.value;
              }
            }

            function resolveCollisions() {
              nodesByBreadth.forEach(function(nodes) {
                var node,
                    dy,
                    y0 = 0,
                    n = nodes.length,
                    i;

                // Push any overlapping nodes down.
                nodes.sort(ascendingDepth);
                for (i = 0; i < n; ++i) {
                  node = nodes[i];
                  dy = y0 - node.y;
                  if (dy > 0) node.y += dy;
                  y0 = node.y + node.dy + nodePadding;
                }

                // If the bottommost node goes outside the bounds, push it back up.
                dy = y0 - nodePadding - size[1];
                if (dy > 0) {
                  y0 = node.y -= dy;

                  // Push any overlapping nodes back up.
                  for (i = n - 2; i >= 0; --i) {
                    node = nodes[i];
                    dy = node.y + node.dy + nodePadding - y0;
                    if (dy > 0) node.y -= dy;
                    y0 = node.y;
                  }
                }
              });
            }

            function ascendingDepth(a, b) {
              return a.y - b.y;
            }
          }

          function computeLinkDepths() {
            nodes.forEach(function(node) {
              node.sourceLinks.sort(ascendingTargetDepth);
              node.targetLinks.sort(ascendingSourceDepth);
            });
            nodes.forEach(function(node) {
              var sy = 0, ty = 0;
              node.sourceLinks.forEach(function(link) {
                link.sy = sy;
                sy += link.dy;
              });
              node.targetLinks.forEach(function(link) {
                link.ty = ty;
                ty += link.dy;
              });
            });

            function ascendingSourceDepth(a, b) {
              return a.source.y - b.source.y;
            }

            function ascendingTargetDepth(a, b) {
              return a.target.y - b.target.y;
            }
          }

          function center(node) {
            return node.y + node.dy / 2;
          }

          function value(link) {
            return link.value;
          }

          return sankey;
        };

        energy = array_for_graph1;

        var margin = {top: 100, right: 250, bottom: 6, left: 10},
            width = 1350 - margin.left - margin.right,
            height = 775 - margin.top - margin.bottom;

        var formatNumber = d3.format(",.0f"),
            format = function(d) { return formatNumber(d) + " Alumnos"; },
            color = d3.scaleOrdinal(d3.schemeCategory10);

        var drag = d3.drag()
          .subject(function(d) { return d; })
          .on("start", function() { this.parentNode.appendChild(this); })
          .on("drag", dragmove);

        var svg = d3.select("#specialtyFlowChart").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        svg.append("text")
            .attr("x", 0)
            .attr("y", 0 - (margin.top/2))
            .attr("text-anchor", "start")
            .style("font-size", "16px")
            .style("font-weight", "bold")
            .text("Mapa de flujo de cambios de especialidad y mención por año en la carrera");

        var sankey = d3.sankey()
            .nodeWidth(7)
            .nodePadding(20)
            .size([width, height]);

        var path = sankey.link();

          sankey
              .nodes(energy.nodes)
              .links(energy.links)
              .layout(1000);

          var link = svg.append("g").selectAll(".link")
              .data(energy.links)
              .enter().append("path")
              .attr("class", "link")
              .attr("d", path)
              .style("stroke-width", function(d) { return Math.max(1, d.dy); })
              .style("fill", "none")
              .style("stroke", "#000")
              .style("stroke-opacity", 0.2)
              .sort(function(a, b) { return b.dy - a.dy; })
              .on("mouseover", function(){
                  d3.select(this).style("stroke-opacity", 0.5)
              })
              .on("mouseout", function(){
                  d3.select(this).style("stroke-opacity", 0.2)
              });

          link.append("title")
              .text(function(d) { return d.source.name + " → " + d.target.name + "\n" + format(d.value); });

          var node = svg.append("g").selectAll(".node")
              .data(energy.nodes)
            .enter().append("g")
              .attr("class", "node")
              .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
            .call(drag);

          node.append("rect")
              .attr("height", function(d) { return d.dy; })
              .attr("width", sankey.nodeWidth())
              .style("fill", function(d) { return d.color = color(d.name.replace(/ .*/, "")); })
              .style("stroke", function(d) { return d3.rgb(d.color).darker(2); })
              .style("cursor", "movnonee")
              .style("fill-opacity", 0.9)
              .style("shape-rendering", "crispEdges")
            .append("title")
              .text(function(d) { return d.name + "\n" + format(d.value); });

          node.append("text")
              .attr("x", 6 + sankey.nodeWidth())
              .attr("y", function(d) { return d.dy / 2; })
              .attr("dy", ".35em")
              .attr("text-anchor", "start")
              .style("font-size", "12px")
              .style("font-weight", "bold")
              .attr("transform", null)
              .text(function(d) { return d.name; })
            .filter(function(d) { return d.x < width / 2; })
              .attr("x", 6 + sankey.nodeWidth())
              .attr("text-anchor", "start")
              .style("pointer-events", null)
              .style("text-shadow", "0 1px 0 #fff")
              .style("font-size", "12px")
              .style("font-weight", "bold");

          function dragmove(d) {
            d3.select(this).attr("transform", "translate(" + d.x + "," + (d.y = Math.max(0, Math.min(height - d.dy, d3.event.y))) + ")");
            sankey.relayout();
            link.attr("d", path);
          }

    }
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // Loaded when the docs finishes loading.
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    $(document).ready(function () {
        setTimeout(function(){
        // Load the chart objects, and pass the callback function which will get graph data and draw it.
            SAF.loadChart(getSpecialtyFlowChart);
            $('#specialtyFlowChart').hide();
        }, 500);
    });