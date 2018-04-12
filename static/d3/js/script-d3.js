 var fill = d3.scale.category20();
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
        .padding(2)
        .on("end", draw)


    function draw(words, divBool) {
        console.log(divBool);
        if(divBool){
            var element = d3.select("#wordcloud");
        }
        else{
            var element = d3.select("#little-wordcloud");
        }


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
    function get_words() {
        //make ajax call
        d3.json("http://127.0.0.1:5000/result-wordcloud/" + keywords, function (json) {
            console.log(json);
            mycloud.stop().words(json,true).start();
        });
    };

    get_words();
    d3.select("#wordcloud").append("svg")
        .attr("width", 600)
        .attr("height", 600)

