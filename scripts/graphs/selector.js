// For some reason Chosen doesn't work with Liquid so we have to add all options manually
function addOptions(results) {
    nameSet = new Set();
    for (const res of results.data) {
        nameSet.add(res.Name);
    }
    for (const name of nameSet) {
        var option = document.createElement("option");
        option.text = name;
        option.value = name;
        var select = document.getElementById("indexes");
        select.appendChild(option);
    }
}

Papa.parse("https://raw.githubusercontent.com/learnedsystems/SOSDLeaderboard/main/_data/latency.csv", {
	download: true,
	complete: function(results) {
		addOptions(results);
        $(".chzn-select").chosen({max_selected_options : 6});
        var startingIndexes = ["RMI", "BTree", "ALEX", "RS"];
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
        var removed_index = currentlySelected[0];
        var buttons = document.getElementsByClassName(`button_${removed_index}`);
        for (const button of buttons) {
            button.innerHTML = "Add";
        }
        currentlySelected.shift();
    }
    $('#indexes').val(currentlySelected);
    $("#indexes").trigger('chosen:updated');
    graphData(obj);
    console.log($('#indexes').val());
}

function removeIndex(index) {
    console.log(`Removing ${index} from plot`);
    var currentlySelected = $("#indexes").val();
    if (!currentlySelected.includes(index)) {
        return;
    }
    var newSelected = currentlySelected.filter(function(value){ return value != index;});
    $('#indexes').val(newSelected);
    $("#indexes").trigger('chosen:updated');
    graphData(obj);
    console.log($('#indexes').val());
}

function toggleIndex(index) {
    var currentlySelected = $("#indexes").val();
    var buttons = document.getElementsByClassName(`button_${index}`);
    if (currentlySelected.includes(index)) {
        removeIndex(index);
        for (const button of buttons) {
            button.innerHTML = "Add";
        }
    } else {
        selectIndex(index);
        for (const button of buttons) {
            button.innerHTML = "Remove";
        }
    }
}

function clearChosen() {
    console.log("Clearing plot");
    var indexes = $("#indexes").val();
    for (const index of indexes) {
        toggleIndex(index);
    }
    $("#indexes").val([]).trigger("chosen:updated");
    console.log($('#indexes').val());
    graphData(obj);
}