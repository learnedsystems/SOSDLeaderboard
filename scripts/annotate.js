var url_map = new Map([
    ["RMI", "https://github.com/learnedsystems/RMI"],
    ["RS", "https://github.com/learnedsystems/RadixSpline"],
    ["RBS", "https://github.com/learnedsystems/SOSD/blob/master/competitors/radix_binary_search.h"],
    ["ART", "https://github.com/learnedsystems/SOSD/blob/master/competitors/art_primary_lb.h"],
    ["IBTree", "https://github.com/learnedsystems/SOSD/blob/master/competitors/interpolation_btree.h"],
    ["FST", "https://github.com/christophanneser/FST"],
    ["FAST", "https://github.com/RyanMarcus/fast64"],
    ["PGM", "https://github.com/gvinciguerra/PGM-index"],
    ["BTree", "https://github.com/bingmann/stx-btree"],
    ["Wormhole", "https://github.com/wuxb45/wormhole"],
    ["CuckooMap", "https://github.com/learnedsystems/SOSD/blob/master/competitors/stanford_hash.h"],
    ["RobinHash", "https://github.com/Tessil/robin-map"],
    ["ALEX", "https://github.com/microsoft/ALEX"],
    ["BinarySearch", "https://github.com/learnedsystems/SOSD/blob/master/searches/branching_binary_search.h"]
]);

// initial displays
$(document).ready(function () {
    $('.group').hide();
    $('#latency-leaderboard').show();
    $('#select').change(function () {
      $('.group').hide();
      $('#'+$(this).val()).show();
    });
    annotate();
  });

// annotate latency table
function annotate() {
    var $table = $("#latency-table");
    $table.find("th").each(function(columnIndex)
    {
        var oldValue=Infinity, currentValue=0;
        var minValue = null;
        var $trs = $table.find("tr:visible");
        $trs.each(function(index, element)
        {
            $(this).find("td:eq("+ columnIndex +")").each(function()
            {
                if(!isNaN(currentValue) && currentValue != 0 && currentValue < oldValue)
                oldValue = currentValue;
                currentValue = parseFloat($(this).html());
                let currentText = $(this).html().trim();
                if (url_map.has(currentText)) {
                    $(this).css("cursor", "pointer")
                    $(this).css("text-decoration", "underline");
                    $(this).css("color", "blue");
                    $(this).on("click", function(e) {
                        e.stopImmediatePropagation();
                        window.open(url_map.get(currentText), "_blank");
                    });
                }
                if(!isNaN(currentValue) && currentValue != 0 && currentValue < oldValue)
                {
                    minValue = currentValue;
                }
            });
        });
        $trs.each(function(index, element)
        {
            $(this).find("td:eq("+ columnIndex +")").each(function()
            {
                currentValue = parseFloat($(this).html());
                if(!isNaN(currentValue) && currentValue != 0)
                {
                    if (currentValue == minValue) {
                        $(this).css("font-weight", "bold");
                        $(this).css("background-color", "#00CA08");
                    }
                    else if (currentValue / minValue < 2) {
                        $(this).css("font-weight", "normal");
                        $(this).css("background-color", "#A8F8B8");
                    }
                    else if (currentValue / minValue < 3) {
                        $(this).css("font-weight", "normal");
                        $(this).css("background-color", "#e3e16d");
                    }
                    else if (currentValue / minValue < 4) {
                        $(this).css("font-weight", "normal");
                        $(this).css("background-color", "#F7A441");
                    }
                    else {
                        $(this).css("font-weight", "normal");
                        $(this).css("background-color", "#E15959");
                    }
                }
            });
        });
    })
}