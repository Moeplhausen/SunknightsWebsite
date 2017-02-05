//User description stuff
try {
  sh;
} catch(err) {
  //sh not defined bcuz ????
  window.sh = new showdown.Converter({
    simplifiedAutoLink: true,
    excludeTrailingPunctuationFromURLs: true,
    strikethrough: true,
    tasklists: true,
    requireSpaceBeforeHeadingText: true,
    tables: true,
    simpleLineBreaks: true
  });
}
try {
  link;
} catch(err) {
  //just in case
  window.link = function(){
    return window.location.href.replace(new RegExp(window.location.hash + "$"), "");
  };
}
function getDesc(selector, md) {
  md = md.replace(/&/g, "&amp;").replace(/[><'"]/g, function(l){
    switch(l) {
      case "<":
        return "&lt;";
      case ">":
        return "&gt;";
      case "'":
        return "&#39";
      default:
        return "&quot;";
    }
  });
  window.descmd = md;
  var descNode = $(selector);
  var newhtml = sh.makeHtml(md);
  descNode.html(newhtml);
}

function editDesc(button, cancelsel, selector/*, inputselec*/) {
  var descNode = $(selector);
  var submit = $("#" + button.id);
  var cancel = $(cancelsel);
  //var input = $(inputselec);
  descNode.html("<textarea class='form-control' id='descinput' rows='10' >"+descmd+"</textarea>");
  submit.html("Submit").attr("onclick", "setDesc(\"#descinput\")");
  cancel.css("display", "block");
}

function cancelDesc(cancelbutton, buttonsel, selector) {
  window.location = link();
  //var descNode = $(selector);
  //var button = $(buttonsel);
  //cancelbutton.css("display", "none");
  //button.html("Edit").attr("editDesc(this, \"#" + cancelbutton.id + "\", \"" + selector + "\")");
  //getDesc(selector, descmd);
}

function setDesc(selector) {
  $.ajax(window.ajaxhandlerurl, {
    type: "POST",
    data: {
      ajax_action_id: window.ajaxactions.CHANGEDESC,
      description: $(selector).val() || "None"
    },
    headers: {
      'X-CSRFToken': $.cookie('csrftoken')
    },
    error: function(res, s, err) {
      console.error("Error while submitting (Status: " + s + "): " + err);
      $("#thealertze").clone().attr("id", "currentalert").css("display", "block").appendTo("#alertspot");
    },
    success: function(d, s, res) {
      console.log("Status: " + s + " (Debug)");
      window.location = link();
    }
  });
}