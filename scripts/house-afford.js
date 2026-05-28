/**
 * House affordability calculator — shared across US hub, state, and city pages.
 * Uses 28/36 rules + regional tax/insurance/HOA defaults.
 */
(function (global) {
  'use strict';

  var REGIONS = {
    national: { label: 'US average', taxPct: 1.1, insPct: 0.35, hoa: 0, maintPct: 1.0 },
    california: { label: 'California', taxPct: 0.75, insPct: 0.45, hoa: 200, maintPct: 1.0 },
    texas: { label: 'Texas', taxPct: 1.6, insPct: 0.4, hoa: 75, maintPct: 1.0 },
    florida: { label: 'Florida', taxPct: 0.9, insPct: 0.55, hoa: 150, maintPct: 1.0 },
    'new-york': { label: 'New York', taxPct: 1.4, insPct: 0.4, hoa: 250, maintPct: 1.0 }
  };

  var STATES = {
    california: {
      name: 'California',
      slug: 'california',
      medianPrice: 785000,
      medianIncome: 96000,
      taxPct: 0.75,
      insPct: 0.45,
      hoa: 200,
      insight: 'Coastal prices and insurance push payments above the 28% rule for many earners.',
      cities: [
        { slug: 'los-angeles', name: 'Los Angeles', medianPrice: 875000, medianIncome: 82000, taxPct: 0.72, insPct: 0.5, hoa: 275 },
        { slug: 'san-francisco', name: 'San Francisco', medianPrice: 1250000, medianIncome: 140000, taxPct: 0.7, insPct: 0.42, hoa: 450 },
        { slug: 'san-diego', name: 'San Diego', medianPrice: 920000, medianIncome: 95000, taxPct: 0.73, insPct: 0.48, hoa: 320 }
      ]
    },
    texas: {
      name: 'Texas',
      slug: 'texas',
      medianPrice: 345000,
      medianIncome: 72000,
      taxPct: 1.6,
      insPct: 0.4,
      hoa: 75,
      insight: 'No state income tax helps take-home pay, but property tax is among the highest in the US.',
      cities: [
        { slug: 'houston', name: 'Houston', medianPrice: 310000, medianIncome: 68000, taxPct: 1.65, insPct: 0.45, hoa: 60 },
        { slug: 'dallas', name: 'Dallas', medianPrice: 385000, medianIncome: 75000, taxPct: 1.7, insPct: 0.42, hoa: 85 },
        { slug: 'austin', name: 'Austin', medianPrice: 485000, medianIncome: 88000, taxPct: 1.55, insPct: 0.4, hoa: 120 }
      ]
    },
    florida: {
      name: 'Florida',
      slug: 'florida',
      medianPrice: 395000,
      medianIncome: 68000,
      taxPct: 0.9,
      insPct: 0.55,
      hoa: 150,
      insight: 'Insurance and HOA fees often matter more than the mortgage payment itself.',
      cities: [
        { slug: 'miami', name: 'Miami', medianPrice: 580000, medianIncome: 62000, taxPct: 0.95, insPct: 0.65, hoa: 280 },
        { slug: 'tampa', name: 'Tampa', medianPrice: 385000, medianIncome: 65000, taxPct: 0.92, insPct: 0.52, hoa: 140 },
        { slug: 'orlando', name: 'Orlando', medianPrice: 410000, medianIncome: 64000, taxPct: 0.9, insPct: 0.5, hoa: 125 }
      ]
    },
    'new-york': {
      name: 'New York',
      slug: 'new-york',
      medianPrice: 425000,
      medianIncome: 82000,
      taxPct: 1.4,
      insPct: 0.4,
      hoa: 250,
      insight: 'NYC adds local tax and sky-high prices; upstate metros look more like the US median.',
      cities: [
        { slug: 'new-york-city', name: 'New York City', medianPrice: 725000, medianIncome: 95000, taxPct: 0.88, insPct: 0.45, hoa: 450 },
        { slug: 'buffalo', name: 'Buffalo', medianPrice: 215000, medianIncome: 58000, taxPct: 2.2, insPct: 0.35, hoa: 50 },
        { slug: 'albany', name: 'Albany', medianPrice: 285000, medianIncome: 72000, taxPct: 1.8, insPct: 0.38, hoa: 80 }
      ]
    }
  };

  function fmt(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function mortgagePayment(loan, annualRate, years) {
    var r = (annualRate / 100) / 12;
    var n = years * 12;
    if (r <= 0) return loan / n;
    var factor = (r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
    return loan * factor;
  }

  function solvePrice(paymentCap, down, annualRate, taxPct, insPct, hoa) {
    var rate = (annualRate / 100) / 12;
    var n = 360;
    var factor = rate * Math.pow(1 + rate, n) / (Math.pow(1 + rate, n) - 1);
    var taxInsMonthlyRate = (taxPct / 100 + insPct / 100) / 12;
    var fixedHoa = hoa || 0;
    var mortgageBudget = paymentCap - fixedHoa;
    if (mortgageBudget <= 0) return { price: 0, loan: 0, mortgage: 0, tax: 0, ins: 0, hoa: fixedHoa, maint: 0, piti: paymentCap };
    var denom = factor + taxInsMonthlyRate;
    var loan = (mortgageBudget - down * taxInsMonthlyRate) / denom;
    if (loan < 0) loan = 0;
    var price = loan + down;
    var mortgage = loan * factor;
    var tax = (price * taxPct / 100) / 12;
    var ins = (price * insPct / 100) / 12;
    var maint = (price * 0.01) / 12;
    var piti = mortgage + tax + ins + fixedHoa;
    return { price: price, loan: loan, mortgage: mortgage, tax: tax, ins: ins, hoa: fixedHoa, maint: maint, piti: piti };
  }

  function stressLevel(piti, monthlyGross, paymentCap, housingCap) {
    var pct = (piti / monthlyGross) * 100;
    if (paymentCap < housingCap - 1) {
      return { level: 'over', label: 'Over limit', className: 'ha-stress--over' };
    }
    if (pct > 32) return { level: 'high', label: 'Stretched', className: 'ha-stress--high' };
    if (pct > 26) return { level: 'moderate', label: 'Moderate', className: 'ha-stress--moderate' };
    return { level: 'comfortable', label: 'Comfortable', className: 'ha-stress--comfortable' };
  }

  function calc(opts) {
    opts = opts || {};
    var gross = opts.gross || 0;
    var debts = opts.debts || 0;
    var down = opts.down || 0;
    var rate = opts.rate != null ? opts.rate : 6.5;
    var regionKey = opts.region || 'national';
    var r = REGIONS[regionKey] || REGIONS.national;
    if (opts.taxPct != null) r = Object.assign({}, r, { taxPct: opts.taxPct, insPct: opts.insPct != null ? opts.insPct : r.insPct, hoa: opts.hoa != null ? opts.hoa : r.hoa });

    var monthlyGross = gross / 12;
    var housingCap = monthlyGross * 0.28;
    var totalCap = monthlyGross * 0.36 - debts;
    var paymentCap = Math.min(housingCap, totalCap);

    if (paymentCap <= 0) {
      return { ok: false, message: 'Your other monthly debts already use the 36% back-end cap. Pay debt down first, then try again.' };
    }

    var core = solvePrice(paymentCap, down, rate, r.taxPct, r.insPct, r.hoa);
    var safeLow = solvePrice(paymentCap * 0.85, down, rate, r.taxPct, r.insPct, r.hoa);
    var safeHigh = solvePrice(Math.min(paymentCap * 1.0, housingCap), down, rate, r.taxPct, r.insPct, r.hoa);
    var stress = stressLevel(core.piti, monthlyGross, paymentCap, housingCap);
    var pctGross = (core.piti / monthlyGross) * 100;

    return {
      ok: true,
      gross: gross,
      monthlyGross: monthlyGross,
      paymentCap: paymentCap,
      housingCap: housingCap,
      price: core.price,
      piti: core.piti,
      breakdown: core,
      safeRange: { low: safeLow.price, high: safeHigh.price },
      stress: stress,
      pctGross: pctGross,
      region: r
    };
  }

  function bindForm(config) {
    config = config || {};
    var form = document.getElementById(config.formId || 'ha-calc-form');
    var results = document.getElementById(config.resultsId || 'ha-calc-results');
    if (!form || !results) return;

    var ids = config.fields || {
      gross: 'ha-income',
      debts: 'ha-debt',
      down: 'ha-down',
      rate: 'ha-rate',
      region: 'ha-location'
    };

    function getRegionKey() {
      var sel = document.getElementById(ids.region);
      if (!sel) return config.defaultRegion || 'national';
      return sel.value;
    }

    function render() {
      var gross = parseFloat(document.getElementById(ids.gross).value) || 0;
      var debts = parseFloat(document.getElementById(ids.debts).value) || 0;
      var down = parseFloat(document.getElementById(ids.down).value) || 0;
      var rate = parseFloat(document.getElementById(ids.rate).value) || 6.5;
      var region = getRegionKey();
      var extra = {};
      if (config.stateSlug && STATES[config.stateSlug]) {
        var st = STATES[config.stateSlug];
        extra = { taxPct: st.taxPct, insPct: st.insPct, hoa: st.hoa };
      }
      if (config.city) {
        extra = { taxPct: config.city.taxPct, insPct: config.city.insPct, hoa: config.city.hoa };
      }
      var out = calc(Object.assign({ gross: gross, debts: debts, down: down, rate: rate, region: region }, extra));

      if (!out.ok) {
        results.innerHTML = '<p class="ha-results__empty">' + out.message + '</p>';
        results.hidden = false;
        return;
      }

      var b = out.breakdown;
      results.innerHTML =
        '<div class="ha-results__grid">' +
          '<article class="ha-results__hero">' +
            '<p class="ha-results__label">Recommended home price</p>' +
            '<p class="ha-results__price">' + fmt(out.price) + '</p>' +
            '<p class="ha-results__sub">Safe range: <strong>' + fmt(out.safeRange.low) + ' – ' + fmt(out.safeRange.high) + '</strong></p>' +
          '</article>' +
          '<article class="ha-results__stat">' +
            '<p class="ha-results__label">Monthly payment (PITI + HOA)</p>' +
            '<p class="ha-results__value">' + fmt(out.piti) + '/mo</p>' +
          '</article>' +
          '<article class="ha-results__stat">' +
            '<p class="ha-results__label">Affordability stress</p>' +
            '<p class="ha-results__stress ' + out.stress.className + '">' + out.stress.label + '</p>' +
            '<p class="ha-results__hint">' + out.pctGross.toFixed(0) + '% of gross pay · cap ' + fmt(out.paymentCap) + '/mo</p>' +
          '</article>' +
        '</div>' +
        '<div class="ha-breakdown" aria-label="Payment breakdown">' +
          '<h3 class="ha-breakdown__title">Affordability breakdown</h3>' +
          '<div class="ha-breakdown__cards">' +
            breakdownCard('Mortgage', b.mortgage, 'Principal + interest on your loan') +
            breakdownCard('Property tax', b.tax, 'Based on local effective rate') +
            breakdownCard('Insurance', b.ins, 'Homeowners — shop quotes') +
            breakdownCard('HOA', b.hoa, b.hoa ? 'Monthly association fee' : 'Often $0 outside condos') +
            breakdownCard('Maintenance', b.maint, 'Budget ~1% of home value per year') +
          '</div>' +
        '</div>';
      results.hidden = false;
    }

    function breakdownCard(title, amount, note) {
      return '<article class="ha-breakdown__card"><h4>' + title + '</h4><p class="ha-breakdown__amt">' + fmt(amount) + '<span>/mo</span></p><p class="ha-breakdown__note">' + note + '</p></article>';
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      render();
    });
    var btn = form.querySelector('[type="submit"], .ha-calc__btn');
    if (btn) btn.addEventListener('click', function (e) { e.preventDefault(); render(); });

    if (config.runOnLoad !== false) render();
  }

  global.HouseAfford = {
    REGIONS: REGIONS,
    STATES: STATES,
    fmt: fmt,
    calc: calc,
    bindForm: bindForm,
    mortgagePayment: mortgagePayment,
    solvePrice: solvePrice
  };
})(typeof window !== 'undefined' ? window : this);
