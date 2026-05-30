/**
 * Comfortable salary calculator — hub, state, and city pages
 */
(function (global) {
  'use strict';

  var LIFESTYLE = {
    basic: { label: 'Basic Lifestyle', mult: 0.72, savings: 0.06 },
    comfortable: { label: 'Comfortable Lifestyle', mult: 1, savings: 0.12 },
    comfortable_plus: { label: 'Comfortable Plus', mult: 1.32, savings: 0.15 },
    high_comfort: { label: 'Affluent Lifestyle', mult: 1.75, savings: 0.18 }
  };

  var HOUSEHOLD = {
    single: { coreMult: 1, grossShare: 0.43, childcare: 0 },
    couple: { coreMult: 1.38, grossShare: 0.45, childcare: 0 },
    family4: { coreMult: 1.35, grossShare: 0.48, childcare: 1400 }
  };

  var HOUSING = { rent: 1, own: 1.16 };

  function fmt(n) {
    if (n >= 1000000) return '$' + (n / 1000000).toFixed(1).replace('.0', '') + 'M+';
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function el(id) {
    return document.getElementById(id);
  }

  function readCatalog() {
    var node = el('cs-catalog');
    if (!node) return [];
    try {
      return JSON.parse(node.textContent || '[]');
    } catch (e) {
      return [];
    }
  }

  function catalogMap(list) {
    var m = {};
    list.forEach(function (c) {
      m[c.id] = c;
    });
    return m;
  }

  function coreMonthly(c) {
    return c.rent + c.groceries + c.utilities + c.transport;
  }

  function roundSalary(n) {
    return Math.round(n / 5000) * 5000;
  }

  function compute(city, household, housing, lifestyleKey) {
    var hh = HOUSEHOLD[household] || HOUSEHOLD.single;
    var ho = HOUSING[housing] || HOUSING.rent;
    var life = LIFESTYLE[lifestyleKey] || LIFESTYLE.comfortable;
    var col = (city.colIndex || 100) / 100;
    var core = coreMonthly(city);

    var monthlyCore = core * hh.coreMult * ho * life.mult;
    var childcare = hh.childcare * col * (household === 'family4' ? 1 : 0);
    if (household === 'family4' && (lifestyleKey === 'comfortable_plus' || lifestyleKey === 'high_comfort')) {
      childcare *= 1.15;
    }
    var essentials = monthlyCore + childcare;
    var savings = essentials * life.savings;
    var monthly = essentials + savings;
    var annual = roundSalary((monthly * 12) / hh.grossShare);

    var housingAmt = city.rent * hh.coreMult * ho * life.mult + city.utilities * 0.85;
    var foodAmt = city.groceries * hh.coreMult * life.mult * 1.1;
    var transportAmt = city.transport * hh.coreMult * life.mult;
    var lifestyleAmt = Math.max(280, 420 * col * life.mult * (0.6 + hh.coreMult * 0.15));
    var buckets = {
      housing: housingAmt,
      transportation: transportAmt,
      food: foodAmt,
      childcare: childcare,
      savings: savings,
      lifestyle: lifestyleAmt
    };
    var total = 0;
    Object.keys(buckets).forEach(function (k) { total += buckets[k]; });
    if (total < 1) total = 1;
    var breakdown = {};
    Object.keys(buckets).forEach(function (k) {
      breakdown[k] = { amount: Math.round(buckets[k]), pct: Math.round(buckets[k] / total * 100) };
    });

    return { annual: annual, monthly: Math.round(monthly), breakdown: breakdown, lifestyleKey: lifestyleKey };
  }

  function lifestyleRange(city, household, housing) {
    var out = {};
    Object.keys(LIFESTYLE).forEach(function (k) {
      out[k] = compute(city, household, housing, k).annual;
    });
    return out;
  }

  function bindForm(options) {
    options = options || {};
    var form = el('cs-calc-form');
    if (!form) return;

    var catalog = readCatalog();
    var map = catalogMap(catalog);

    function fillSelects() {
      var stateSel = el('cs-state');
      var citySel = el('cs-city');
      if (!stateSel || !citySel) return;
      var states = {};
      catalog.forEach(function (c) {
        if (c.state && c.stateName) states[c.state] = c.stateName;
      });
      var stateHtml = '<option value="">Select state</option>';
      Object.keys(states).sort(function (a, b) {
        return states[a].localeCompare(states[b]);
      }).forEach(function (slug) {
        stateHtml += '<option value="' + slug + '">' + states[slug] + '</option>';
      });
      stateSel.innerHTML = stateHtml;

      function fillCities(stateSlug) {
        var html = '<option value="">Select city (optional)</option>';
        catalog.forEach(function (c) {
          if (c.id.indexOf('/') === -1 || c.state !== stateSlug) return;
          html += '<option value="' + c.id + '">' + c.name + '</option>';
        });
        citySel.innerHTML = html;
      }

      stateSel.addEventListener('change', function () {
        fillCities(stateSel.value);
        run();
      });

      if (options.defaultState && states[options.defaultState]) {
        stateSel.value = options.defaultState;
      }
      fillCities(stateSel.value || options.defaultState || '');
      if (options.defaultCity) {
        citySel.value = options.defaultCity;
        if (!citySel.value && options.defaultState) {
          fillCities(options.defaultState);
          citySel.value = options.defaultCity;
        }
      }
    }

    function getCity() {
      var cityId = el('cs-city') && el('cs-city').value;
      var stateId = el('cs-state') && el('cs-state').value;
      if (cityId && map[cityId]) return map[cityId];
      if (stateId && map[stateId]) return map[stateId];
      return catalog[0] || null;
    }

    function readInputs() {
      var city = getCity();
      if (!city) return null;
      return {
        city: city,
        household: el('cs-household') ? el('cs-household').value : 'single',
        housing: el('cs-housing') ? el('cs-housing').value : 'rent'
      };
    }

    function renderBreakdown(breakdown) {
      var labels = {
        housing: 'Housing',
        transportation: 'Transportation',
        food: 'Food',
        childcare: 'Childcare',
        savings: 'Savings',
        lifestyle: 'Lifestyle Spending'
      };
      Object.keys(labels).forEach(function (key) {
        var b = breakdown[key];
        if (!b) return;
        var val = el('cs-mix-' + key + '-value');
        var pct = el('cs-mix-' + key + '-pct');
        var bar = el('cs-mix-' + key + '-bar');
        if (val) val.textContent = fmt(b.amount);
        if (pct) pct.textContent = b.pct + '%';
        if (bar) bar.style.width = b.pct + '%';
      });
    }

    function renderResults(inp) {
      var range = lifestyleRange(inp.city, inp.household, inp.housing);
      var tiers = ['basic', 'comfortable', 'comfortable_plus', 'high_comfort'];
      tiers.forEach(function (k) {
        var node = el('cs-tier-' + k);
        if (node) node.textContent = fmt(range[k]);
      });
      var active = compute(inp.city, inp.household, inp.housing, 'comfortable');
      renderBreakdown(active.breakdown);
      var loc = el('cs-result-location');
      if (loc) loc.textContent = inp.city.name + (inp.city.stateName ? ', ' + inp.city.stateName : '');
    }

    function run() {
      var inp = readInputs();
      if (!inp) return;
      renderResults(inp);
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      run();
    });

    ['cs-city', 'cs-household', 'cs-housing'].forEach(function (id) {
      var node = el(id);
      if (!node) return;
      node.addEventListener('change', run);
      node.addEventListener('input', run);
    });

    fillSelects();
    if (options.runOnLoad !== false) run();

    // What-if buttons
    document.querySelectorAll('[data-cs-whatif]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var action = btn.getAttribute('data-cs-whatif');
        if (action === 'texas' && el('cs-state')) {
          el('cs-state').value = 'texas';
          el('cs-state').dispatchEvent(new Event('change'));
          if (el('cs-city')) el('cs-city').value = 'texas/austin';
        } else if (action === 'child' && el('cs-household')) {
          el('cs-household').value = 'family4';
        } else if (action === 'own' && el('cs-housing')) {
          el('cs-housing').value = 'own';
        }
        run();
        var out = el('cs-whatif-result');
        if (out) {
          var inp = readInputs();
          if (inp) {
            var r = lifestyleRange(inp.city, inp.household, inp.housing);
            if (action === 'debt') {
              out.textContent =
                'Basic tier: ' + fmt(r.basic) + '. Comfortable tier: ' + fmt(r.comfortable) + ' in ' + inp.city.name + '.';
            } else {
              out.textContent = 'Updated comfortable target: ' + fmt(r.comfortable) + ' in ' + inp.city.name + '.';
            }
          }
        }
      });
    });
  }

  function init() {
    var page = document.body && document.body.getAttribute('data-cs-page');
    var opts = { runOnLoad: true };
    if (page === 'state') {
      opts.defaultState = document.body.getAttribute('data-cs-state') || '';
    } else if (page === 'city') {
      opts.defaultState = document.body.getAttribute('data-cs-state') || '';
      opts.defaultCity = document.body.getAttribute('data-cs-city') || '';
    }
    bindForm(opts);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  global.ComfortableSalary = { compute: compute, lifestyleRange: lifestyleRange, fmt: fmt, bindForm: bindForm };
})(typeof window !== 'undefined' ? window : this);
