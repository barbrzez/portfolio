// Theme toggle: switches between the default paper theme and the
// experimental hacker theme. Preference is remembered in localStorage.

(function () {
  var KEY = "theme";
  var toggle = document.getElementById("theme-toggle");
  if (!toggle) return;

  function stored() {
    try {
      return localStorage.getItem(KEY) === "hacker";
    } catch (e) {
      return false;
    }
  }

  function setHacker(value) {
    document.body.classList.toggle("theme-hacker", value);
    toggle.setAttribute("aria-pressed", value ? "true" : "false");
    toggle.textContent = value ? "Normal mode" : "Hacker mode";
    try {
      localStorage.setItem(KEY, value ? "hacker" : "default");
    } catch (e) {}
  }

  setHacker(stored());

  toggle.addEventListener("click", function () {
    setHacker(!document.body.classList.contains("theme-hacker"));
  });
})();
