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
        $(".chzn-select").chosen({ max_selected_options: 4});
        var startingIndexes = ["RMI", "BTree", "ALEX"]
        $('#indexes').val(startingIndexes);
        $("#indexes").trigger('chosen:updated');
        console.log($('#indexes').val());
        graphData(obj);
	},
    header: true
});