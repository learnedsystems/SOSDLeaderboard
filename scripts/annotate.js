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

