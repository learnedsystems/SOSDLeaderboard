// TODO: add back RS after RS has been fitted to the new synthetic datasets

starts_checked = [
    "RMI",
    "RBS",
    "BinarySearch",
    "BTree",
    "FAST",
    "PGM",
    "ART",
    "ALEX",
]

readOnly = [
    "RMI",
    "RS",
    "FAST",
    "FST",
    "RBS"
]

for (const indexName of starts_checked) {
    document.getElementById(indexName).checked = true;
}

$(document).ready(function() {
    $('.tables').each( function() {
        $(this).find('tr').each (function() {
            var trow = $(this);
            if (trow.index() > 0) {
                var indexValue = trow.find("td:first").text().trim();
                trow.prepend($(`<td><button onclick="removeIndex('${indexValue}')">Remove plot</button>`));
                trow.prepend($(`<td><button onclick="selectIndex('${indexValue}')">Add plot</button>`));
            } 
        });
    });
    jQuery('input[type="checkbox"][name="filter"]').on('change', filter_magic);
    $("#dataswitch").on('change', filter_magic);
    $('.tables td:nth-child(9), th:nth-child(9)').hide();
    filter_magic();
    $clicks = $(".startClick");
    $clicks.each( function() {
        $(this).click();
        sortfwdind = document.createElement('span');
        sortfwdind.id = "sorttable_sortfwdind";
        sortfwdind.innerHTML = stIsIE ? '&nbsp<font face="webdings">6</font>' : '&nbsp;&#x25BC;';
        $(this).appendChild(sortfwdind);
    })
});