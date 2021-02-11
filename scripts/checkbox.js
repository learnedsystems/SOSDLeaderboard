starts_checked = [
    "RMI",
    "RS",
    "RBS",
    "BS",
    "BTree",
    "FAST",
    "PGM",
    "ART",
]

for (const indexName of starts_checked) {
    document.getElementById(indexName).checked = true;
}

tables = [
    "latency-table",
    "buildtime-table",
    "size-table"
];

$(document).ready(function() {
    var filter_magic = function(e) {
        for (const table of tables) {
            var trs = jQuery(`#${table} tr:not(:first)`);
            trs.hide();
            jQuery('input[type="checkbox"][name="filter"]').each(function() {
                if (jQuery(this).is(':checked')) {
                    var val = jQuery(this).val();
                    trs.each(function() {
                        var tr = jQuery(this);
                        var td = tr.find('td:nth-child(1)');
                        console.log(td.text().trim());
                        if (td.text().trim() === val) {
                            tr.show();
                        }
                    });
                }
            });
        };
    };

    jQuery('input[type="checkbox"][name="filter"]').on('change', filter_magic);
    filter_magic();
});