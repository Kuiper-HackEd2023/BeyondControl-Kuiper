//first add an event listener for page load
document.addEventListener('DOMContentLoaded', get_json_data, false); // get_json_data is the function name that will fire on page load

//this function is in the event listener and will execute on page load
function get_json_data() {
	// Relative URL of external json file
	var json_url = '../gesture_function_map.json';

	//Build the XMLHttpRequest (aka AJAX Request)
	xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200)
			append_json(JSON.parse(this.responseText)); // pass the json object to the append_json function
	};
	//set the request destination and type
	xmlhttp.open('POST', json_url, true);
	//set required headers for the request
	xmlhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	// send the request
	xmlhttp.send(); // when the request completes it will execute the code in onreadystatechange section
}

//this function appends the json data to the table 'gable'
function append_json(data) {

	var table = document.getElementById('gestures-table');
	
	Object.keys(data).forEach(function (gesture) {
		var tr = document.createElement('tr');
		tr.innerHTML =
			'<td>' +
			gesture +
			'</td>' +
			'<td>' +
			data[gesture].function +
			'</td>' +
			'<td>' +
			data[gesture].delay +
			'</td>';
		table.appendChild(tr);
	});
}
