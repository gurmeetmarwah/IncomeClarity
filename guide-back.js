(function () {
  var BACK_LABEL = "← Back";

  function stripPath(pathname) {
    var p = pathname || "";
    if (/\/index\.html$/i.test(p)) {
      p = p.slice(0, -10) || "/";
    } else if (/\.html$/i.test(p)) {
      p = p.slice(0, -5);
    }
    if (p.length > 1 && p.endsWith("/")) {
      p = p.slice(0, -1);
    }
    return p.toLowerCase();
  }

  function getFallbackHref(link) {
    if (!link) {
      return "/";
    }
    var stored = link.getAttribute("data-back-fallback");
    if (stored) {
      return stored;
    }
    return (
      link.getAttribute("data-debt-back-default") ||
      link.getAttribute("data-housing-back-default") ||
      link.getAttribute("data-living-back-default") ||
      link.getAttribute("href") ||
      "/"
    );
  }

  function canUseHistoryBack() {
    if (window.history.length < 2) {
      return false;
    }
    var ref = document.referrer;
    if (!ref) {
      return false;
    }
    try {
      var refUrl = new URL(ref);
      if (refUrl.origin !== location.origin) {
        return false;
      }
      var here = stripPath(location.pathname);
      var there = stripPath(refUrl.pathname);
      return here !== there;
    } catch (_e) {
      return false;
    }
  }

  function onBackClick(event) {
    if (
      event.button !== 0 ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey
    ) {
      return;
    }
    if (canUseHistoryBack()) {
      event.preventDefault();
      window.history.back();
    }
  }

  function enhanceLink(link, options) {
    if (!link) {
      return;
    }

    var opts = options || {};
    var fallback = opts.fallbackHref || getFallbackHref(link);
    link.setAttribute("data-back-fallback", fallback);
    link.setAttribute("href", fallback);

    if (!link.dataset.backEnhanced) {
      link.dataset.backEnhanced = "1";
      link.addEventListener("click", onBackClick);
    }

    if (canUseHistoryBack()) {
      link.textContent = BACK_LABEL;
    } else if (opts.fallbackLabel) {
      link.textContent = opts.fallbackLabel;
    }
  }

  function mountAll() {
    var selector =
      "#debt-guide-back-link, #housing-guide-back-link, #living-hub-back-link, .debt-minimum-guide-back-link";
    document.querySelectorAll(selector).forEach(function (link) {
      enhanceLink(link);
    });
  }

  window.IncomeClarityBack = {
    enhance: enhanceLink,
    canUseHistoryBack: canUseHistoryBack,
    mountAll: mountAll,
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mountAll);
  } else {
    mountAll();
  }
})();
