// Language filter: hides posts marked with lang="pl" across the site.
// The toggle button lives on the blog index; the preference is remembered
// in localStorage and applied on every page load.

(function () {
  var KEY = "hide_pl";

  function stored() {
    try {
      return localStorage.getItem(KEY) === "1";
    } catch (e) {
      return false;
    }
  }

  var toggle = document.getElementById("lang-toggle");

  function setHidden(value) {
    document.body.classList.toggle("hide-pl", value);
    if (toggle) {
      toggle.setAttribute("aria-pressed", value ? "true" : "false");
      toggle.textContent = value ? "Show Polish posts" : "Hide Polish posts";
    }
    try {
      localStorage.setItem(KEY, value ? "1" : "0");
    } catch (e) {}
  }

  setHidden(stored());

  if (toggle) {
    toggle.addEventListener("click", function () {
      setHidden(!document.body.classList.contains("hide-pl"));
    });
  }
})();
