/**
 * Income Reality Calculator — Austin salary scenario pages
 */
(function () {
  'use strict';

  var TAKE_HOME_LOW = 0.768;
  var TAKE_HOME_HIGH = 0.816;
  var DEFAULT_EXPENSES = {
    single: { utilities: 180, groceries: 450, transport: 450, healthcare: 300, entertainment: 250 },
    couple: { utilities: 220, groceries: 650, transport: 520, healthcare: 450, entertainment: 350 },
    family4: { utilities: 280, groceries: 900, transport: 580, healthcare: 550, entertainment: 300, childcare: 1200 }
  };

  function fmt(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function el(id) {
    return document.getElementById(id);
  }

  function takeHomeMonthly(gross) {
    var low = (gross * TAKE_HOME_LOW) / 12;
    var high = (gross * TAKE_HOME_HIGH) / 12;
    return { low: low, high: high, mid: (low + high) / 2 };
  }

  function comfortScore(housingRatio, disposable, household) {
    var score = 78;
    if (housingRatio > 35) score -= 12;
    else if (housingRatio > 30) score -= 6;
    if (disposable < 500) score -= 18;
    else if (disposable < 1000) score -= 10;
    else if (disposable > 2000) score += 8;
    if (household === 'family4') score -= 8;
    return Math.max(25, Math.min(95, Math.round(score)));
  }

  function run() {
    var form = el('ss-calc-form');
    if (!form) return;

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      update();
    });

    ['ss-salary', 'ss-household', 'ss-rent', 'ss-savings'].forEach(function (id) {
      var node = el(id);
      if (node) node.addEventListener('input', update);
      if (node) node.addEventListener('change', update);
    });

    update();
  }

  function update() {
    var gross = Number(el('ss-salary').value) || 75000;
    var household = el('ss-household').value || 'single';
    var rent = Number(el('ss-rent').value) || 1700;
    var savingsGoal = Number(el('ss-savings').value) || 400;
    var exp = DEFAULT_EXPENSES[household] || DEFAULT_EXPENSES.single;

    var takeHome = takeHomeMonthly(gross);
    var monthlyExpenses = rent + exp.utilities + exp.groceries + exp.transport + exp.healthcare + exp.entertainment + (exp.childcare || 0);
    var disposable = takeHome.mid - monthlyExpenses - savingsGoal;
    var housingRatio = takeHome.mid > 0 ? (rent / takeHome.mid) * 100 : 0;
    var score = comfortScore(housingRatio, disposable, household);

    setOut('ss-out-takehome', fmt(takeHome.low) + ' – ' + fmt(takeHome.high));
    setOut('ss-out-disposable', fmt(disposable));
    setOut('ss-out-housing-ratio', Math.round(housingRatio) + '%');
    setOut('ss-out-comfort', score + '/100');

    var disposableNode = el('ss-out-disposable');
    disposableNode.classList.remove('ss-out--pos', 'ss-out--warn', 'ss-out--neg');
    if (disposable >= 1200) disposableNode.classList.add('ss-out--pos');
    else if (disposable >= 400) disposableNode.classList.add('ss-out--warn');
    else disposableNode.classList.add('ss-out--neg');

    var scoreNode = el('ss-out-comfort');
    scoreNode.classList.remove('ss-out--pos', 'ss-out--warn', 'ss-out--neg');
    if (score >= 70) scoreNode.classList.add('ss-out--pos');
    else if (score >= 50) scoreNode.classList.add('ss-out--warn');
    else scoreNode.classList.add('ss-out--neg');
  }

  function setOut(id, text) {
    var node = el(id);
    if (!node) return;
    var strong = node.querySelector('strong');
    if (strong) strong.textContent = text;
    else node.textContent = text;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
})();
