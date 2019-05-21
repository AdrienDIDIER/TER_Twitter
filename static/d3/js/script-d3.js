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
            infoMarker(response.length, session);
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
        async: false,
        success: function (response) {
            if(session != null && session==2){
                $('#loading_circle_polarity2').hide();
            }else{
                $('#loading_circle_polarity').hide();
            }
            createChart(response[0], response[1], response[2],session);

        },
        error: function (error) {
            console.log("ERROR");
        }
    });
}


function createBarChart(words,session){
    if(session != null){
        var valeurID = "#bar_chart" + session;
    }
    else{
        var valeurID = "#bar_chart";
    }
    var data = words.splice(2);
    // set the dimensions and margins of the graph

    const margin = {top: 20, right: 20, bottom: 90, left: 120},
        width = 600 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    const x = d3.scaleBand()
        .range([0, width])
        .padding(0.1);

    const y = d3.scaleLinear()
        .range([height, 0]);

    const svg = d3.select(valeurID).append("svg")
        .attr("id", "svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    const div = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    // Mise en relation du scale avec les données de notre fichier
    // Pour l'axe X, c'est la liste des pays
    // Pour l'axe Y, c'est le max des populations
    x.domain(data.map(function(d) { return d[0]; }));
    y.domain([0, d3.max(data, function(d) { return d[1]; })]);

    // Ajout de l'axe X au SVG
    // Déplacement de l'axe horizontal et du futur texte (via la fonction translate) au bas du SVG
    // Selection des noeuds text, positionnement puis rotation
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickSize(0))
        .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-65)");

    // Ajout de l'axe Y au SVG avec 6 éléments de légende en utilisant la fonction ticks (sinon D3JS en place autant qu'il peut).
    svg.append("g")
        .call(d3.axisLeft(y).ticks(6));

    // Ajout des bars en utilisant les données de notre fichier data.tsv
    // La largeur de la barre est déterminée par la fonction x
    // La hauteur par la fonction y en tenant compte de la population
    // La gestion des events de la souris pour le popup
    svg.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d[0]); })
        .attr("width", x.bandwidth())
        .attr("y", function(d) { return y(d[1]); })
        .attr("height", function(d) { return height - y(d[1]); })
        .on("mouseover", function(d) {
            div.transition()
                .duration(200)
                .style("opacity", .9);
            div.html("Population : " + d[1])
                .style("left", (d3.event.pageX + 10) + "px")
                .style("top", (d3.event.pageY - 50) + "px");
        })
        .on("mouseout", function(d) {
            div.transition()
                .duration(500)
                .style("opacity", 0);
        });
}


function ajax_tweet_frequency_words(session){
    $.ajax({
        url: '/result-frequency-words',
        type: 'GET',
        dataType: 'json',

        success: function (response) {
            if(session==2){
                $('#loading_circle_bar_chart2').hide();
            }else{
                $('#loading_circle_bar_chart').hide();
            }
            createBarChart(response,session);
        },

        error: function(error){
            console.log("ERROR");
        }

    });
}

function ajax_tweet_sunburst(session){
    $.ajax({
        url: '/result-sunburst/',
        type: 'GET',
        dataType: 'json',

        success: function (response) {
            if(session==2){
                $('#loading_circle_sunburst2').hide();
            }else{
                $('#loading_circle_sunburst').hide();
            }
            createSunburst(response[0],response[1],response[2],response[3],response[4],response[5],session);

        },
        error: function (error) {
            console.log("ERROR");
        }

    });

}
