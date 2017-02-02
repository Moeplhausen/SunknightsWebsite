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
function loadMd(markdown) {
  md = markdown.replace(/&/g, "&amp;");
}
function mdToHtml(element,helptext) {
  if (helptext) {
    console.log('lo?');
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
  thing.html("<textarea rows='10' cols='30'>" + md + "</textarea>");
  button.html("Submit");
  button.attr("onclick", "editsubmit(" + elementID + ", this, " + sbuttonID);
  cancelb[0].style.display = "block";
}
function editsubmit(elementID, button, sbuttonID) {
  var idselect = function (theid) {
    return "#" + theid;
  };
  var thing = $(idselect(elementID));
  var oldhtml = thing.html();
  $.post(window.location.href, {
    newmd: oldhtml
  }, function (d, s) {
    console.log(`Status: ${s} (Debug)`);
    window.location = window.location.href;
  });
}
function canceledit(elementID, buttonID, sbutton) {
  window.location = window.location.href;
  /*var idselect = function(theid){ return "#" + theid; };
  var thing = $(idselect(elementID));
  var button = $(idselect(buttonID));
  var oldhtml = thing.html();
  thing.html(mdToHtml(idselect(elementID)));
  button.html("Edit");
  button.attr("onclick", "editor("+elementID+", this, "+ sbutton.attr("id"));
  sbutton[0].style.display = "none";*/
}