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

  /* ---- availability notice (Sundays & Mondays only) ---- */
  var MSG = "Currently accepting requests on <strong>Sundays and Mondays only</strong>. Thanks for understanding!";

  // persistent bottom bar — shows on every page, dismissible for the session
  if (sessionStorage.getItem("wsAvailBarClosed") !== "1") {
    var bar = document.createElement("div");
    bar.className = "avail-bar";
    bar.setAttribute("role", "region");
    bar.setAttribute("aria-label", "Availability notice");
    bar.innerHTML =
      '<p class="avail-bar__text">' + MSG + "</p>" +
      '<a class="btn" href="/contact/">Check Availability</a>' +
      '<button class="avail-bar__close" type="button" aria-label="Dismiss notice">&times;</button>';
    document.body.appendChild(bar);
    requestAnimationFrame(function () { bar.classList.add("is-in"); });
    bar.querySelector(".avail-bar__close").addEventListener("click", function () {
      bar.classList.remove("is-in");
      sessionStorage.setItem("wsAvailBarClosed", "1");
      setTimeout(function () { bar.remove(); }, 500);
    });
  }

  // first-visit modal — once per browser session
  if (sessionStorage.getItem("wsAvailModalSeen") !== "1") {
    var modal = document.createElement("div");
    modal.className = "avail-modal";
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");
    modal.setAttribute("aria-label", "Availability notice");
    modal.innerHTML =
      '<div class="avail-modal__card">' +
        '<button class="avail-modal__close" type="button" aria-label="Close">&times;</button>' +
        '<img class="avail-modal__leaf" src="/assets/img/leaf.png" alt="">' +
        '<span class="eyebrow">A quick note</span>' +
        "<h2>Sundays &amp; Mondays only</h2>" +
        "<p>" + MSG + "</p>" +
        '<a class="btn" href="/contact/">Check Availability</a>' +
      "</div>";
    document.body.appendChild(modal);
    requestAnimationFrame(function () { modal.classList.add("is-in"); });
    sessionStorage.setItem("wsAvailModalSeen", "1");

    var closeModal = function () {
      modal.classList.remove("is-in");
      setTimeout(function () { modal.remove(); }, 400);
      document.removeEventListener("keydown", onEsc);
    };
    var onEsc = function (e) { if (e.key === "Escape") closeModal(); };
    modal.querySelector(".avail-modal__close").addEventListener("click", closeModal);
    modal.addEventListener("click", function (e) { if (e.target === modal) closeModal(); });
    document.addEventListener("keydown", onEsc);
  }
})();
