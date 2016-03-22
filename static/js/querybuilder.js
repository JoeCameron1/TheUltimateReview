$(document).ready( function() {
	var no = 0;
	var curQue = ""
	$('button[id="addButton"]').click( function() {
		no = no + 1;
		var toAdd = $('input[name=queryBox]').val();
		var type = $('select[name=fieldType]').val();
		var eType = $('select[name=entryType]').val();
		if (no == 1) {
			$('.queries').html('<div class="item">'  + toAdd + type + " " + '</div>');
			curQue = (toAdd + type);
		} else{
				$('.queries').html('<div class="item">(' + curQue + ") "  + eType + " " + toAdd +type + ' </div>');
				curQue = ('(' + curQue + ") "  + eType + " " + toAdd + type);
		}
		$('textarea[id="queryID"]').val('(' + curQue + ")") 
	});
	$('button[id="queryAddButton"]').click( function() {
		$('textarea[id="queryID"]').prepend($('select[name=entryType]').val() + " (");
		$('textarea[id="queryID"]').append($(this).val() + ")");
	});
});
