let sleep_json = {};
$.ajax({
    url: 'http://127.0.0.1:5000/sleep',
    type: 'GET',
    async: false,
    success: function (result) {
        // console.log("result",result);
        sleep_json = result;
        // console.log("result: ", sleep_json);
    }
});
console.log(sleep_json);
am4core.ready(function () {
    // Themes begin
    am4core.useTheme(am4themes_dataviz);
    am4core.useTheme(am4themes_animated);
    // Themes end

    function getDataPoint(jsonStr) {
        console.log("DataJSON", jsonStr);
        var data = [];
        for (var state in jsonStr) {
            var age = jsonStr[state].median_age;
            var avg_tweet = jsonStr[state].average_person_tweet;
            data.push({
                median_age: age,
                average_person_tweet: avg_tweet
            });
        }
        return data;
    }

    function createXYChart(data, divName) {
        var chart = am4core.create(divName, am4charts.XYChart);
        chart.data = data;
        // Create axes
        var XAxis = chart.xAxes.push(new am4charts.ValueAxis());
        // XAxis.renderer.minGridDistance = 3;

        var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        // valueAxis.renderer.minGridDistance=1;

        // Create series
        var series = chart.series.push(new am4charts.ColumnSeries());
        series.dataFields.valueY = "average_person_tweet";
        series.dataFields.valueX = "median_age";

        var bullet = series.bullets.push(new am4charts.CircleBullet());
        bullet.circle.radius = 5;
        bullet.circle.fill = am4core.color('blue');

        series.tooltip.pointerOrientation = "vertical";

        chart.cursor = new am4charts.XYCursor();
        chart.cursor.snapToSeries = series;
        chart.cursor.xAxis = XAxis;

        // chart.scrollbarY = new am4core.Scrollbar();
        chart.scrollbarX = new am4core.Scrollbar();
    }

    createXYChart(data = getDataPoint(sleep_json), "chartdiv1");
});