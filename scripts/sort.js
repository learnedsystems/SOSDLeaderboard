// Click each element that should start off clicked

$(document).ready( function() {
    $clicks = $(".startClick");
    $clicks.each( function() {
        $(this).click();
        sortfwdind = document.createElement('span');
        sortfwdind.id = "sorttable_sortfwdind";
        sortfwdind.innerHTML = stIsIE ? '&nbsp<font face="webdings">6</font>' : '&nbsp;&#x25BE;';
        $(this).appendChild(sortfwdind);
    })
})