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
    simpleLineBreaks: true,
    extensions: ["tank"]
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
  window.descmd = md;
  var descNode = $(selector);
  var newhtml = sh.makeHtml(md.replace(/&/g, "&amp;").replace(/[><'"]/g, function(l){
    switch(l) {
      case "<":
        return "&lt;";
      case ">":
        return "&gt;";
      case "'":
        return "&apos;";
      default:
        return "&quot;";
    }
  }));
  descNode.html(newhtml);
}

function editDesc(button, cancelsel, selector/*, inputselec*/) {
  var descNode = $(selector);
  var count = $("#charcount");
  var submit = $("#" + button.id);
  var cancel = $(cancelsel);
  //var input = $(inputselec);
  descNode.html("<textarea class='form-control' id='descinput' rows='10' oninput='keyUpEdit(this)'>"+descmd+"</textarea>");
  submit.html("Submit").attr("onclick", "setDesc(\"#descinput\")");
  var theval = $("#descinput").val();
  if (theval.length > 1500/*char limit*/) {
    submit.prop("disabled", true).attr("onclick", "//" + (submit.attr("onclick")));
    count.css("color", "red").html("(" + theval.length + "/1500)");
  } else {
    count.html("(" + theval.length + "/1500)");
  }
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
  var value = $(selector).val() || "None";
  if (value.length > 1500) return;
  $.ajax(window.ajaxhandlerurl, {
    type: "POST",
    data: {
      ajax_action_id: window.ajaxactions.CHANGEDESC,
      description: value
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

function keyUpEdit(area) {
  area = $(area);
  var val = area.val();
  var count = $("#charcount");
  var charlimit = 1500;
  var zebutton = $("#userdescbutton");
  if (val.length > charlimit) {
    zebutton.prop("disabled", true);
    if (!(zebutton.attr("onclick").startsWith("//"))) zebutton.attr("onclick", "//" + (zebutton.attr("onclick")));
    count.css("color", "red").html("(" + val.length + "/1500)");
  } else {
    if (zebutton.prop("disabled")) zebutton.prop("disabled", false);
    if (zebutton.attr("onclick").startsWith("//")) zebutton.attr("onclick", (zebutton.attr("onclick").replace(/^\/\//, "")));
    count.html("(" + val.length + "/1500)");
    count.css("color", "inherit");
  }
}
