function toggle(elt) {
  var elts,j;
  while (elt && !elt.classList.contains("section")) {
    elt = elt.parentElement;
  }
  if (!elt) return;
  elts = elt.querySelectorAll(".section-text, .section-toggle");
  for (j = 0; j < elts.length; j++)
    elts[j].classList.toggle("active");
}

function focus() {
  var h,elts,e,tk,i;
  h = window.location.hash;
  e = document.getElementById(h.substring(1));
  while (e) {
    tk = e.classList;
    if (tk.contains("section-text") && !tk.contains("active")) {
      toggle(e);
      break;
    }
    e = e.parentElement;
  }
}

function escape(evt) {
  var elts,e,i;
  if (evt.code === "Escape") {
    window.location = "";
    elts = document.querySelectorAll(".section");
    for (i=0; i< elts.length; i++) {
      e = elts[i];
      if (e.querySelectorAll(".section-toggle.active").length)
        toggle(e);
    }
  }
}

(function(){
  var nodes,i;

  nodes = document.getElementsByClassName("section-toggle");
  for (i = 0; i < nodes.length; i++) {
    nodes[i].addEventListener("click", function() {
      toggle(this);
    });
  }

  focus();
  window.addEventListener('onload',focus);
  window.addEventListener('hashchange',focus);
  window.addEventListener('keypress',escape);

})();
