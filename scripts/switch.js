// switch between datasets

$(document).ready(function () {
    $('.tables td:nth-child(7), tr:nth-child(7), th:nth-child(7)').hide();
    var trs = jQuery(`.tables tr:not(:first)`);
    trs.hide();
    $("#dataswitch").change( function() {
        trs.hide();
        trs.each(function() {
            var tr = $(this);
            var td = tr.find('td:nth-child(7)');
            var dataset = tr.find('td:nth-child(7)');
            if (td.text().trim() == $(this).val()) {
                console.log(td.text().trim());
                tr.show();
            }
        });
    });
});