let exercise_json = {};
$.ajax({
    url: '/sport',
    type: 'GET',
    async: false,
    success: function (result) {
        console.log("result", result);
        exercise_json = result;
    }
})
// console.log(exercise_json);


var html = '';
var i = 1;
for (var exercise in exercise_json) {
    var nameOfContainer = "chartContainer" + String(i);
    var nameOfId = exercise;
    var title = "The relation between income and " + nameOfId;
    var nameOfChart = "chartdiv" + String(i);
    i += 1;
    html += '<chartContainer id="' + nameOfContainer + '",class="chartContainer"><h2 id="' +
        nameOfId + '">' + title + '</h2><div id="' + nameOfChart + '"></div></chartContainer>';

}
document.getElementById('charts').innerHTML = html;

am4core.ready(function () {
    // Themes begin
    am4core.useTheme(am4themes_dataviz);
    am4core.useTheme(am4themes_animated);
    // Themes end

    function getDataPoint(jsonStr) {
        console.log("DataJSON", jsonStr);
        var data = [];
        for (var state in jsonStr) {
            var income = jsonStr[state].income;
            var percent = jsonStr[state].sport_percent;
            data.push({
                income: income,
                exercise_percent: percent
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
        series.dataFields.valueY = "exercise_percent";
        series.dataFields.valueX = "income";

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
    var j = 1;
    for (var exercise in exercise_json) {
        var nameOfChart = "chartdiv" + String(j);
        console.log("chartDiv", nameOfChart);
        dataJSON = exercise_json[exercise];
        createXYChart(data = getDataPoint(dataJSON), nameOfChart);
        j += 1;
    }
});