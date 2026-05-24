(function () {
  if (!window.IncomeClarityPayoffScenario) return;
  window.IncomeClarityPayoffScenario.init({
    idPrefix: "sc5",
    defaultBalance: 5000,
    defaultPayment: 200,
    paymentTablePayments: [100, 150, 200, 250, 300, 500],
    budgetBoost: 75,
    whatIf: [
      { title: "Pay $50 more", extra: 50 },
      { title: "Pay $100 more", extra: 100 },
      { title: "Lump sum $1,000", lump: 1000 },
    ],
    realistic: [
      { key: "comfortable", label: "Comfortable", pct: 0.025, floor: 100 },
      { key: "moderate", label: "Moderate", pct: 0.04, floor: 175 },
      { key: "aggressive", label: "Aggressive", pct: 0.07, floor: 300 },
    ],
  });
})();
