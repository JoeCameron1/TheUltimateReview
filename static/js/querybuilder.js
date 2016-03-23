$(document).ready( function() {
	var no = 0;
	var curQue = ""
	$('button[id="addButton"]').click( function() {
	curQue = $('textarea').val()
		no = no + 1
		$('textarea[id="queryIDb"]').val($('textarea[id="queryID"]').val());
		var toAdd = $('input[name=queryBox]').val();
		var type = $('select[name=fieldType]').val();
		var eType = $('select[name=entryType]').val();
		if (no == 1) {
			if ($('textarea').val() == ""){
				curQue = ($('textarea').val() + toAdd + type);
				}
			else 
				{
				curQue = ("(" + $('textarea').val() + ") " + eType + " " + toAdd + type)
				}
		} else{
				curQue = ('(' + curQue + ") "  + eType + " " + toAdd + type);
		}
		$('textarea').val('(' + curQue + ")") 
	});
	$('button[id="queryAddButton"]').click( function() {
		$('textarea[id="queryID"]').append($(this).val() + ")");
		$('textarea[id="queryID"]').prepend($('select[name=entryType]').val() + " (");
	});
	
	$('form[id="saveButton"]').click(function(){
		$('textarea[id="queryIDb"]').val($('textarea[id="queryID"]').val());
	});
});


