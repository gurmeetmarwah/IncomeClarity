(function () {
  var LINK_ID = "housing-guide-back-link";
  var HOUSING_HUB_PATH = "/living/housing";
  var HOUSING_HUB_LABEL = "Housing affordability";
  var HOUSING_BACK_TEXT = "← Back to housing affordability";
  var CALCULATOR_PATH = "/debt/credit-cards/credit-card-payoff-calculator";
  var CALCULATOR_LABEL = "Credit card payoff calculator";
  var RENT_VS_BUY_PATH = "/rent-vs-buy-calculator";
  var RENT_VS_BUY_LABEL = "Living (rent vs buy)";

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
    "credit-cards": {
      path: "/debt/credit-cards",
      label: "Credit cards",
    },
    "life-decisions": {
      path: "/debt/life-decisions",
      label: "Debt vs life decisions",
    },
  };

  var LIVING_HUBS = {
    "rent-vs-buy": {
      path: RENT_VS_BUY_PATH,
      label: "Living tools",
    },
    housing: {
      path: HOUSING_HUB_PATH,
      label: HOUSING_HUB_LABEL,
    },
    budgeting: {
      path: "/living/budgeting",
      label: "Budget planning",
    },
    "lifestyle-family": {
      path: "/living/lifestyle-family",
      label: "Lifestyle & family",
    },
  };

  var CALCULATOR_HASH_TO_DEBT = {
    "#debt-hub-scenarios": "payoff-scenarios",
    "#debt-hub-apr": "interest-apr",
    "#debt-hub-strategies": "payoff-strategies",
    "#debt-hub-health": "financial-health",
    "#debt-hub-credit-cards": "credit-cards",
    "#debt-hub-life": "life-decisions",
  };

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

  function hubHref(hub) {
    return (hub.path || "") + (hub.hash || "");
  }

  function debtHubKeyFromPath(pathname) {
    var p = stripPath(pathname);
    var key;
    for (key in DEBT_HUBS) {
      if (stripPath(DEBT_HUBS[key].path) === p) {
        return key;
      }
    }
    return null;
  }

  function livingHubKeyFromPath(pathname) {
    var p = stripPath(pathname);
    var key;
    for (key in LIVING_HUBS) {
      if (stripPath(LIVING_HUBS[key].path) === p) {
        return key;
      }
    }
    return null;
  }

  function hubFromKey(key) {
    if (key && DEBT_HUBS[key]) {
      return DEBT_HUBS[key];
    }
    if (key && LIVING_HUBS[key]) {
      return LIVING_HUBS[key];
    }
    return null;
  }

  function isDebtHub(hub) {
    return hub && debtHubKeyFromPath(hub.path) !== null;
  }

  function isHousingHubPath(pathname) {
    return stripPath(pathname) === stripPath(HOUSING_HUB_PATH);
  }

  function isRentVsBuyPath(pathname) {
    return stripPath(pathname) === stripPath(RENT_VS_BUY_PATH);
  }

  function isHousingSiloGuidePage() {
    var path = stripPath(location.pathname);
    return path.indexOf("/living/housing/") === 0 && path !== stripPath(HOUSING_HUB_PATH);
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

  function hubFromReferrer(refUrl) {
    if (!refUrl) {
      return null;
    }

    var debtKey = debtHubKeyFromPath(refUrl.pathname);
    if (debtKey) {
      return hubFromKey(debtKey);
    }

    var livingKey = livingHubKeyFromPath(refUrl.pathname);
    if (livingKey) {
      var hub = hubFromKey(livingKey);
      if (refUrl.hash) {
        return Object.assign({}, hub, { hash: refUrl.hash });
      }
      return hub;
    }

    if (stripPath(refUrl.pathname) === stripPath(CALCULATOR_PATH)) {
      var mapped = CALCULATOR_HASH_TO_DEBT[(refUrl.hash || "").toLowerCase()];
      if (mapped) {
        return hubFromKey(mapped);
      }
    }

    return null;
  }

  function defaultHubFromLink(link) {
    var raw =
      link.getAttribute("data-housing-back-default") || link.getAttribute("href");
    if (!raw) {
      return null;
    }
    var pathPart = raw.split("#")[0];
    var hash = raw.indexOf("#") >= 0 ? raw.slice(raw.indexOf("#")) : "";
    var debtKey = debtHubKeyFromPath(pathPart);
    if (debtKey) {
      return hubFromKey(debtKey);
    }
    var livingKey = livingHubKeyFromPath(pathPart);
    if (livingKey) {
      var hub = hubFromKey(livingKey);
      return hash ? Object.assign({}, hub, { hash: hash }) : hub;
    }
    return null;
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

  function applyDebtSiloBreadcrumbs(hub) {
    var ol = document.querySelector(".take-home-return-breadcrumbs");
    if (!ol) {
      return;
    }

    var title = getCurrentBreadcrumbTitle();
    ol.innerHTML = "";

    var calcLi = document.createElement("li");
    var calcLink = document.createElement("a");
    calcLink.href = CALCULATOR_PATH + "#payoff";
    calcLink.textContent = CALCULATOR_LABEL;
    calcLi.appendChild(calcLink);

    var hubLi = document.createElement("li");
    var hubLink = document.createElement("a");
    hubLink.href = hubHref(hub).split("#")[0];
    hubLink.textContent = hub.label;
    hubLi.appendChild(hubLink);

    var currentLi = document.createElement("li");
    currentLi.setAttribute("aria-current", "page");
    currentLi.textContent = title;

    ol.appendChild(calcLi);
    ol.appendChild(hubLi);
    ol.appendChild(currentLi);
  }

  function applyHousingSiloBreadcrumbs(hubHrefValue, hubLabel) {
    var ol = document.querySelector(".take-home-return-breadcrumbs");
    if (!ol) {
      return;
    }

    var title = getCurrentBreadcrumbTitle();
    var parentPath = hubHrefValue.split("#")[0];
    ol.innerHTML = "";

    var rentLi = document.createElement("li");
    var rentLink = document.createElement("a");
    rentLink.href = RENT_VS_BUY_PATH;
    rentLink.textContent = RENT_VS_BUY_LABEL;
    rentLi.appendChild(rentLink);

    var hubLi = document.createElement("li");
    var hubLink = document.createElement("a");
    hubLink.href = parentPath;
    hubLink.textContent = hubLabel;
    hubLi.appendChild(hubLink);

    var currentLi = document.createElement("li");
    currentLi.setAttribute("aria-current", "page");
    currentLi.textContent = title;

    ol.appendChild(rentLi);
    ol.appendChild(hubLi);
    ol.appendChild(currentLi);
  }

  function applyDebtParentNav(link, hub) {
    applyDebtSiloBreadcrumbs(hub);
    if (window.IncomeClarityBack) {
      window.IncomeClarityBack.enhance(link, {
        fallbackHref: hubHref(hub),
        fallbackLabel: "← Back to " + hub.label,
      });
    }
  }

  function applyLivingSiloParentNav(link, hub) {
    if (window.IncomeClarityBack) {
      window.IncomeClarityBack.enhance(link, {
        fallbackHref: hubHref(hub),
        fallbackLabel: "← Back to " + hub.label,
      });
    }
    if (stripPath(hub.path) === stripPath(HOUSING_HUB_PATH)) {
      applyHousingSiloBreadcrumbs(hubHref(hub), hub.label);
    } else if (stripPath(hub.path) === stripPath(RENT_VS_BUY_PATH)) {
      applyHousingSiloBreadcrumbs(hubHref(hub), "Living (rent vs buy)");
    }
  }

  function housingHubHref(refUrl) {
    return HOUSING_HUB_PATH + (refUrl && refUrl.hash ? refUrl.hash : "");
  }

  function rewriteBreadcrumbs(href) {
    var ol = document.querySelector(".take-home-return-breadcrumbs");
    if (!ol) {
      return;
    }

    var title = getCurrentBreadcrumbTitle();
    ol.innerHTML = "";

    var parentLi = document.createElement("li");
    var parentLink = document.createElement("a");
    parentLink.href = href.split("#")[0];
    parentLink.textContent = HOUSING_HUB_LABEL;
    parentLi.appendChild(parentLink);

    var currentLi = document.createElement("li");
    currentLi.setAttribute("aria-current", "page");
    currentLi.textContent = title;

    ol.appendChild(parentLi);
    ol.appendChild(currentLi);
  }

  function applyHousingSiloNav(refUrl) {
    var href = housingHubHref(refUrl);
    var link = document.getElementById(LINK_ID);

    if (link && window.IncomeClarityBack) {
      window.IncomeClarityBack.enhance(link, {
        fallbackHref: href,
        fallbackLabel: HOUSING_BACK_TEXT,
      });
    }

    applyHousingSiloBreadcrumbs(href, HOUSING_HUB_LABEL);
  }

  function applyHousingHubNav(refUrl) {
    var href = housingHubHref(refUrl);
    var link = document.getElementById(LINK_ID);

    if (link && window.IncomeClarityBack) {
      window.IncomeClarityBack.enhance(link, {
        fallbackHref: href,
        fallbackLabel: HOUSING_BACK_TEXT,
      });
    }

    if (isHousingSiloGuidePage()) {
      applyHousingSiloBreadcrumbs(href, HOUSING_HUB_LABEL);
    } else {
      rewriteBreadcrumbs(href);
    }
  }

  function applyRentVsBuyBackLink(refUrl) {
    var link = document.getElementById(LINK_ID);
    if (!link) {
      return;
    }

    var href = refUrl.pathname + refUrl.search + refUrl.hash;
    if (window.IncomeClarityBack) {
      window.IncomeClarityBack.enhance(link, {
        fallbackHref: href,
        fallbackLabel: "← Back to Living (rent vs buy)",
      });
    }
    applyHousingSiloBreadcrumbs(
      refUrl.pathname + refUrl.hash,
      "Living (rent vs buy)"
    );
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

  function mount() {
    var link = document.getElementById(LINK_ID);
    if (!link) {
      return;
    }

    var parent =
      hubFromQueryParam() ||
      hubFromReferrer(getValidReferrer()) ||
      defaultHubFromLink(link);

    if (parent && isDebtHub(parent)) {
      applyDebtParentNav(link, parent);
      cleanFromQueryParam();
      return;
    }

    if (isHousingSiloGuidePage()) {
      if (parent && livingHubKeyFromPath(parent.path)) {
        applyLivingSiloParentNav(link, parent);
        cleanFromQueryParam();
        return;
      }

      var refUrl = getValidReferrer();
      if (refUrl && isHousingHubPath(refUrl.pathname)) {
        applyHousingSiloNav(refUrl);
        return;
      }

      if (refUrl && isRentVsBuyPath(refUrl.pathname)) {
        applyRentVsBuyBackLink(refUrl);
        return;
      }

      if (window.IncomeClarityBack) {
        window.IncomeClarityBack.enhance(link);
      }
      return;
    }

    var refUrl = getValidReferrer();
    if (!refUrl) {
      if (window.IncomeClarityBack) {
        window.IncomeClarityBack.enhance(link);
      }
      return;
    }

    if (isHousingHubPath(refUrl.pathname)) {
      applyHousingHubNav(refUrl);
      return;
    }

    if (isRentVsBuyPath(refUrl.pathname)) {
      applyRentVsBuyBackLink(refUrl);
      return;
    }

    if (window.IncomeClarityBack) {
      window.IncomeClarityBack.enhance(link);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
