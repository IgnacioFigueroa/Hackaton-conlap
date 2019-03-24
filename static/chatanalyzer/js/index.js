function getchart(){
    $.ajax({
        async: true,
        type:'GET',
        url : '/get_chart_data/',
        dataType : 'json',
        success: function(data){
            console.log(data);
            data1 = data[0];
            prevalent = data[1];
            drawEmotionsChart(data1, prevalent);
        },
        error: function () {
            console.log("i got an error")
        }
    })
}

function drawEmotionsChart(array_for_graph, prev){
    var data = new google.visualization.arrayToDataTable(array_for_graph);
    var options = {
        hAxis: {
          title: 'Time'
        },
        vAxis: {
          title: 'Score'
        },
        backgroundColor: '#f1f8e9'
      };
    var container = document.getElementById('graph');
    var chart = new google.visualization.LineChart(container);
    var images = {'sadness': '/static/chatanalyzer/images/sad_emoji.png',
        'joy': '/static/chatanalyzer/images/happy_emoji.png', 'fear': '/static/chatanalyzer/images/surprised_emoji.png',
        'disgust': '/static/chatanalyzer/images/disgusted_emoji.png', 'anger': '/static/chatanalyzer/images/angry_emoji.png'};
    google.visualization.events.addListener(chart, 'ready', function () {
        var layout = chart.getChartLayoutInterface();
        for (var i = 0; i < data.getNumberOfRows(); i++) {
          // add image above every fifth element
            var xPos = layout.getXLocation(data.getValue(i, 0));
            var yPos = layout.getYLocation(data.getValue(i, 1));



            document.getElementById("img"+(i+1)).src = images[prev[i]];
            document.getElementById('img'+(i+1)).setAttribute("style", "top: (yPos - 16) + 53 + px ; left: (xPos) + 528 + px ; position: absolute; width: 25px; height: 25px");
            document.getElementById("img"+(i+1)).style.top = (yPos - 48) + 'px';
            document.getElementById("img"+(i+1)).style.left = (xPos-490) + 'px';

            console.log(xPos, yPos, 'img'+(i+1), document.getElementById('img'+(i+1)).style.left = (xPos));
            // 16x16 (image size in this example)

        }
      });

    function placeMarker(dataTable) {
        var cli = chart.getChartLayoutInterface();
        var chartArea = cli.getChartAreaBoundingBox();
        // "Zombies" is element #5.
        for (var i = 0; i < data.getNumberOfRows(); i++) {

        }
      };
    google.visualization.events.addListener(chart, 'ready',
        placeMarker.bind(chart, data));

      chart.draw(data, options);
}


$(document).ready(function () {
    $.ajaxSetup({ cache: true });

    // Download the Google JSAPI.
    var url = 'https://www.google.com/jsapi'; //?autoload={"modules":[{"name":"visualization","version":"1"}]}';
    $.getScript(url, function() {
        // When the JSAPI has been loaded, load the appropriate graph charts. When that is done,
        // call the callback to draw whatever chart needs to be drawn.
        google.load("visualization", "1", {'packages': ["corechart"], 'callback': getchart});
    });

});

