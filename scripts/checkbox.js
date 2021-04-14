var filter_magic = function(e) {
    var trs = jQuery(`.tables tbody tr`);
    trs.hide();
    jQuery('input[type="checkbox"][name="filter"]').each(function() {
        if (jQuery(this).is(':checked')) {
            var val = jQuery(this).val();
            trs.each(function() {
                var tr = jQuery(this);
                var td = tr.find('td:nth-child(3)');
                var dataset = tr.find('td:nth-child(9)');
                if (td.text().trim() === val && dataset.text().trim() === $("#dataswitch").val()) {
                    tr.show();
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
    filter_magic();
}