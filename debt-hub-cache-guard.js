/**
 * If an old cached copy of the debt page is shown (no Explore buttons on topic cards),
 * reload once so users get the current markup after Living → Debt navigation or bfcache.
 */
(function () {
  var ATTEMPT_KEY = "ic-debt-hub-explore-reload";

  function hubMissingExplore() {
    var hub = document.getElementById("debt-hub-scenarios");
    return hub && !hub.querySelector(".debt-topic-explore-btn");
  }

  function clearAttempt() {
    try {
      sessionStorage.removeItem(ATTEMPT_KEY);
    } catch (e) {}
  }

  function reloadOnceIfStale(fromBfcache) {
    if (!hubMissingExplore()) {
      clearAttempt();
      return;
    }
    if (fromBfcache) {
      location.reload();
      return;
    }
    try {
      if (sessionStorage.getItem(ATTEMPT_KEY)) return;
      sessionStorage.setItem(ATTEMPT_KEY, "1");
    } catch (e) {}
    location.replace(location.href);
  }

  window.addEventListener("pageshow", function (e) {
    reloadOnceIfStale(Boolean(e.persisted));
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", reloadOnceIfStale);
  } else {
    reloadOnceIfStale();
  }
})();
