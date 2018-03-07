var fill = d3.scale.category20();
d3.layout.cloud().size([1000, 1000])
    .words(words)
    .rotate(function() { return ~~(Math.random() * 2) * 9; })
    .fontSize(function(d) { return d.size + 8; })
    .padding(5)
    .on("end", draw)
    .start();
function draw(words) {
    d3.select("body").append("svg")
        .attr("width", 1000)
        .attr("height", 1000)
        .attr("class", "wordcloud")
        .append("g")
        .attr("transform", "translate(400,400)")
        .selectAll("text")
        .data(words)
        .enter().append("text")
        .style("font-family", "Impact")
        .style("font-size", function(d) { return d.size + "px"; })
        .style("fill", function(d, i) { return fill(i); })
        .attr("transform", function(d) {
            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function(d) { return d.text; });
}