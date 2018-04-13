function histogram(freq_per_date) {
    var formatTime = d3.time.format("%H:%M");

    var bins = [];
    for (var i = 0; i <= freq_per_date.length - 1; i++) {
        bins.push(formatTime(new Date(1000 * freq_per_date[i].start_date)));
        bins.push(formatTime(new Date(1000 * freq_per_date[i].stop_date)));
    }
    var dates = []
    for (var i = 0; i <= freq_per_date.length - 1; i++) {
        dates.push(freq_per_date[i].start_date);
        dates.push(freq_per_date[i].stop_date);
    }
    var width = 550;

    var freq = [];
    for (var i = 0; i <= freq_per_date.length - 1; i++) {
        freq.push(freq_per_date[i].freq);
    }
    var height = 550;

    var svg = d3.select('div.duration').append('svg')
        .attr("transform", "translate(25,25)");

 var diff = (d3.max(dates) - d3.min(dates)) / dates.length;

    var xScale = d3.scalePoint()
        .range([0, diff * freq.length]);
    xScale.domain(bins);

    var color = d3.scale.category20c();

    svg.attr("width", diff*freq.length + 100)
        .attr("height", height + 50);

    svg.selectAll('rect').data(freq).enter().append('rect')
        .attr("width", diff)
        .attr('height', function (d) {
            return d*2;
        })
        .attr('x', function (d, i) {
            return i * diff;
        })
        .attr('y', function (d) {
            return height - d*2;
        })
        .attr("transform", function(d){ return  "translate("+ 20+",0)";})
        .attr("fill", function (d, i) {
            return color(i);
        })
        .attr('id', function (d, i) {
            return i;
        })

        .on("mouseover", function () {
            d3.select(this)
                .attr("fill", "red");
        })
        .on("mouseout", function (d, i) {
            d3.select(this).attr("fill", function () {
                return "" + color(this.id) + "";
            });
        })
        .on("click", function (d, i) {
            var da = dates[i] + diff * i;
            var s = da + diff;
            d3.json("http://127.0.0.1:5000/result-wordcloud/" + da + "/" + s, function (json) {
                mycloud.stop().words(json).start().on("end", draw(json, "little-wordcloud"));
            });
        });

    svg.append("g")
        .attr("class", "axis axis--x")
      .attr("transform", "translate("+ 20+"," + height + ")")
      .call(d3.axisBottom(xScale));

    var yScale = d3.scaleLinear()
        .domain([0, d3.max(freq) + (10 - (d3.max(freq) % 10))])
        .range([height, height- d3.max(freq) * 2])
        .nice();

    svg.append("g")
      .attr("class", "axis axis--y")
      .call(d3.axisLeft(yScale))
      .attr("transform", "translate("+20+", 0)")
        .append("text")
      .attr("y", 2)
      .attr("dy", "0.71em")
      .attr("text-anchor", "end");

}