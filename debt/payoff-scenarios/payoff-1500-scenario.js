(function () {
  if (!window.IncomeClarityPayoffScenario) return;
  window.IncomeClarityPayoffScenario.init({
    idPrefix: "sc15",
    defaultBalance: 1500,
    defaultPayment: 100,
    paymentTablePayments: [50, 75, 100, 125, 150, 200],
    budgetBoost: 25,
    whatIf: [{ title: "Pay $25 more", extra: 25 }, { title: "Pay $50 more", extra: 50 }, { title: "Lump sum $300", lump: 300 }],
    realistic: [{ key: "comfortable", label: "Comfortable", pct: 0.025, floor: 50 }, { key: "moderate", label: "Moderate", pct: 0.04, floor: 75 }, { key: "aggressive", label: "Aggressive", pct: 0.07, floor: 125 }],
  });
})();
