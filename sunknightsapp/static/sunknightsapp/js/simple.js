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
			    console.log(data);
				handler(true, data);
		}
	});
}

var ajaxusersearchoptions = {
    ajax          : {
        url     : ajaxretrieveuserurl,

        type    : 'POST',
        dataType: 'json',
        headers: {
            'X-CSRFToken': $.cookie('csrftoken')
        },
        // Use "{{{q}}}" as a placeholder and Ajax Bootstrap Select will
        // automatically replace it with the value of the search query.
        data    : {
            searchusers: '{{{q}}}',
            ajax_action_id:ajaxretrieveuserstofightagainstid.RETRIEVEUSERSTOFIGHTAGAINST
        }
    },
    locale        : {
        emptyTitle: 'Select and Begin Typing'
    },
    log           : 3,
    preprocessData: function (data) {
    	data=data['message']['data'];
        var i, l = data.length, array = [];
        if (l) {
            for (i = 0; i < l; i++) {
                array.push($.extend(true, data[i], {
                    text : data[i].discord_nickname+"#"+data[i].discord_discriminator,
                    value: data[i].id,
                }));
            }
        }
        // You must always return a valid array when processing data. The
        // data argument passed is a clone and cannot be modified directly.
        return array;
    }
};

function showhide(button, id){
  var target = document.getElementById(id);
  target.style.display = target.style.display=="none"?"block":"none";
  button.innerHTML = button.innerHTML=="View"?"Hide":"View";
}

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})
