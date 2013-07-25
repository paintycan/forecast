function w(s) { document.writeln(s); }
function id(s) { return document.getElementById(s); }
function imgstr(s) { return "<img src=\"" + baseurl + "/static/images/icons/svc_" + s + ".png\" height=20 align=absmiddle>&nbsp;"; }

// handle form cancel
function fcancel() { window.location = "/vfc"; }

// handle form submit
function fsubmit(f) {
    f.elements[0].value = id("gfh").value;
    f.elements[1].value = id("gfm").value;
    f.elements[2].value = id("key").value;
    f.elements[3].value = id("st").value;
    f.elements[4].value = id("zip").value;
    f.submit();
}

function pad(n) {
    return (n < 10) ? ("0" + n) : n;
}

w("<button style=\"height:44\" onclick=\"fcancel()\">"+imgstr("back")+"Back</button><hr>");
w("<div style=\"padding-top:10px;padding-bottom:0px;\"><b>" + "Forecast Settings" + "</b></div><hr>");
w("<form name=sfc action=cfcs method=get><input type=hidden name=RuntimeHr><input type=hidden name=RuntimeMin>");
w("<input type=hidden name=WundergroundAPIKey><input type=hidden name=State><input type=hidden name=Zip");
w("<div style=\"padding-left:5px;padding-right:5px;\">");
w("Get forecast and apply rules daily at: <input type=text size=2 maxlength=2 id=gfh> : <input type=text size=2 maxlength=2 id=gfm> (hh:mm)<hr>");
w("Wunderground API Key: <input type=text size=20 id=key><br />");
w("State (i.e. CA): <input type=text size=2 maxlength=2 id=st><br />");
w("Zip Code (5 digits): <input type=text size=4 maxlength=5 id=zip><br />");
w("</div></form>");

//fill current values
id("gfh").value = pad(runtimehr);
id("gfm").value = pad(runtimemin);
id("key").value = api;
id("st").value = state;
id("zip").value = zip; 

w("<p><button style=\"height:36\" onclick=\"fsubmit(sfc)\"><b>Submit</b></button>");
w("<button style=\"height:36\" onclick=\"fcancel()\">Cancel</button></p>");
