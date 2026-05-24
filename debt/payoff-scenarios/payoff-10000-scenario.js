(function () {
  if (!window.IncomeClarityPayoffScenario) return;
  window.IncomeClarityPayoffScenario.init({
    idPrefix: "sc10",
    defaultBalance: 10000,
    defaultPayment: 400,
    paymentTablePayments: [250, 300, 400, 500, 600, 800],
    budgetBoost: 150,
    whatIf: [
      { title: "Pay $100 more", extra: 100 },
      { title: "Pay $200 more", extra: 200 },
      { title: "Lump sum $2,500", lump: 2500 },
    ],
    realistic: [
      { key: "comfortable", label: "Comfortable", pct: 0.025, floor: 200 },
      { key: "moderate", label: "Moderate", pct: 0.04, floor: 350 },
      { key: "aggressive", label: "Aggressive", pct: 0.07, floor: 600 },
    ],
  });
})();
