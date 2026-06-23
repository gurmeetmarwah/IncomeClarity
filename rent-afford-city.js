/**
 * Rent affordability — city landing pages
 */
(function () {
  'use strict';

  function fmt(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function el(id) {
    return document.getElementById(id);
  }

  function num(id, fallback) {
    var node = el(id);
    if (!node) return fallback || 0;
    var v = parseFloat(node.value);
    return isNaN(v) ? (fallback || 0) : v;
  }

  function readCityData() {
    var node = document.getElementById('ra-city-data');
    if (!node) return null;
    try {
      return JSON.parse(node.textContent || '{}');
    } catch (e) {
      return null;
    }
  }

  function calcRent(data, income, debt, family, savePct) {
    var net = (income / 12) * (data.taxTakehome || 0.73);
    var grossMonthly = income / 12;
    var baseEss = 0.3 + Math.min(0.07, family * 0.01);
    var debtPct = debt / Math.max(1, net);
    var save = savePct / 100;
    var comfortPct = Math.max(0.2, 1 - baseEss - save - debtPct - 0.08);
    comfortPct = Math.min(0.38, comfortPct);
    var comfortFromNet = net * comfortPct;
    var comfortFromGross = grossMonthly * 0.3;
    var comfort = Math.min(comfortFromNet, comfortFromGross);
    return {
      net: net,
      low: comfort * 0.88,
      high: comfort * 1.03,
      stretch: comfort * 1.15,
      income: income
    };
  }

  function verdict(comfortHigh, stretch, median) {
    if (comfortHigh >= median * 0.98) {
      return { label: 'Comfortable', cls: 'ra-verdict--good' };
    }
    if (stretch >= median) {
      return { label: 'Stretch', cls: 'ra-verdict--mid' };
    }
    return { label: 'Tight', cls: 'ra-verdict--risk' };
  }

  function update(data) {
    var income = num('ra-city-income', data.defaultIncome);
    var debt = num('ra-city-debt', data.defaultDebt);
    var family = num('ra-city-family', data.defaultFamily);
    var save = num('ra-city-save', data.defaultSave);
    var r = calcRent(data, income, debt, family, save);
    var v = verdict(r.high, r.stretch, data.medianRent);

    setText('ra-ci-income', fmt(r.income));
    setText('ra-ci-comfort', fmt(r.low) + ' – ' + fmt(r.high) + '/month');
    setText('ra-ci-stretch', fmt(r.stretch) + '/month');
    setText('ra-ci-median', fmt(data.medianRent) + '/month');

    var verdictEl = el('ra-ci-verdict');
    if (verdictEl) {
      verdictEl.textContent = v.label;
      verdictEl.className = 'ra-verdict ' + v.cls;
    }

    var summary = el('ra-ci-summary');
    if (summary) {
      summary.textContent =
        'At ' + fmt(r.income) + ' gross and about ' + fmt(r.net) + '/mo take-home, a comfortable rent target is ' +
        fmt(r.low) + '–' + fmt(r.high) + '. Median local rent is ' + fmt(data.medianRent) + ' — verdict: ' + v.label + '.';
    }
  }

  function setText(id, value) {
    var node = el(id);
    if (node) node.textContent = value;
  }

  function init() {
    var data = readCityData();
    if (!data) return;

    var form = el('ra-city-form');
    if (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        update(data);
      });
    }

    ['ra-city-income', 'ra-city-debt', 'ra-city-family', 'ra-city-save'].forEach(function (id) {
      var node = el(id);
      if (!node) return;
      node.addEventListener('input', function () {
        update(data);
      });
      node.addEventListener('change', function () {
        update(data);
      });
    });

    update(data);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
