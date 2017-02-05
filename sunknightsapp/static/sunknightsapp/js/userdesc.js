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
  md = md.replace(/&/g, "&amp;");
  var descNode = $(selector);
  var newhtml = sh.makeHtml(md);
  descNode.html(newhtml);
}

function setDesc(selector, inputselec) { /*WIP*/ }