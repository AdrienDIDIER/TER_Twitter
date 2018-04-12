var formatTime = d3.time.format("%H:%M");

var bins = [];
for(var i = 0; i <= freq_per_date.length-1; i++) {
    bins.push(formatTime(new Date(1000 * freq_per_date[i].start_date)));
    bins.push(formatTime(new Date(1000 * freq_per_date[i].stop_date)));
}
var dates = []
for(var i = 0; i <= freq_per_date.length-1; i++) {
    dates.push(freq_per_date[i].start_date);
    dates.push(freq_per_date[i].stop_date);
}
var width = 500;

var freq = [];
for(var i = 0; i <= freq_per_date.length -1; i++){
    freq.push(freq_per_date[i].freq);
}
var height = d3.max(freq);
var svg = d3.select('div.duration').append('svg')
    .attr("width", width+200)
    .attr("height", height+200)
    .attr("transform","translate(100,100)");
var barWidth = (width - (bins.length -1)) / (bins.length-1);
var xScale = d3.scalePoint()
    .range([0, barWidth*freq.length]);
xScale.domain(bins);

var diff = (d3.max(dates) - d3.min(dates)) / dates.length;

var color = d3.scale.category20c();
var xAxis = d3.axisBottom().scale(xScale).ticks(5);

svg.selectAll('rect').data(freq).enter().append('rect')
    .attr("width",barWidth)
    .attr('height' , function(d) { return d;})
    .attr('x' , function(d,i){ return i*barWidth;})
    .attr('y', function(d){ return height - d;})
    .attr("transform", "translate(50,20)")
    .attr("fill", function(d, i) {
            return color(i);})
    .attr('id', function (d,i) {  return i;
    })

    .on("mouseover", function() {
            d3.select(this)
            	.attr("fill", "red");})
    .on("mouseout", function(d, i) {
        d3.select(this).attr("fill", function() {
            return "" + color(this.id) + "";});
    })
    .on("click", function(d,i){
        var da = dates[i] + diff*i;
        var s = da + diff;
        d3.json("http://127.0.0.1:5000/result-wordcloud/" + da + "/" + s, function (json) {
            mycloud.stop().words(json).start().on("end", draw(json,"little-wordcloud"));
         });
    });

svg.append("g").call(xAxis)
    .attr("transform", "translate(50," + 155 + ")");

var yScale = d3.scaleLinear()
    .domain([0, d3.max(freq)])
    .range([height, 0]);


var yAxis = d3.axisLeft().scale(yScale);

svg.append("g").call(yAxis)
    .attr("transform", "translate(50," + 20 + ")");

