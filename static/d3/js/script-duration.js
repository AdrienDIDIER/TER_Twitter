var ss = freq_per_date;
/*console.log(values);
// Formatters for counts and times (converting numbers to Dates).

var larg =700;
var haut =100;
var barPadding =5;//Padding des barres
var nbb = values.length;//Nb de barres
var lb =((larg - nbb)/nbb)*5;//Largeur barre
var ch =(haut / d3.max(values, function(d){
    return d.freq //Coef. hauteur.
}));


//Creation élément SVG
var svg = d3.select("#duration")
            .append("svg")
            .attr("width", larg)
            .attr("height", haut);

svg.selectAll("rect")
    .data(values)
    .enter()
    .append("rect")
    .attr("x", function(d, i){
        return(i * lb);
    })
    .classed("rect", true)
    .attr("y", function(d){
        return haut -(d.freq * ch);
    })
    .attr("width", lb - barPadding)
    .attr("height", function(d){
        return(d.freq * ch);
    })
    .attr("fill", function(d){
        return"rgb(0, 0, "+(d.freq*10)+")";
    });

var y = d3.scaleLinear()
          .range([0, haut]);

var x = d3.scaleTime()
          .domain(bins)
          .rangeRound([0, larg]);
y.domain([0, d3.max(values, function(d) { return d.freq; })]);
console.log(x);
svg.selectAll("text")
    .data(values)
    .enter()
    .append("text")
    .text(function(d){
        return d.freq;
    })
    .attr("x", function(d, i){
        return(i * lb)+12;
    })
    .attr("y", function(d){
        return haut -((d.freq * ch)-12);
    })
    .attr("font-family", "sans-serif")
    .attr("font-size", "11px")
    .attr("fill", "white");

svg.append("g")
      .attr("transform", "translate(0," + haut + ")")
      .call(d3.axisBottom(x));

  svg.append("g")
      .call(d3.axisLeft(y));
*/
/*

}
console.log(bins);
var data = [10,20,30,40];


var svg = d3.select('div.duration').append('svg')
    .attr("width", '500px')
    .attr("height", '200px');

var xScale = d3.scalePoint()
    .range([0, 400]);
xScale.domain(bins);
var ticks = d3.range(0, xScale.domain()[1] + 1, 60);
var donnees = d3.layout.histogram()
    .bins(ticks)
    (freq);

var xAxis = d3.axisBottom().scale(xScale).tickValues(ticks).tickFormat();

/*var tickCount = xAxis.ticks()[0];
xScale.ticks(tickCount);
var firstdate = xScale(xScale().ticks(tickCount)[0]);
var secondDate = xScale(xScale().ticks(tickCount)[1]);
var colwidth = secondDate - firstdate;
*/
/*
svg.selectAll('rect').data(freq).enter().append('rect')
    .attr("width", xScale(donnees[0].dx) -1)
    .attr('height' , function(d) { return d-(d/2);})
    .attr('x' , function(d,i){ return i*100;})
    .attr('y', function(d){ return 100 - (d-(d/2));})
    .attr("transform", "translate(50,10)");

svg.append("g").call(xAxis)
    .attr("transform", "translate(50," + 110 + ")");
var yScale = d3.scaleLinear()
    .domain([0, d3.max(freq)])
    .range([200/2, 0])


*/
console.log(freq_per_date);
var formatTime = d3.time.format("%H:%M");

var bins = [];
for(var i = 0; i <= freq_per_date.length-1; i++) {
    console.log(formatTime(new Date(1000 * freq_per_date[i].start_date)));
    console.log(formatTime(new Date(1000 * freq_per_date[i].stop_date)));
    bins.push(formatTime(new Date(1000 * freq_per_date[i].start_date)));
    bins.push(formatTime(new Date(1000 * freq_per_date[i].stop_date)));
    //console.log(freq_per_date[i]);
}
console.log(bins);
var dates = []
for(var i = 0; i <= freq_per_date.length-1; i++) {
    dates.push(freq_per_date[i].start_date);
    dates.push(freq_per_date[i].stop_date);
    //console.log(freq_per_date[i]);
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
            mycloud.stop().words(json,false).start();
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

