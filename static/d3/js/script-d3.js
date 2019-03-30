d3.select("#wordcloud").append("svg")
    .attr("width", 600)
    .attr("height", 600);
d3.select("#little-wordcloud").append("svg")
    .attr("width", 600)
    .attr("height", 600);

var fontsize = d3.scale.log().range([10, 20]);

var mycloud = d3.layout.cloud().size([600, 600])
    .words([])
    .rotate(function () {
        return ~~(Math.random() * 2) * 90;
    })
    .fontSize(function (d) {
        return fontsize(d.size);
    })
    .font("Impact")
    .padding(2);

function draw(words, divElement) {
    var fill = d3.scale.category20();
    var element = d3.select("#" + divElement);
    element.selectAll("svg").selectAll("g")
        .transition()
        .duration(1000)
        .style("opacity", 1e-6)
        .remove();

    element.selectAll("svg")
        .append("g")
        .attr("transform", "translate(300,300)")
        .selectAll("text")
        .data(words)
        .enter().append("text")
        .style("font-family", "Impact")
        .attr("text-anchor", "middle")
        .style("font-size", function (d) {
            return d.size+ "px";
        })
        .style("fill", function (d, i) {
            return fill(i);
        })
        .style("opacity", 1e-6)
        .attr("transform", function (d) {
            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .transition()
        .style("opacity", 1)
        .text(function (d) {
            return d.text;
        });
}

function ajax_wordcloud(){
    $.ajax({
        url: '/result-wordcloud/',
        type: 'GET',
        data: { get_param: 'value' },
        dataType: 'json',

        success: function (response) {
            var stream_button_pressed = $('#start-stream_button').is(":disabled");
            var startdated_button_pressed = $('#start-dated_tweets_button').is(":disabled");
            if(stream_button_pressed || startdated_button_pressed){
                refresh_wordcloud(false);
            }else{
                mycloud.stop().words(response).start().on("end", draw(response, "wordcloud"));
                $('#loading_circle').hide();
            }
        },
        error: function (error) {
            /**/
        }
    });
}

function ajax_geolocalisation(session){
    $.ajax({
        url: '/result-geolocalisation/',
        type: 'GET',
        dataType: 'json',

        success: function (response) {
            clearMarker(session);
            for(var i=0;i<response.length;i++){
                addMarker(response[i],session);
            }
        },
        error: function (error) {
            console.log("ERROR");
        }
    });
}

function createChart(negatif, neutre, positif,session){
    let total = negatif + neutre + positif;
    let neg = (negatif*100)/total;
    let neu = (neutre*100)/total;
    let pos = (positif*100)/total;

    if(session != null){
        var valeurID = "pie_chart" + session;
    }
    else{
        var valeurID = "pie_chart";
    }

    console.log(valeurID);
    var pie = new d3pie(valeurID, {
        "data": {
            "content": [

                {"label":"Negatif","value":neg, "color": "#cb2121"},

                {"label":"Neutre", "value":neu, "color": "#2484c1"},

                {"label":"Positif", "value": pos, "color": "#4daa4b"}

            ]

        }});
}

function ajax_tweet_polarity(session){
     $.ajax({
        url: '/result-tweetpolarity/',
        type: 'GET',
        dataType: 'json',

        success: function (response) {
            $('#loading_circle_polarity').hide();
            createChart(response[0], response[1], response[2],session);

        },
        error: function (error) {
            console.log("ERROR");
        }
    });

}

function ajax_tweet_sunburst(){
     $.ajax({
        url: '/result-sunburst/',
        type: 'GET',
        dataType: 'json',

        success: function (response) {
            console.log("SUCCESS");
        },
        error: function (error) {
            console.log("ERROR");
        }
    });
}
