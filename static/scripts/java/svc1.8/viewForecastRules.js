function w(s) {document.writeln(s);}
function id(s){return document.getElementById(s);}
function imgstr(s) {return "<img src=\""+baseurl+"/static/images/icons/svc_"+s+".png\" height=20 align=absmiddle>&nbsp;";}
function link(s) {window.location=s;}

// handle form cancel
function fcancel() {window.location="/vfc";}

// handle form submit
function mod(form, idx) {
  form.elements[0].value = idx;
  form.submit();
}

w("<form name=mfc action=mfc method=get><input type=hidden name=rid></form>");
w("<form name=dfc action=dfc method=get><input type=hidden name=rid></form>");
w("<button style=\"height:44\" onclick=link(\"/\")>"+imgstr("home")+"<b>Home</b></button>");
w("<button style=\"height:44\" onclick=\"mod(mfc,-1)\">"+imgstr("addall")+"<b>Add a New Rule</b></button>");
w("<button style=\"height:44\" onclick=link(\"/fcs\")>"+imgstr("options")+"Settings</button><hr>");
w("<div style=\"padding-top:10px;padding-bottom:0px;\"><b>"+"Forecast"+"</b></div>");
w("<p>Todays High: " + hi +"&deg;F</br>");
w("Todays Precip: " + pre +" inches</p><hr>");

