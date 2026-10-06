// Language toggle: hides posts marked with lang="pl" on the blog index.
// Preference is remembered in localStorage.

(function () {
  var KEY = "hide_pl";
  var toggle = document.getElementById("lang-toggle");
  if (!toggle) return;

  function hidden() {
    try {
      return localStorage.getItem(KEY) === "1";
    } catch (e) {
      return false;
    }
  }

  function setHidden(value) {
    document.body.classList.toggle("hide-pl", value);
    toggle.setAttribute("aria-pressed", value ? "true" : "false");
    try {
      localStorage.setItem(KEY, value ? "1" : "0");
    } catch (e) {}
  }

  if (hidden()) setHidden(true);

  toggle.addEventListener("click", function () {
    setHidden(!document.body.classList.contains("hide-pl"));
  });
})();
