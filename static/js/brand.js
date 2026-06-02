(function () {
  "use strict";
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-brand-enhance]").forEach(function (element) {
      element.addEventListener("submit", function () {
        element.classList.add("brand-action--active");
        window.setTimeout(function () { element.classList.remove("brand-action--active"); }, 900);
      });
    });
    if (document.querySelector(".message--success")) {
      document.documentElement.classList.add("brand-has-success");
      window.setTimeout(function () { document.documentElement.classList.remove("brand-has-success"); }, 1200);
    }
  });
}());
