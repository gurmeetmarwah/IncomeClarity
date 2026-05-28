/**
 * Moving cost calculator — hub and geo pages
 */
(function (global) {
  'use strict';

  var SIZE_MULT = { studio: 0.7, '1br': 1, '2br': 1.35, '3br': 1.75 };
  var MOVE_RATE = {
    diy: { base: 180, perMile: 0.55 },
    truck: { base: 420, perMile: 1.05 },
    movers: { base: 900, perMile: 2.35 }
  };

  function fmt(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function fmtRange(lo, hi) {
    return fmt(lo) + '–' + fmt(hi);
  }

  function fmtSigned(n, suffix) {
    var sign = n > 0 ? '+' : n < 0 ? '−' : '';
    return sign + fmt(Math.abs(n)) + (suffix || '');
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

  function setWidth(id, pct) {
    var node = el(id);
    if (node) node.style.width = Math.max(0, Math.min(100, pct)) + '%';
  }

  function readCatalog() {
    var node = el('mc-catalog');
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

  function estMiles(fromId, toId, map) {
    if (!fromId || !toId) return 500;
    if (fromId === toId) return 35;
    var a = map[fromId];
    var b = map[toId];
    if (!a || !b) return 800;
    if (a.state === b.state) return 280;
    if (a.region === b.region) return 650;
    var west = { west: 1, south: 1, northeast: 1, midwest: 1 };
    if (a.region && b.region && a.region !== b.region) {
      if (
        (a.region === 'west' && b.region === 'northeast') ||
        (a.region === 'northeast' && b.region === 'west')
      ) {
        return 2800;
      }
      if (a.region === 'midwest' || b.region === 'midwest') return 1200;
      return 1600;
    }
    return 900;
  }

  function monthlyBundle(c) {
    if (!c) return 0;
    return c.rent + c.groceries + c.utilities + c.transport + c.taxes;
  }

  function moveServicesCost(type, miles, sizeKey, family) {
    var rate = MOVE_RATE[type] || MOVE_RATE.truck;
    var mult = SIZE_MULT[sizeKey] || 1;
    var fam = Math.max(1, family);
    var core = (rate.base + rate.perMile * miles) * mult;
    var low = core * 0.88;
    var high = core * (1.12 + fam * 0.04);
    return { low: low, high: high, mid: (low + high) / 2 };
  }

  function calc(opts) {
    var map = opts.map;
    var fromId = opts.from;
    var toId = opts.to;
    var miles = opts.miles;
    var type = opts.moveType;
    var size = opts.size;
    var family = opts.family;
    var pets = opts.pets;
    var tempHousing = opts.tempHousing;
    var flights = opts.flights;
    var storage = opts.storage;
    var vehicle = opts.vehicle;

    var from = map[fromId];
    var to = map[toId];
    if (!miles || miles < 1) miles = estMiles(fromId, toId, map);

    var move = moveServicesCost(type, miles, size, family);
    var destRent = to ? to.rent * (SIZE_MULT[size] || 1) : 1800;
    var deposits = destRent * 1.5;
    var firstMonth = destRent;
    var utilitySetup = 220 + family * 25;
    var furnish = 350 + (SIZE_MULT[size] || 1) * 280;
    var travel = 180 + family * 120 + (flights ? 450 * Math.min(family, 4) : 0);
    var storageCost = storage ? 180 + (SIZE_MULT[size] || 1) * 90 : 0;
    var vehicleCost = vehicle ? 950 + miles * 0.35 : 0;
    var petsCost = pets ? 175 : 0;
    var tempCost = tempHousing ? 140 * 7 : 0;

    var immediate =
      deposits +
      firstMonth +
      move.mid +
      utilitySetup +
      furnish * 0.65 +
      travel +
      storageCost +
      vehicleCost +
      petsCost +
      tempCost;

    var immediateLow = immediate * 0.9;
    var immediateHigh = immediate * 1.15;

    var monthlyFrom = monthlyBundle(from);
    var monthlyTo = monthlyBundle(to);
    var monthlyDiff = monthlyTo - monthlyFrom;

    return {
      moveLow: move.low,
      moveHigh: move.high,
      immediateLow: immediateLow,
      immediateHigh: immediateHigh,
      monthlyDiff: monthlyDiff,
      miles: miles,
      breakdown: {
        moving: move,
        deposits: deposits,
        firstMonth: firstMonth,
        travel: travel,
        utilitySetup: utilitySetup,
        furnish: furnish,
        storage: storageCost,
        vehicle: vehicleCost,
        pets: petsCost,
        temp: tempCost
      },
      from: from,
      to: to
    };
  }

  function affordStress(salary, savings, debt, emergency, monthlyDiff) {
    var net = (salary / 12) * 0.73;
    var cushion = savings + emergency;
    var monthsCover = net > 0 ? cushion / net : 0;
    var debtLoad = debt / Math.max(1, net);
    var hit = monthlyDiff > 0 ? monthlyDiff / Math.max(1, net) : 0;
    var score = 0;
    if (monthsCover < 2) score += 2;
    else if (monthsCover < 4) score += 1;
    if (debtLoad > 0.2) score += 2;
    else if (debtLoad > 0.12) score += 1;
    if (hit > 0.12) score += 2;
    else if (hit > 0.06) score += 1;
    if (score <= 1) return { level: 'Comfortable', note: 'Your savings and income look able to handle this move with planning.' };
    if (score <= 3) return { level: 'Moderate', note: 'This move is possible, but build a larger cash buffer before lease signing.' };
    return { level: 'High risk', note: 'Monthly costs or debt may squeeze savings. Delay the move or cut fixed costs first.' };
  }

  function bindForm(options) {
    options = options || {};
    var form = el('mc-calc-form');
    if (!form) return;

    var catalog = readCatalog();
    var map = catalogMap(catalog);
    var scenario = { family: 0, moveType: null, size: null, milesBoost: 0 };
    var latestResult = null;

    function fillCitySelects() {
      var fromSel = el('mc-from');
      var toSel = el('mc-to');
      var affordFrom = el('mc-afford-from');
      var affordTo = el('mc-afford-to');
      if (!fromSel || !toSel) return;
      var html = '<option value="">Select city</option>';
      catalog.forEach(function (c) {
        html += '<option value="' + c.id + '">' + c.name + ', ' + c.stateName + '</option>';
      });
      fromSel.innerHTML = html;
      toSel.innerHTML = html;
      if (affordFrom) affordFrom.innerHTML = html;
      if (affordTo) affordTo.innerHTML = html;
      if (options.defaultFrom) fromSel.value = options.defaultFrom;
      if (options.defaultTo) toSel.value = options.defaultTo;
      if (affordFrom && options.defaultFrom) affordFrom.value = options.defaultFrom;
      if (affordTo && options.defaultTo) affordTo.value = options.defaultTo;
    }

    function readInputs() {
      var milesInput = num('mc-distance', 0);
      var fromId = el('mc-from') ? el('mc-from').value : '';
      var toId = el('mc-to') ? el('mc-to').value : '';
      if (!milesInput && fromId && toId) {
        milesInput = estMiles(fromId, toId, map) + scenario.milesBoost;
        if (el('mc-distance')) el('mc-distance').value = Math.round(milesInput);
      }
      var moveType = scenario.moveType || (el('mc-move-type') ? el('mc-move-type').value : 'truck');
      var size = scenario.size || (el('mc-size') ? el('mc-size').value : '1br');
      var family = scenario.family || num('mc-family', 1);
      return {
        from: fromId,
        to: toId,
        miles: milesInput + scenario.milesBoost,
        moveType: moveType,
        size: size,
        family: family,
        pets: el('mc-pets') && el('mc-pets').checked,
        tempHousing: el('mc-temp') && el('mc-temp').checked,
        flights: el('mc-flights') && el('mc-flights').checked,
        storage: el('mc-storage') && el('mc-storage').checked,
        vehicle: el('mc-vehicle') && el('mc-vehicle').checked,
        map: map
      };
    }

    function renderResults(r) {
      latestResult = r;
      var moveRange = el('mc-move-range');
      if (moveRange) moveRange.textContent = fmtRange(r.moveLow, r.moveHigh);
      var imm = el('mc-immediate');
      if (imm) imm.textContent = fmtRange(r.immediateLow, r.immediateHigh);
      var diff = el('mc-monthly-diff');
      if (diff) {
        var sign = r.monthlyDiff >= 0 ? '+' : '−';
        var city = r.to ? r.to.name : 'destination';
        diff.textContent = sign + ' ' + fmt(Math.abs(r.monthlyDiff)) + '/month in ' + city;
        diff.className = 'mc-result-delta ' + (r.monthlyDiff >= 0 ? 'mc-result-delta--up' : 'mc-result-delta--down');
      }

      var list = el('mc-immediate-list');
      if (list) {
        var b = r.breakdown;
        list.innerHTML =
          '<li>Deposits &amp; first month rent</li>' +
          '<li>Moving services (' + fmtRange(r.moveLow, r.moveHigh) + ')</li>' +
          '<li>Utility setup &amp; essentials</li>' +
          (b.storage ? '<li>Storage</li>' : '') +
          (b.vehicle ? '<li>Vehicle transport</li>' : '') +
          (b.temp ? '<li>Temporary housing</li>' : '');
      }

      updateBreakdownCards(r);
      updateCityCompare(r);
      updateAfford(r);
    }

    function updateBreakdownCards(r) {
      var b = r.breakdown;
      var m = r.breakdown.moving;

      var mix = {
        moving: m.mid,
        deposits: b.deposits + b.firstMonth,
        travel: b.travel,
        util: b.utilitySetup,
        furnish: b.furnish,
        temp: b.temp,
        storage: b.storage,
        vehicle: b.vehicle
      };
      var total = 0;
      Object.keys(mix).forEach(function (k) { total += mix[k]; });
      if (total < 1) total = 1;

      Object.keys(mix).forEach(function (k) {
        var amount = mix[k];
        var pct = (amount / total) * 100;
        setText('mc-mix-' + k + '-value', fmt(amount));
        setText('mc-mix-' + k + '-pct', Math.round(pct) + '%');
        setWidth('mc-mix-' + k + '-bar', pct);
      });
    }

    function updateCityCompare(r) {
      if (!r.from || !r.to) return;
      setText('mc-compare-from', r.from.name);
      setText('mc-compare-to', r.to.name);
      var rent = r.to.rent - r.from.rent;
      var gro = r.to.groceries - r.from.groceries;
      var tax = r.to.taxes - r.from.taxes;
      var trans = r.to.transport - r.from.transport;
      var maxAbs = Math.max(1, Math.abs(rent), Math.abs(gro), Math.abs(tax), Math.abs(trans));
      setText('mc-diff-rent', fmtSigned(rent, '/mo'));
      setText('mc-diff-gro', fmtSigned(gro, '/mo'));
      setText('mc-diff-tax', fmtSigned(tax, '/mo'));
      setText('mc-diff-trans', fmtSigned(trans, '/mo'));
      setText('mc-compare-net', 'Net monthly impact: ' + fmtSigned(r.monthlyDiff, '/mo'));
      ['mc-diff-rent', 'mc-diff-gro', 'mc-diff-tax', 'mc-diff-trans'].forEach(function (id) {
        var node = el(id);
        if (!node) return;
        var v = id === 'mc-diff-rent' ? rent : id === 'mc-diff-gro' ? gro : id === 'mc-diff-tax' ? tax : trans;
        node.className = v > 0 ? 'mc-compare-delta mc-compare-delta--up' : v < 0 ? 'mc-compare-delta mc-compare-delta--down' : 'mc-compare-delta';
      });
      [
        ['mc-diff-rent-bar', rent],
        ['mc-diff-gro-bar', gro],
        ['mc-diff-tax-bar', tax],
        ['mc-diff-trans-bar', trans]
      ].forEach(function (pair) {
        var bar = el(pair[0]);
        if (!bar) return;
        var v = pair[1];
        bar.style.width = Math.round((Math.abs(v) / maxAbs) * 100) + '%';
        bar.className = v > 0 ? 'mc-compare-mini__fill mc-compare-mini__fill--up' : v < 0 ? 'mc-compare-mini__fill mc-compare-mini__fill--down' : 'mc-compare-mini__fill';
      });
      var net = el('mc-compare-net');
      if (net) {
        net.className = r.monthlyDiff > 0 ? 'mc-compare-pill mc-compare-pill--up' : r.monthlyDiff < 0 ? 'mc-compare-pill mc-compare-pill--down' : 'mc-compare-pill';
      }
    }

    function updateAfford(r) {
      var salary = num('mc-salary', 85000);
      var savings = num('mc-savings', 12000);
      var debt = num('mc-debt', 400);
      var emergency = num('mc-emergency', 5000);
      var saveGoal = num('mc-save-goal', 600);
      var net = (salary / 12) * 0.73;
      var essentials = net * 0.42;
      var costIncrease = Math.max(0, r.monthlyDiff);
      var monthlyLeft = net - essentials - debt - costIncrease;
      var cashLeft = savings - emergency - r.immediateHigh;
      var burn = Math.max(1, essentials + debt + costIncrease);
      var runway = cashLeft > 0 ? cashLeft / burn : 0;
      var stress = affordStress(salary, savings, debt, emergency, r.monthlyDiff);
      var recommended = Math.max(r.immediateHigh * 1.2, burn * 3 + saveGoal * 3);
      setText('mc-afford-level', stress.level);
      setText('mc-afford-note', stress.note);
      setText('mc-afford-buffer', fmt(recommended));
      setText('mc-afford-cash-left', fmt(cashLeft));
      setText('mc-afford-monthly-left', fmt(monthlyLeft));
      setText('mc-afford-runway', (runway > 0 ? runway.toFixed(1) : '0') + ' months');

      var saveHit = r.monthlyDiff > 0 ? Math.round((r.monthlyDiff / Math.max(1, net)) * 100) : 0;
      var saveGap = monthlyLeft - saveGoal;
      setText(
        'mc-afford-save-hit',
        saveHit > 0
          ? 'This move may raise monthly costs by about ' + saveHit + '% of take-home pay. Savings goal gap: ' + fmt(saveGap) + '/mo.'
          : 'Monthly costs may stay flat or improve after this move. Savings goal gap: ' + fmt(saveGap) + '/mo.'
      );

      setWidth('mc-afford-cash-meter', (Math.max(0, savings - emergency) / Math.max(1, recommended)) * 100);
      setWidth('mc-afford-runway-meter', (runway / 6) * 100);

      if (cashLeft < 0) {
        setText('mc-afford-action-1', 'Delay move or cut one-time costs: you are short ' + fmt(Math.abs(cashLeft)) + ' after protecting emergency cash.');
      } else {
        setText('mc-afford-action-1', 'You keep about ' + fmt(cashLeft) + ' after move-in. Keep this as post-move contingency, not furnishing spend.');
      }
      if (monthlyLeft < saveGoal) {
        setText('mc-afford-action-2', 'Monthly plan is tight. Reduce rent target or debt by about ' + fmt(Math.abs(monthlyLeft - saveGoal)) + '/mo.');
      } else {
        setText('mc-afford-action-2', 'Monthly plan supports your savings goal with about ' + fmt(monthlyLeft - saveGoal) + '/mo extra room.');
      }
      setText('mc-afford-action-3', 'Before committing, confirm deposits, utility setup fees, and first 60-day cash needs in writing.');

      ['mc-step-ready', 'mc-step-almost', 'mc-step-notyet'].forEach(function (id) {
        var n = el(id);
        if (n) n.className = 'mc-afford-step';
      });
      if (stress.level === 'Comfortable') {
        var ready = el('mc-step-ready');
        if (ready) ready.className = 'mc-afford-step mc-afford-step--active mc-afford-step--ready';
      } else if (stress.level === 'Moderate') {
        var almost = el('mc-step-almost');
        if (almost) almost.className = 'mc-afford-step mc-afford-step--active mc-afford-step--almost';
      } else {
        var notyet = el('mc-step-notyet');
        if (notyet) notyet.className = 'mc-afford-step mc-afford-step--active mc-afford-step--notyet';
      }
    }

    function setText(id, value) {
      var node = el(id);
      if (node) node.textContent = value;
    }

    function run() {
      var inp = readInputs();
      if (!inp.from || !inp.to) return;
      renderResults(calc(inp));
    }

    function runAffordOnly() {
      if (!latestResult) return;
      updateAfford(latestResult);
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      scenario = { family: 0, moveType: null, size: null, milesBoost: 0 };
      run();
    });

    ['mc-from', 'mc-to', 'mc-distance', 'mc-move-type', 'mc-size', 'mc-family', 'mc-pets', 'mc-temp', 'mc-flights', 'mc-storage', 'mc-vehicle'].forEach(function (id) {
      var node = el(id);
      if (!node) return;
      node.addEventListener('change', run);
      node.addEventListener('input', run);
    });

    var syncFrom = el('mc-afford-from');
    var syncTo = el('mc-afford-to');
    if (syncFrom) {
      syncFrom.addEventListener('change', function () {
        if (el('mc-from')) el('mc-from').value = syncFrom.value;
        run();
      });
    }
    if (syncTo) {
      syncTo.addEventListener('change', function () {
        if (el('mc-to')) el('mc-to').value = syncTo.value;
        run();
      });
    }

    ['mc-salary', 'mc-savings', 'mc-debt', 'mc-emergency', 'mc-save-goal'].forEach(function (id) {
      var node = el(id);
      if (!node) return;
      node.addEventListener('input', runAffordOnly);
      node.addEventListener('change', runAffordOnly);
    });

    fillCitySelects();
    var fromMain = el('mc-from');
    var toMain = el('mc-to');
    if (fromMain && syncFrom) {
      fromMain.addEventListener('change', function () { syncFrom.value = fromMain.value; });
    }
    if (toMain && syncTo) {
      toMain.addEventListener('change', function () { syncTo.value = toMain.value; });
    }
    if (options.runOnLoad !== false) run();
  }

  function init() {
    bindForm({ runOnLoad: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else init();

  global.MovingCost = { calc: calc, bindForm: bindForm, fmt: fmt };
})(typeof window !== 'undefined' ? window : this);
