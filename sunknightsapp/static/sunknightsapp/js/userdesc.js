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
function getDesc(selector, md) {
  md = md.replace(/&(?![^\s;];)/g, "&amp;");
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
  var descNode = $(selector);
  var button = $(buttonsel);
  cancelbutton.css("display", "none");
  button.html("Edit").attr("editDesc(this, \"#" + cancelbutton.id + "\", \"" + selector + "\")");
  getDesc(selector, descmd);
}

function setDesc(selector) {
  //WIP
}