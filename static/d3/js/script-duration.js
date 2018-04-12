var values = freq_per_date;
console.log(values);
// Formatters for counts and times (converting numbers to Dates).
//var formatTime = d3.timeFormat("%d %H:%M");
//var start = formatTime(new Date(1000*start_date));
//var stop = formatTime(new Date(1000*stop_date));
var larg =700;
var haut =100;
var barPadding =5;//Padding des barres
var nbb = values.length;//Nb de barres
var lb =((larg - nbb)/nbb)*5;//Largeur barre
var ch =(haut / d3.max(values, function(d){
    return d.freq //Coef. hauteur.
}));
var bins = [];
for(var i in freq_per_date) {
    bins.push(i.start_date);
    bins.push(i.stop_date);
}

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
