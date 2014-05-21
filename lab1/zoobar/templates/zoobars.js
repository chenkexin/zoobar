
var myZoobars = {{ g.user.person.zoobars if g.user.person.zoobars > 0 else 0 }};

var div = document.getElementById("myZoobars");
if (div != null) {
    div.innerHTML = myZoobars;
}