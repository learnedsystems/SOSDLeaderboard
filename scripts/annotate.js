//github url map
let url_map = new Map([
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
    ["ALEX", "https://github.com/microsoft/ALEX"]
]);

// initial displays
$(document).ready(function () {
    $('.group').hide();
    $('#latency-leaderboard').show();
    $('#select').change(function () {
      $('.group').hide();
      $('#'+$(this).val()).show();
    });
  });

// annotate latency table
var $table = $("#latency-table");
$table.find("th").each(function(columnIndex)
{
    var oldValue=Infinity, currentValue=0, $elementToMark=null;
    var minValue = null;
    var $trs = $table.find("tr");
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
                $(this).click( function() {
                    window.open(url_map.get(currentText), "_blank");
                });
            }
            if(!isNaN(currentValue) && currentValue != 0 && currentValue < oldValue)
            {
                $elementToMark = $(this);
            }
            if(index == $trs.length-1)
            {
              if ($elementToMark != null) {
                $elementToMark.css("font-weight", "bold");
                minValue = oldValue;
              }
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
                    $(this).css("background-color", "green");
                }
                else if (currentValue / minValue < 2) {
                    $(this).css("background-color", "#7be095");
                }
                else if (currentValue / minValue < 3) {
                    $(this).css("background-color", "#e3e16d");
                }
                else if (currentValue / minValue < 4) {
                    $(this).css("background-color", "#e3836d");
                }
                else {
                    $(this).css("background-color", "#eb0e0e");
                }
            }
        });
    });
})

