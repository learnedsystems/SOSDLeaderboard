// Click each element that should start off clicked. This script makes sure that tables are 
// all initially sorted by medium and start off with the arrow denoting this

$(document).ready( function() {
    $clicks = $(".startClick");
    $clicks.each( function() {
        $(this).click();
        sortfwdind = document.createElement('span');
        sortfwdind.id = "sorttable_sortfwdind";
        sortfwdind.innerHTML = stIsIE ? '&nbsp<font face="webdings">6</font>' : '&nbsp;&#x25BC;';
        $(this).appendChild(sortfwdind);
    })
})