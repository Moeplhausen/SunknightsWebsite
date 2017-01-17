/**
 * Ajax requests to /ajaxhandler/
 * @param param paras for the request (command, id, …)
 * @param handler Handler for the answer as function(bool result, object data)
 * @param contentType Content-Type
 * @param processData param
 */
function sunKnightsJsonRequest(param, handler, contentType, processData) {
	contentType = typeof contentType !== 'undefined' ?
			contentType : 'application/x-www-form-urlencoded; charset=UTF-8';
	processData = typeof processData !== 'undefined' ?
			processData : true;
	jQuery.ajax('/ajaxhandler/', {
		'type': 'POST',
		'data': param,
		'cache': false,
		'contentType': contentType,
		'processData': processData,
		'headers': {
			'X-CSRFToken': $.cookie('csrftoken')
		},
		'dataType': 'json',
		'error': function(response, textStatus, errorThrown) {
			// Fehler bei der Anfrage
			var result = {
				'status': 'failure',
				'response': errorThrown + ': ' + response.status + '; ' + response.statusText
			};
			console.log(result);
			handler(false, result);
		},
		'success': function(data, textStatus, response) {
			if (data.status != 'success') {
				// Server-seitiger Fehler
				console.log(data);
				handler(false, data);
			} else
			    console.log(data)
				handler(true, data);
		}
	});
}

