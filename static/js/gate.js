// Minimal client-side password gate for GitHub Pages.
// GitHub Pages serves static files only and cannot do real password
// protection. This gate hides page content in the browser until the
// correct password is entered. It is a deterrent, not real security:
// the HTML is still publicly downloadable.

(function () {
  var COOKIE = "blog_gate";
  // SHA-256 hex of the password. Generate with:
  //   echo -n "yourpassword" | sha256sum
  // The default password is "changeme" -- CHANGE THIS.
  var HASH = "5836eb4ed1847b0a8701882734fd1c4b065a5d38a62af457b7c96ef7fccd4b77";

  function setCookie(name, value, days) {
    var d = new Date();
    d.setTime(d.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie =
      name + "=" + value + ";path=/;expires=" + d.toUTCString() + ";SameSite=Lax";
  }

  function getCookie(name) {
    var parts = document.cookie ? document.cookie.split("; ") : [];
    for (var i = 0; i < parts.length; i++) {
      var kv = parts[i].split("=");
      if (kv[0] === name) return kv[1];
    }
    return "";
  }

  function sha256(text) {
    // GitHub Pages is HTTPS, so crypto.subtle is available.
    return crypto.subtle
      .digest("SHA-256", new TextEncoder().encode(text))
      .then(function (buf) {
        return Array.prototype.map
          .call(new Uint8Array(buf), function (b) {
            return ("0" + b.toString(16)).slice(-2);
          })
          .join("");
      });
  }

  function unlocked() {
    return getCookie(COOKIE) === "ok";
  }

  function unlock() {
    setCookie(COOKIE, "ok", 30);
    hideGate();
  }

  function hideGate() {
    var overlay = document.getElementById("gate-overlay");
    if (overlay) overlay.hidden = true;
  }

  function makeGate() {
    var overlay = document.createElement("div");
    overlay.id = "gate-overlay";
    overlay.innerHTML =
      '<div class="gate-box">' +
      "<h1>This site is password protected</h1>" +
      '<p class="gate-error" id="gate-error"></p>' +
      '<input type="password" id="gate-input" placeholder="Password" ' +
      'autocomplete="current-password">' +
      '<button id="gate-button" type="button">Enter</button>' +
      "</div>";
    document.body.appendChild(overlay);
    var input = overlay.querySelector("#gate-input");
    var button = overlay.querySelector("#gate-button");
    var error = overlay.querySelector("#gate-error");

    function tryUnlock() {
      var value = input.value;
      if (!value) return;
      sha256(value).then(function (hash) {
        if (hash === HASH) {
          unlock();
        } else {
          error.textContent = "Wrong password, try again.";
          input.value = "";
          input.focus();
        }
      });
    }

    button.addEventListener("click", tryUnlock);
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") tryUnlock();
    });
    input.focus();
  }

  if (unlocked()) return;
  makeGate();
})();
