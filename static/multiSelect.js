$(document).ready(function() {
	$("#objectRightSelected").click(function(){
		$("#object option:selected").each(function(){
			$("#objectSelect").append("<option value=" + $(this).val() + ">" + $(this).html() + "</option>");
			$(this).remove();
        	});
		SortOption("#objectSelect");
	});

	$("#objectLeftSelected").click(function(){    
		$("#objectSelect option:selected").each(function(){
			$("#object").append("<option value=" + $(this).val() + ">" + $(this).html() + "</option>");
			$(this).remove();
		});
		SortOption("#object");
	});
    
	// $("#outDoorRightSelected").click(function(){
	// 	$("#outDoor option:selected").each(function(){
	// 		$("#outDoorSelect").append("<option value=" + $(this).val() + ">" + $(this).html() + "</option>");
	// 		$(this).remove();
	// 	});
	// 	SortOption("#outDoorSelect");
	// });

	// $("#outDoorLeftSelected").click(function(){    
	// 	$("#outDoorSelect option:selected").each(function(){
	// 		$("#outDoor").append("<option value=" + $(this).val() + ">" + $(this).html() + "</option>");
	// 		$(this).remove();
	// 	});
	// 	SortOption("#outDoor");
	// });

	$("#Confirm").click(function() {
		$('#objectSelect option').prop('selected', true);
		// $('#outDoorSelect option').prop('selected', true);

	});
	
	function SortOption(selectName) {
		var $dd = $(selectName);

		if ($dd.length > 0) {
			var selectedVal = $dd.val();
			var $options = $('option', $dd);
			var arrVals = [];
			$options.each(function() {
				arrVals.push({
					text: $(this).text(),
					val: $(this).val()
				});
			});
			
			arrVals.sort(function(a, b) {
				if (a.text > b.text) {
					return 1;
				}
				else if (a.text == b.text) {
					return 0;
				}
				else {
					return -1;
				}
			});
			
			for (var i = 0, l = arrVals.length; i < l; i++) {
				$($options[i]).val(arrVals[i].val).text(arrVals[i].text);
			}	
		}	
    	}
});
