//Helper for loading markdown in the info files
try {
  window.md;
} catch (err) {
  //no window.md? then create one
  window.md = undefined;
}

var sh = new showdown.Converter({
  simplifiedAutoLink: true,
  excludeTrailingPunctuationFromURLs: true,
  strikethrough: true,
  tasklists: true,
  requireSpaceBeforeHeadingText: true,
  tables: true,
  simpleLineBreaks: true
});
function link(){
  return window.location.href.replace(new RegExp(window.location.hash + "$"), "");
}
function loadMd(markdown) {
  md = markdown.replace(/&/g, "&amp;");
}
function mdToHtml(element,helptext) {
  if (helptext) {
    $(element).html(sh.makeHtml(helptext));
  }
  return !!helptext;
}
function editor(elementID, button, sbuttonID) {
  var idselect = function (theid) {
    return "#" + theid;
  };
  var thing = $(idselect(elementID));
  var cancelb = $(idselect(sbuttonID));
  button = $(button);
  var oldhtml = thing.html();
  thing.html("<textarea class='form-control' id='newcontentz' rows='10' >" + md + "</textarea>");
  button.html("Submit");
  button.attr("onclick", "editsubmit('" + elementID + "', this, '" + sbuttonID + "')");
  cancelb[0].style.display = "block";
}
function editsubmit(elementID, button, sbuttonID) {
  var idselect = function (theid) {
    return "#" + theid;
  };
  var thing = $(idselect(elementID));
  var oldhtml = $(idselect("newcontentz")).val();
  $.ajax(link(), {
    type: "POST",
    data: {
      newcontent: oldhtml
    },
    headers: {
      'X-CSRFToken': $.cookie('csrftoken')
    },
    error: function(res, s, err) {
      console.error("Error while submitting (Status: " + s + "): " + err);
      $("#thealert").clone().attr("id", "currentalert").css("display", "block").appendTo("#alertspot");
    },
    success: function(d, s, res) {
      console.log("Status: " + s + " (Debug)");
      window.location = link();
    }
  }/*, function (d, s) {
    console.log(`Status: ${s} (Debug)`);
    window.location = link();
  }*/);
}
function canceledit(elementID, buttonID, sbutton) {
  window.location = link();
  /*var idselect = function(theid){ return "#" + theid; };
  var thing = $(idselect(elementID));
  var button = $(idselect(buttonID));
  var oldhtml = thing.html();
  thing.html(mdToHtml(idselect(elementID)));
  button.html("Edit");
  button.attr("onclick", "editor("+elementID+", this, "+ sbutton.attr("id"));
  sbutton[0].style.display = "none";*/
}