function w(s) { document.writeln(s); }
function id(s) { return document.getElementById(s); }
function imgstr(s) { return "<img src=\"" + baseurl + "/static/images/icons/svc_" + s + ".png\" height=20 align=absmiddle>&nbsp;"; }

// handle form cancel
function fcancel() { window.location = "/vfc"; }

// handle form submit
function fsubmit(f) {
    f.elements[0].value = rid;
    f.elements[1].value = id("sp").value;
    f.elements[2].value = id("enabled").checked;
    f.submit();
}

w("<div style=\"padding-top:10px;padding-bottom:0px;\"><b>" + "Forecast" + "</b></div><hr>");
w("<p>Todays High: " + hi + "&deg;F</br>");
w("Todays Precip: " + pre + "  inches </br>");
w("Sunrise: " + srh + ":" + srm + "</p><hr>");

w("<form name=cfc action=cfc method=get><input type=hidden name=rid><input type=hidden name=thresh><input type=hidden name=enabled>");
w("<div style=\"padding-left:5px;padding-right:5px;\">");
w("<p><input type=checkbox name=enabled id=enabled>Enabled</p>");
w("<p>If <select name=type id=type><option value=Temperature>Temperature</option><option value=Precip>Precipitation</option></select>");
w("<select name=eval id=eval><option value='>'>greater than</option><option value='<'>less than</option></select>");
w("<input type=text size=8 id=sp name=thresh> (&deg;F/inches), then ");
w("<select name=action id=action><option value=Enable>Enable</option><option value=Disable>Disable</option></select>");
w("<select name=prog>");
for (pid = 0; pid < nprogs; pid++) {
   w("<option value=" + (pid) + (rule.prog==pid?" selected ":" ")+">" + "Program " + (pid + 1) + "</option>");
}
w("</select>");
w("</div></form>");
w("<p><button style=\"height:36\" onclick=\"fsubmit(cfc)\"><b>Submit</b></button>");
w("<button style=\"height:36\" onclick=\"fcancel()\">Cancel</button></p>");

// Check enabled box by default
id("enabled").checked=true;

// fill in existing rule values
if(rid>-1) {
	if (rule.enabled == "true") {
		id("enabled").checked=true;
	}
    id("sp").value = rule.thresh;
    id("eval").value = rule.eval;
    id("action").value = rule.action;
    id("type").value = rule.type;
}
