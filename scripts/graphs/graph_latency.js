var obj;
var colors = [];

fetch('https://raw.githubusercontent.com/alhuan/alhuan.github.io/main/_data/all_results.json')
  .then(res => res.json())
  .then(data => obj = data)
  .then(() => console.log(obj))
  .then(() => graphData(obj));

function graphData(obj) {
    var dataset = $("#select").val();
    var indexes = $("#indexes").val();

    if (indexes.length == 0) {
        return;
    }

    var indexData = [];
    for (const index of indexes) {
        if (dataset in obj[index]) {
            indexData.push({
                label: index,
                data: convertSizeLatency(obj[index][dataset]),
                showLine: true
            });
        }
    }

    var ctx = document.getElementById("latencyChart");
    console.log(indexData);
    var chart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: indexData
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Size-Latency Pareto Plot'
            },
            scales: {
                xAxes: [{
                    type: 'logarithmic',
                    position: 'bottom',
                    ticks: {
                        userCallback: function(tick) {
                            var remain = tick / (Math.pow(10, Math.floor(Chart.helpers.log10(tick))));
                            if (remain === 1 || remain === 2 || remain === 5) {
                                return getSizeStr(tick);
                            }
                            return '';
                        },
                    },
                    scaleLabel: {
                        labelString: 'Size',
                        display: true,
                    }
                }],
                yAxes: [{
                    type: 'linear',
                    ticks: {
                        userCallback: function(tick) {
                            return tick.toString() + 'ns';
                        }
                    },
                    scaleLabel: {
                        labelString: 'Latency',
                        display: true
                    }
                }]
            },
            tooltips: {
                mode: 'index'
            },
        }
    });
}

function convertSizeLatency(dataset) {
    result = [];
    for (const dat of dataset) {
        result.push({
            x: dat.size,
            y: dat.latency
        })
    }
    result.sort(function(a, b) {
        return a.x - b.x;
    });
    return result;
}

function getSizeStr(num) {
    if (num < 1e6) {
        return (Math.round(num / 1000)).toString() + " KB";
    } else if (num < 1e9) {
        return (Math.round(num / 1e6)).toString() + " MB";
    } else {
        return (Math.round(num / 1e9)).toString() + " GB";
    }
}

$('#indexes').on('change', function(e) {
    graphData(obj);
})

$("#select").on('change', function(e) {
    graphData(obj);
})