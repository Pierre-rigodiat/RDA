res_utils_get_id = function(event){
	resultDiv = $(event.target).closest('.xmlResult');
	id = $(resultDiv).parent().attr("id");
	return id;
}