function submit() {
	var query = $('input[name="quest"]:checked');
	var params = "?"
	for(var i = 0; i < query.length; i++) {
		if(params != "?") {
			params += "&"
		}
		params += query[i].value
	}
	if(params === "?") {
		alert("Please select at least one topic");
	} else {
		window.location.replace("./question.html" + params)
	}
}