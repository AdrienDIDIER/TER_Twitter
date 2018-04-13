d3.select("#wordcloud").append("svg")
    .attr("width", 600)
    .attr("height", 600);
d3.select("#little-wordcloud").append("svg")
    .attr("width", 600)
    .attr("height", 600);

var fontsize = d3.scale.log().range([10, 50]);

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
            return d.size * 1 + "px";
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
        .duration(1000)
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
            $('#loading_circle').hide();
            mycloud.stop().words(response).start().on("end", draw(response, "wordcloud"));
        },
        error: function (error) {
            /**/
        }
    });
}

function ajax_freq_per_date(){
    $.ajax({
        url: '/result-freq-per-date/',
        type: 'GET',
        data: { get_param: 'value' },
        dataType: 'json',

        success: function (response) {
           histogram(response);
        },
        error: function (error) {
            /**/
        }
    });
}


$(document).ready(function () {
    ajax_freq_per_date();
    ajax_wordcloud();
});

