var ANSWER_FORMAT = '<input type="radio" name="q" value="a"> {0} <br>\n' +
					'<input type="radio" name="q" value="b"> {1} <br>\n' +
			        '<input type="radio" name="q" value="c"> {2} <br>\n' +
			        '<input type="radio" name="q" value="d"> {3} <br>\n' +
			        '<input type="radio" name="q" value="e"> {4} <br>\n';
var JSON_URL = "https://python-question-gen.herokuapp.com";
var QUESTION_TYPES = ["exp", "slice", "list", "str", "dict", "class", "io"]
var chosen;
var question;

String.Format = function (b) {
    var a = arguments;
    return b.replace(/(\{\{\d\}\}|\{\d\})/g, function (b) {
        if (b.substring(0, 2) == "{{") return b;
        var c = parseInt(b.match(/\d/)[0]);
        return a[c + 1]
    })
};

function getJson(ext) {
	$.ajax({
		type: "GET",
		url: JSON_URL + ext,
		dataType: "json",
		success: callback,
		error: function (err) {
			alert("AJAX error in request: " + JSON.stringify(err, null, 2));
		}
	});
}

function callback(response) {
	question = response;
	populateQuestion();
	$("#submit").show();
}

function nextQuestion() {
	$("#submit").hide()
	$("#frm").hide()
	$("#question").html("Loading question...")
	var i = Math.floor(Math.random()*chosen.length)
	getJson("/" + chosen[i])
}

function populateQuestion() {
	var question_text = question["question"].replace(/(?:\r\n|\r|\n)/g, '<br />').replace(/\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;')
	$("#question").html(question_text);
	$("#frm").html(String.Format(ANSWER_FORMAT, 
		question["a"], question["b"], question["c"], question["d"], question["e"]));
	$("#frm").show()
}

function pressBtn() {
	var query = $('input[name="q"]:checked');
	var selected;
	if(query === null) {
		selected = null;
	} else {
		selected = query.val();
	}
	if(selected === question["ans"]) {
		alert("Correct!");
	} else {
		alert("Sorry, the correct answer was actually " + question[question["ans"]]);
	}
	nextQuestion();
}

function populateSelected() {
	var match,
		pl = /\+/g,
		search = /([^&=]+)=?([^&]*)/g,
		decode = function(s) { return decodeURIComponent(s.replace(pl, " ")); },
		query = window.location.search.substring(1);

	chosen = [];
	while(match = search.exec(query)) {
		type = decode(match[1])
		if($.inArray(type, QUESTION_TYPES) > -1) {
			chosen.push(type)
		}
	}

	if(chosen.length === 0) {
		$("#submit").hide()
		$("#refresh").hide()
		$("#question").html("Question could not be loaded due to an invalid URL")
	} else {
		nextQuestion();
	}
}

function toMenu() {
	window.location.replace("./menu.html")
}

window.onload = populateSelected;