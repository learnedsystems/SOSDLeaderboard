// For some reason Chosen doesn't work with Liquid so we have to add all options manually
function addOptions(results) {
    nameSet = new Set();
    for (const res of results.data) {
        if (res.Name != "RS") {
            nameSet.add(res.Name);
        }
    }
    for (const name of nameSet) {
        var option = document.createElement("option");
        option.text = name;
        option.value = name;
        var select = document.getElementById("indexes");
        select.appendChild(option);
    }
}

Papa.parse("https://raw.githubusercontent.com/alhuan/alhuan.github.io/main/_data/latency.csv", {
	download: true,
	complete: function(results) {
		addOptions(results);
        $(".chzn-select").chosen({max_selected_options : 6});
        var startingIndexes = ["RMI", "BTree", "ALEX"]
        $('#indexes').val(startingIndexes);
        $("#indexes").trigger('chosen:updated');
        console.log($('#indexes').val());
        graphData(obj);
	},
    header: true
});

function selectIndex(index) {
    console.log(`Adding ${index} to plot`);
    var currentlySelected = $("#indexes").val();
    if (currentlySelected.includes(index)) {
        return;
    }
    if (currentlySelected.length < 6) {
        currentlySelected.push(index);
    } else {
        currentlySelected.push(index);
        currentlySelected.shift();
    }
    $('#indexes').val(currentlySelected);
    $("#indexes").trigger('chosen:updated');
    graphData(obj);
    console.log($('#indexes').val());
}

function clearChosen() {
    console.log("Clearing plot");
    $("#indexes").val([]).trigger("chosen:updated");
    console.log($('#indexes').val());
    graphData(obj);
}