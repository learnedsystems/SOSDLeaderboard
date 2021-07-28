learned_indexes = [
    "RMI",
    "RS",
    "PGM",
    "ALEX"
]

var filter_magic = function(e) {
    var trs = jQuery(`.tables tbody tr`);
    trs.hide();
    jQuery('input[type="checkbox"][name="filter"]').each(function() {
        if (jQuery(this).is(':checked')) {
            var val = jQuery(this).val();
            trs.each(function() {
                var tr = jQuery(this);
                const td = tr.find('td:nth-child(2)');
                var dataset = tr.find('td:nth-child(8)');
                if (td.text().trim() === val && dataset.text().trim() === $("#dataswitch").val()) {
                    tr.show();
                }
                if (learned_indexes.includes(td.text().trim())) {
                    td.css("font-weight", "bold")
                }
            });
        }
    });
    annotate();
};

function showAllIndexes() {
    jQuery('input[type="checkbox"][name="filter"]').each(function() {
        if (!jQuery(this).is(':checked')) {
            console.log($(this).val());
            $(this).prop('checked', true);
        }
    });
    clearChosen();
    for (const index of starts_plotted) {
        toggleIndex(index);
    }
    $("#indexes").val(starts_plotted).trigger("chosen:updated");
    console.log($('#indexes').val());
    graphData(obj);
    filter_magic();
}

function showReadOnly() {
    jQuery('input[type="checkbox"][name="filter"]').each(function() {
        var val = jQuery(this).val();
        if (readOnly.includes(val)) {
            $(this).prop('checked', true);
        }
        else {
            $(this).prop('checked', false);
        }
    });
    clearChosen();
    indexes_to_show = ["RMI", "RS"];
    for (const index of indexes_to_show) {
        toggleIndex(index);
    }
    $("#indexes").val(indexes_to_show).trigger("chosen:updated");
    console.log($('#indexes').val());
    graphData(obj);
    filter_magic();
}

function showUpdatable() {
    jQuery('input[type="checkbox"][name="filter"]').each(function() {
        var val = jQuery(this).val();
        if (readOnly.includes(val)) {
            $(this).prop('checked', false);
        }
        else {
            $(this).prop('checked', true);
        }
    });
    clearChosen();
    indexes_to_show = ["BinarySearch", "BTree", "ALEX"];
    for (const index of indexes_to_show) {
        toggleIndex(index);
    }
    $("#indexes").val(indexes_to_show).trigger("chosen:updated");
    console.log($('#indexes').val());
    graphData(obj);
    filter_magic();
}