var obj;
var chart;
var colors = ['rgb(255, 99, 132)', 'rgb(54, 162, 235)', 'rgb(255, 205, 86)', 'rgb(14, 249, 68)', 'rgb(167, 20, 169)', 'rgb(14, 249, 244)'];
var error_display = document.getElementById("error_display");
var aggregate_datasets = ["all_uint64", "real_uint64", "all_uint32", "real_uint32", "synthetic_uint64", "synthetic_uint32"]
var dataset_aliases = {
    "all_uint64": "All 64-bit",
    "real_uint64": "Real 64-bit",
    "all_uint32": "All 32-bit",
    "real_uint32": "Real 32-bit",
    "osm_cellids_200M_uint64": "OSM (64-bit)",
    "osm_cellids_200M_uint32": "OSM (32-bit)",
    "fb_200M_uint64": "Facebook (64-bit)",
    "fb_200M_uint32": "Facebook (32-bit)",
    "wiki_ts_200M_uint64": "Wiki (64-bit)",
    "wiki_ts_200M_uint32": "Wiki (32-bit)",
    "books_200M_uint64": "Books (64-bit)",
    "books_200M_uint32": "Books (32-bit)",
    "normal_200M_uint64": "Normal (64-bit)",
    "normal_200M_uint32": "Normal (32-bit)",
    "lognormal_200M_uint64": "Lognormal (64-bit)",
    "lognormal_200M_uint32": "Lognormal (32_bit)",
    "uniform_sparse_200M_uint64": "Uniform sparse (64-bit)",
    "uniform_sparse_200M_uint32": "Uniform sparse (32-bit)",
    "uniform_dense_200M_uint64": "Uniform dense (64-bit)",
    "uniform_dense_200M_uint32": "Uniform dense (32-bit)",
    "osm_cellids_400M_uint64": "OSM (64-bit) 400M",
    "osm_cellids_600M_uint64": "OSM (64-bit) 600M",
    "osm_cellids_800M_uint64": "OSM(64-bit) 800M",
    "books_400M_uint64": "Books (64-bit) 400M",
    "books_600M_uint64": "Books (64-bit) 600M",
    "books_800M_uint64": "Books (64-bit) 800M"
}

fetch('https://raw.githubusercontent.com/learnedsystems/SOSDLeaderboard/main/_data/all_results.json')
  .then(res => res.json())
  .then(data => obj = data)
  .then(() => console.log(obj))
  .then(() => graphData(obj));

function graphData(obj) {
    var dataset = $("#dataswitch").val();
    var indexes = $("#indexes").val();
    var error_strings = [];

    var indexData = [];
    var idx = 0;
    var largestSize = 0;
    for (const index of indexes) {
        if (dataset in obj[index]) {
            var data = convertSizeLatency(obj[index][dataset]);
            largestSize = Math.max(largestSize, data[data.length - 1].x);
        } else {
            error_strings.push(`Error: Index ${index} was not evaluated on selected dataset.`);
        }
    }
    for (const index of indexes) {
        console.log(largestSize);
        if (dataset in obj[index]) {
            var nextPoint = {
                label: index,
                data: convertSizeLatency(obj[index][dataset]),
                showLine: true,
                tension: 0,
                backgroundColor: colors[idx],
                borderColor: colors[idx],
                fill: false
            }
            if (nextPoint.data.length == 1 && nextPoint.data[0].x == 0) {
                nextPoint.data.push({x: largestSize, y: nextPoint.data[0].y});
                console.log(nextPoint.data);
            }
            indexData.push(nextPoint);
            idx++;
        }
    }

    $("#latencyChart").remove();
    $("#latency_plot").append('<canvas id="latencyChart" style="height:500px;width:100%"></canvas>');
    var ctx = document.getElementById("latencyChart");
    console.log(indexData);
    chart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: indexData
        },
        options: {
            responsive: false,
            title: {
                display: true,
                text: `Size-Latency Pareto Plot on dataset ${dataset_aliases[dataset]}`
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
                        labelString: 'Index Size',
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
    while( error_display.firstChild ) {
        error_display.removeChild( error_display.firstChild );
    }
    if (aggregate_datasets.includes(dataset)) {
        error_display.appendChild( document.createTextNode("Plotting aggregate results is not supported. Please select an individual dataset."));
        return;
    }
    for (const error_string of error_strings) {
        error_display.appendChild( document.createTextNode(error_string) );
        error_display.appendChild( document.createElement("br") );
    }
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
    console.log($("#indexes").val());
})

$("#dataswitch").on('change', function(e) {
    graphData(obj);
    console.log($("#dataswitch").val());
})