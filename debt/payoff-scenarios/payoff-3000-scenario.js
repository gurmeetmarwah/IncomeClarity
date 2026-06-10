(function () {
  if (!window.IncomeClarityPayoffScenario) return;
  window.IncomeClarityPayoffScenario.init({
    idPrefix: "sc3k",
    defaultBalance: 3000,
    defaultPayment: 150,
    paymentTablePayments: [75, 100, 125, 150, 200, 300],
    budgetBoost: 50,
    whatIf: [{ title: "Pay $50 more", extra: 50 }, { title: "Pay $75 more", extra: 75 }, { title: "Lump sum $500", lump: 500 }],
    realistic: [{ key: "comfortable", label: "Comfortable", pct: 0.025, floor: 75 }, { key: "moderate", label: "Moderate", pct: 0.04, floor: 125 }, { key: "aggressive", label: "Aggressive", pct: 0.07, floor: 200 }],
  });
})();
