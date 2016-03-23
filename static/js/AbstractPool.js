/*
function loadAbstract() {
    var xhttp = new XMLHttpRequest();
    var Abstracter = document.getElementById('AbstractButton').value;


    document.getElementById('AbstractSpace').innerHTML = Abstracter;

   /* xhttp.onreadystatechange = function(){
        if (xhttp.readyState == 4 && xhttp.status == 200){
            document.getElementById("abstractSpace").innerHTML = xhttp.responeText;
        }
    };
    xhttp.open("GET", "/ultimatereview/AbstractPool/", true);
    xhttp.send();
}
*/
$(document).ready(function() {
    $('button[id="AbstractButton"]').click( function() {
        $(AbstractSpace).html("<p>" + $(this).val() + "</p>");
        $('button[name="relevant_button"]').val($(this).val())
        $('button[name="irrelevant_button"]').val($(this).val())
    });
});



