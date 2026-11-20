/* Wildstar Weddings — small site interactions */
(function () {
  "use strict";
  var toggle = document.querySelector(".topbar__toggle");
  var menu = document.getElementById("topbar-nav");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        menu.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }
  var y = document.querySelector("[data-year]");
  if (y) y.textContent = new Date().getFullYear();
})();
