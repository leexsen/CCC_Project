let sleep_json = {};
$.ajax({
    url: '/sleep',
    type: 'GET',
    async: false,
    success: function (result) {
        // console.log("result",result);
        sleep_json = result;
        // console.log("result: ", sleep_json);
    }
});
am4core.ready(function () {
    // Themes begin
    am4core.useTheme(am4themes_dataviz);
    am4core.useTheme(am4themes_animated);
    // Themes end

    function getDataPoint1(jsonStr) {
        console.log("DataJSON", jsonStr);
        let data = [];
        for (var state in jsonStr) {
            var age = jsonStr[state].median_age;
            var avg_0_6 = jsonStr[state].average_person_tweet;
            console.log("avg_tweet",avg_0_6);
            data.push({
                median_age: age,
                average_person_tweet: avg_0_6
            });
        }
        return data;
    }

    function getDataPoint2(jsonStr) {
        console.log("DataJSON", jsonStr);
        let data = [];
        for (var state in jsonStr) {
            var age = jsonStr[state].median_age;
            var avg_0_6 = jsonStr[state].average_person_tweet_6_12;
            console.log("avg_tweet",avg_0_6);
            data.push({
                median_age: age,
                average_person_tweet: avg_0_6
            });
        }
        return data;
    }

    function getDataPoint3(jsonStr) {
        console.log("DataJSON", jsonStr);
        let data = [];
        for (var state in jsonStr) {
            var age = jsonStr[state].median_age;
            var avg_0_6 = jsonStr[state].average_person_tweet_12_18;
            console.log("avg_tweet",avg_0_6);
            data.push({
                median_age: age,
                average_person_tweet: avg_0_6
            });
        }
        return data;
    }

    function getDataPoint4(jsonStr) {
        console.log("DataJSON", jsonStr);
        let data = [];
        for (var state in jsonStr) {
            var age = jsonStr[state].median_age;
            var avg_0_6 = jsonStr[state].average_person_tweet_18_24;
            console.log("avg_tweet",avg_0_6);
            data.push({
                median_age: age,
                average_person_tweet: avg_0_6
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

        valueAxis.title.text = "average tweets per person";
        XAxis.title.text = "median age";

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
    console.log("1");
    createXYChart(data=getDataPoint1(sleep_json), "chartdiv1");
    // console.log("2");
    // createXYChart(data=getDataPoint2(sleep_json), "chartdiv2");
    // console.log("3");
    // createXYChart(data=getDataPoint3(sleep_json), "chartdiv3");
    // console.log("4");
    // createXYChart(data=getDataPoint4(sleep_json), "chartdiv4");
});