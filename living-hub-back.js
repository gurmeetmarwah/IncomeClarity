(function () {
  var LINK_ID = "living-hub-back-link";
  var CALCULATOR_PATH = "/credit-card-payoff-calculator";
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
    "hidden-costs": {
      path: "/debt/hidden-costs",
      label: "Hidden costs of debt",
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
      hash: "#living-budget-hub-title",
    },
    housing: {
      path: "/living/housing",
      label: "Housing affordability",
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

  var RENT_VS_BUY_HASH_TO_LIVING = {
    "#living-budget-hub-title": "budgeting",
    "#living-afford-hub-title": "housing",
    "#living-lifestyle-hub-title": "lifestyle-family",
    "#living-col-hub-title": "rent-vs-buy",
    "#rent-vs-buy": "rent-vs-buy",
  };

  var CALCULATOR_HASH_TO_DEBT = {
    "#debt-hub-scenarios": "payoff-scenarios",
    "#debt-hub-apr": "interest-apr",
    "#debt-hub-strategies": "payoff-strategies",
    "#debt-hub-health": "financial-health",
    "#debt-hub-hidden-costs": "hidden-costs",
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
    if (!hub || !hub.path) {
      return false;
    }
    return debtHubKeyFromPath(hub.path) !== null;
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
      if (livingKey === "rent-vs-buy") {
        if (refUrl.hash) {
          var mapped = RENT_VS_BUY_HASH_TO_LIVING[refUrl.hash.toLowerCase()];
          if (mapped && mapped !== "rent-vs-buy") {
            return hubFromKey(mapped);
          }
          return Object.assign({}, hub, { hash: refUrl.hash });
        }
        if (stripPath(location.pathname) === "/living/budgeting") {
          return Object.assign({}, hub, { hash: "#living-budget-hub-title" });
        }
      }
      return hub;
    }

    if (stripPath(refUrl.pathname) === stripPath(CALCULATOR_PATH)) {
      var debtMapped =
        CALCULATOR_HASH_TO_DEBT[(refUrl.hash || "").toLowerCase()];
      if (debtMapped) {
        return hubFromKey(debtMapped);
      }
    }

    return null;
  }

  function defaultHubFromLink(link) {
    var raw = link.getAttribute("data-living-back-default");
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
    if (stripPath(pathPart) === stripPath(RENT_VS_BUY_PATH)) {
      return Object.assign({}, LIVING_HUBS["rent-vs-buy"], {
        hash: hash || "#living-budget-hub-title",
      });
    }
    return { path: pathPart, label: "previous page", hash: hash };
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

  function applyBreadcrumbs(hub) {
    var ol = document.querySelector(".take-home-return-breadcrumbs");
    if (!ol) {
      return;
    }

    var title = getCurrentBreadcrumbTitle();
    ol.innerHTML = "";

    if (isDebtHub(hub)) {
      var calcLi = document.createElement("li");
      var calcLink = document.createElement("a");
      calcLink.href = CALCULATOR_PATH + "#payoff";
      calcLink.textContent = CALCULATOR_LABEL;
      calcLi.appendChild(calcLink);
      ol.appendChild(calcLi);
    } else {
      var rentLi = document.createElement("li");
      var rentLink = document.createElement("a");
      rentLink.href = RENT_VS_BUY_PATH;
      rentLink.textContent = RENT_VS_BUY_LABEL;
      rentLi.appendChild(rentLink);
      ol.appendChild(rentLi);
    }

    var hubLi = document.createElement("li");
    var hubLink = document.createElement("a");
    hubLink.href = hubHref(hub).split("#")[0];
    hubLink.textContent = hub.label;
    hubLi.appendChild(hubLink);
    ol.appendChild(hubLi);

    var currentLi = document.createElement("li");
    currentLi.setAttribute("aria-current", "page");
    currentLi.textContent = title;
    ol.appendChild(currentLi);
  }

  function applyParentNav(link, hub) {
    link.href = hubHref(hub);
    link.textContent = "← Back to " + hub.label;
    applyBreadcrumbs(hub);
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

    var hub =
      hubFromQueryParam() ||
      hubFromReferrer(getValidReferrer()) ||
      defaultHubFromLink(link);

    if (!hub) {
      return;
    }

    applyParentNav(link, hub);
    cleanFromQueryParam();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
