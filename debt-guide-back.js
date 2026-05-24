(function () {
  var CALCULATOR_PATH = "/credit-card-payoff-calculator";
  var CALCULATOR_LABEL = "Credit card payoff calculator";

  var DEBT_HUBS = {
    "payoff-scenarios": {
      path: "/debt/payoff-scenarios",
      label: "Debt payoff scenarios",
    },
    "interest-apr": {
      path: "/debt/interest-apr",
      label: "Interest & APR",
    },
    "payoff-strategies": {
      path: "/debt/payoff-strategies",
      label: "Debt payoff strategies",
    },
    "financial-health": {
      path: "/debt/financial-health",
      label: "Debt & financial health",
    },
    "hidden-costs": {
      path: "/debt/hidden-costs",
      label: "Hidden costs of debt",
    },
    "life-decisions": {
      path: "/debt/life-decisions",
      label: "Debt vs life decisions",
    },
  };

  var CALCULATOR_HASH_TO_HUB = {
    "#debt-hub-scenarios": "payoff-scenarios",
    "#debt-hub-apr": "interest-apr",
    "#debt-hub-strategies": "payoff-strategies",
    "#debt-hub-health": "financial-health",
    "#debt-hub-hidden-costs": "hidden-costs",
    "#debt-hub-life": "life-decisions",
  };

  var HUB_TO_CALCULATOR_HASH = {
    "payoff-scenarios": "#debt-hub-scenarios",
    "interest-apr": "#debt-hub-apr",
    "payoff-strategies": "#debt-hub-strategies",
    "financial-health": "#debt-hub-health",
    "hidden-costs": "#debt-hub-hidden-costs",
    "life-decisions": "#debt-hub-life",
  };

  var CALCULATOR_PARENT_LABEL = "browse debt topics";

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

  function hubKeyFromPath(pathname) {
    var p = stripPath(pathname);
    var key;
    for (key in DEBT_HUBS) {
      if (stripPath(DEBT_HUBS[key].path) === p) {
        return key;
      }
    }
    return null;
  }

  function hubFromKey(key) {
    return key && DEBT_HUBS[key] ? DEBT_HUBS[key] : null;
  }

  function isCalculatorPath(pathname) {
    return stripPath(pathname) === stripPath(CALCULATOR_PATH);
  }

  function isDebtGuidePage() {
    var path = stripPath(location.pathname);
    if (isCalculatorPath(path)) {
      return false;
    }
    return path.indexOf("/debt/") === 0;
  }

  function getValidReferrer() {
    var rawRef = document.referrer;
    if (!rawRef) {
      return null;
    }

    var refUrl;
    try {
      refUrl = new URL(rawRef);
    } catch (_e) {
      return null;
    }

    if (refUrl.origin !== location.origin) {
      return null;
    }

    if (stripPath(refUrl.pathname) === stripPath(location.pathname)) {
      return null;
    }

    return refUrl;
  }

  function hubFromQueryParam() {
    var from = new URLSearchParams(location.search).get("from");
    return hubFromKey(from);
  }

  function isDebtHubLandingPage() {
    return hubKeyFromPath(location.pathname) !== null;
  }

  function isCalculatorParent(parent) {
    return parent && isCalculatorPath(parent.path);
  }

  function calculatorParentFromHash(hash) {
    return {
      path: CALCULATOR_PATH,
      label: CALCULATOR_PARENT_LABEL,
      hash: hash || "#debt-hub-title",
    };
  }

  function calculatorParentForCurrentHub() {
    var key = hubKeyFromPath(location.pathname);
    if (!key) {
      return null;
    }
    return calculatorParentFromHash(HUB_TO_CALCULATOR_HASH[key]);
  }

  function hubFromReferrer(refUrl) {
    if (!refUrl) {
      return null;
    }

    var currentHubKey = hubKeyFromPath(location.pathname);
    var refHubKey = hubKeyFromPath(refUrl.pathname);

    if (refHubKey && refHubKey !== currentHubKey) {
      return hubFromKey(refHubKey);
    }

    if (isCalculatorPath(refUrl.pathname)) {
      var hashKey = (refUrl.hash || "").toLowerCase();
      if (isDebtHubLandingPage()) {
        return calculatorParentFromHash(
          hashKey || HUB_TO_CALCULATOR_HASH[currentHubKey]
        );
      }
      if (CALCULATOR_HASH_TO_HUB[hashKey]) {
        return calculatorParentFromHash(hashKey);
      }
      return calculatorParentFromHash("#payoff");
    }

    return null;
  }

  function resolveParentHub(link) {
    var fromHub = hubFromQueryParam();
    if (
      fromHub &&
      stripPath(fromHub.path) !== stripPath(location.pathname)
    ) {
      return fromHub;
    }

    var refHub = hubFromReferrer(getValidReferrer());
    if (refHub) {
      return refHub;
    }

    if (isDebtHubLandingPage()) {
      return calculatorParentForCurrentHub();
    }

    return defaultHubFromLink(link);
  }

  function parentHref(hub) {
    return hub.path + (hub.hash || "");
  }

  function backText(hub) {
    return "← Back to " + hub.label;
  }

  function getCurrentBreadcrumbTitle() {
    var current = document.querySelector(
      '.take-home-return-breadcrumbs li[aria-current="page"]'
    );
    if (current) {
      return current.textContent.trim();
    }
    var h1 = document.querySelector("main h1");
    if (h1) {
      return h1.textContent.trim();
    }
    return document.title.split("|")[0].trim();
  }

  function applyHubBreadcrumbs(parent) {
    var ol = document.querySelector(".take-home-return-breadcrumbs");
    if (!ol) {
      return;
    }

    var title = getCurrentBreadcrumbTitle();
    ol.innerHTML = "";

    if (isCalculatorParent(parent)) {
      var calcLi = document.createElement("li");
      var calcLink = document.createElement("a");
      calcLink.href = parentHref(parent);
      calcLink.textContent = CALCULATOR_LABEL;
      calcLi.appendChild(calcLink);

      var currentLi = document.createElement("li");
      currentLi.setAttribute("aria-current", "page");
      currentLi.textContent = title;
      ol.appendChild(calcLi);
      ol.appendChild(currentLi);
      return;
    }

    var calcLi = document.createElement("li");
    var calcLink = document.createElement("a");
    calcLink.href = CALCULATOR_PATH + "#payoff";
    calcLink.textContent = CALCULATOR_LABEL;
    calcLi.appendChild(calcLink);

    var hubLi = document.createElement("li");
    var hubLink = document.createElement("a");
    hubLink.href = parentHref(parent);
    hubLink.textContent = parent.label;
    hubLi.appendChild(hubLink);

    var currentLi = document.createElement("li");
    currentLi.setAttribute("aria-current", "page");
    currentLi.textContent = title;

    ol.appendChild(calcLi);
    ol.appendChild(hubLi);
    ol.appendChild(currentLi);
  }

  function applyHubBackLink(link, hub) {
    if (isDebtGuidePage()) {
      applyHubBreadcrumbs(hub);
    }
    if (window.IncomeClarityBack) {
      window.IncomeClarityBack.enhance(link, {
        fallbackHref: parentHref(hub),
        fallbackLabel: backText(hub),
      });
    }
  }

  function defaultHubFromLink(link) {
    var raw = link.getAttribute("data-debt-back-default");
    if (!raw) {
      return null;
    }
    var hubKey = hubKeyFromPath(raw.split("#")[0]);
    if (hubKey) {
      return hubFromKey(hubKey);
    }
    if (isCalculatorPath(raw.split("#")[0])) {
      return calculatorParentFromHash(
        raw.indexOf("#") >= 0 ? raw.slice(raw.indexOf("#")) : "#payoff"
      );
    }
    return { path: raw.split("#")[0], label: "previous page", hash: "" };
  }

  function cleanFromQueryParam() {
    if (!location.search || location.search.indexOf("from=") < 0) {
      return;
    }
    var params = new URLSearchParams(location.search);
    if (!params.has("from")) {
      return;
    }
    params.delete("from");
    var next =
      location.pathname +
      (params.toString() ? "?" + params.toString() : "") +
      location.hash;
    window.history.replaceState({}, "", next);
  }

  function appendFromParam(href, fromKey) {
    if (!href || href.indexOf("from=") >= 0) {
      return href;
    }
    var hash = "";
    var base = href;
    if (href.indexOf("#") >= 0) {
      var parts = href.split("#");
      base = parts[0];
      hash = "#" + parts.slice(1).join("#");
    }
    var join = base.indexOf("?") >= 0 ? "&" : "?";
    return base + join + "from=" + encodeURIComponent(fromKey) + hash;
  }

  function propagateFromParamToMainLinks(fromKey) {
    if (!fromKey || !hubFromKey(fromKey)) {
      return;
    }
    var main = document.querySelector("main");
    if (!main) {
      return;
    }
    main.querySelectorAll("a[href]").forEach(function (anchor) {
      var href = anchor.getAttribute("href");
      if (!href || href.charAt(0) !== "/") {
        return;
      }
      if (
        href.indexOf("/debt/") !== 0 &&
        href.indexOf("/living/") !== 0 &&
        href.indexOf("/hourly-to-salary-after-tax") !== 0 &&
        href.indexOf("/rent-vs-buy-calculator") !== 0 &&
        href.indexOf("/credit-card-payoff-calculator") !== 0
      ) {
        return;
      }
      anchor.setAttribute("href", appendFromParam(href, fromKey));
    });
  }

  function mountDebtGuideBackLink() {
    var link = document.getElementById("debt-guide-back-link");
    var parentFromKey = new URLSearchParams(location.search).get("from");

    if (parentFromKey) {
      propagateFromParamToMainLinks(parentFromKey);
    }

    if (!link) {
      if (parentFromKey) {
        cleanFromQueryParam();
      }
      return;
    }

    var hub = resolveParentHub(link);

    if (hub) {
      applyHubBackLink(link, hub);
    } else if (window.IncomeClarityBack) {
      window.IncomeClarityBack.enhance(link);
    }

    cleanFromQueryParam();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mountDebtGuideBackLink);
  } else {
    mountDebtGuideBackLink();
  }
})();
