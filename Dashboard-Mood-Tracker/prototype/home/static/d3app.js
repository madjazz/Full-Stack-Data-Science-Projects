
var time_parse = d3.timeParse('%Y-%m-%d %H:%M:%S');
var time_format = d3.timeFormat('%m-%d %H:%M:%S');
var chart_width = 800;
var chart_height = 600;
var padding = 50;

var svg = d3.select('#chart')
    .append('svg')
    .attr('width', chart_width)
    .attr('height', chart_height);


d3.json(url, function(error, data) {
    if (error) {
        console.warn("Error");
        console.warn(error);
        return;
        }
    }).then(function(data){
        createPlot(data)
    });

    function createPlot(data) {

        // Format Dates
        data.forEach(function(e, i){
            data[i].date = time_parse(e.date);
        });

        // Scales
        var x_scale = d3.scaleTime()
            .domain([
                d3.min(data, function(d){
                    return d.date;
                }),
                d3.max(data, function(d){
                    return d.date;
                })
            ])
            .range([padding, chart_width - padding]);

        var y_scale = d3.scaleLinear()
            .domain([
                0, d3.max(data, function(d){
                    return d.rating;
                })
            ])
            .range([chart_height - padding, padding]);

        // Create Axes
        var x_axis = d3.axisBottom(x_scale)
            .ticks(12)
            .tickFormat(time_format);
        var y_axis = d3.axisLeft(y_scale)
            .ticks(5);
        svg.append('g')
            .attr('transform', 'translate(0,' + (chart_height - padding) + ')')
            .call(x_axis);
        svg.append('g')
            .attr('transform', 'translate(' + padding + ',0)')
            .call(y_axis);

        // Create Line
        var line = d3.line()
            .defined(function(d){
                return d.rating;
        })
        .x(function(d){
            return x_scale(d.date);
        })
        .y(function(d){
            return y_scale(d.rating);
        });

        svg.append('path')
            .datum(data)
            .attr('fill', 'none')
            .attr('stroke', '#73FF36')
            .attr('stroke-width', 5)
            .attr('d', line);
    };
