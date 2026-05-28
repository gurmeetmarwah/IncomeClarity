(function () {
  function el(id) { return document.getElementById(id); }
  function money(n) { return "$" + Math.round(n).toLocaleString(); }
  function roomLabel(n) {
    if (n >= 0) return money(n) + "/month surplus";
    return money(Math.abs(n)) + "/month deficit";
  }
  var cityData = {
    nyc: { name: "NYC", rent: 2800, util: 220, groceries: 540, transport: 210, comfortable: 112000 },
    sf: { name: "San Francisco", rent: 3000, util: 210, groceries: 520, transport: 180, comfortable: 122000 },
    la: { name: "Los Angeles", rent: 2450, util: 210, groceries: 500, transport: 360, comfortable: 98000 },
    austin: { name: "Austin", rent: 1650, util: 180, groceries: 410, transport: 280, comfortable: 76000 },
    chicago: { name: "Chicago", rent: 1800, util: 190, groceries: 430, transport: 220, comfortable: 82000 },
    atlanta: { name: "Atlanta", rent: 1600, util: 190, groceries: 400, transport: 290, comfortable: 74000 }
  };

  function lifestyleMult(level) {
    if (level === "minimal") return 0.85;
    if (level === "flexible") return 1.15;
    if (level === "premium") return 1.35;
    return 1;
  }

  function scoreLabel(score) {
    if (score < 35) return "Struggling";
    if (score < 50) return "Tight";
    if (score < 68) return "Comfortable";
    if (score < 83) return "Strong";
    return "Very Safe";
  }

  function scoreText(label, cityName, margin, save) {
    if (label === "Struggling") return "Living alone in " + cityName + " is likely too tight right now. Your budget shows very little room for shocks.";
    if (label === "Tight") return "You can technically afford living alone in " + cityName + ", but your margin for emergencies and savings may feel stressful.";
    if (label === "Comfortable") return "You're likely able to live alone comfortably while still saving consistently.";
    if (label === "Strong") return "You have healthy breathing room in " + cityName + ". You can save, handle surprises, and keep lifestyle flexibility.";
    return "Your solo budget looks very safe in " + cityName + ". You have strong resilience and room for long-term goals.";
  }

  function run() {
    var salary = +el("sla-salary").value || 0;
    var cityKey = el("sla-city").value;
    var city = cityData[cityKey];
    var debt = +el("sla-debt").value || 0;
    var goal = +el("sla-goal").value || 0;
    var life = el("sla-life").value;

    var student = el("sla-student").checked ? 220 : 0;
    var car = el("sla-car").checked ? 320 : 0;
    var pet = el("sla-pet").checked ? 95 : 0;
    var remote = el("sla-remote").checked ? -120 : 0;

    var netMonthly = salary * 0.72 / 12;
    var rent = city.rent;
    var utilities = city.util;
    var groceries = city.groceries;
    var transport = Math.max(90, city.transport + remote);
    var entertainment = 260 * lifestyleMult(life);
    var emergency = Math.max(120, netMonthly * 0.08);
    var debtTotal = debt + student + car;
    var savings = goal;

    var essentials = rent + utilities + groceries + transport + debtTotal + savings + entertainment + emergency + pet;
    var breathing = netMonthly - essentials;
    var fixedLoad = (rent + debtTotal + utilities + transport) / Math.max(netMonthly, 1);
    var saveRate = savings / Math.max(netMonthly, 1);
    var resilience = Math.max(0, Math.min(100, 100 - (fixedLoad * 62) + (saveRate * 80) + (breathing > 0 ? 10 : -18)));
    var label = scoreLabel(resilience);

    var pin = Math.max(4, Math.min(96, resilience));
    el("sla-pin").style.left = pin + "%";
    el("sla-score-label").textContent = label + " (" + Math.round(resilience) + "/100)";
    el("sla-score-text").textContent = scoreText(label, city.name, breathing, savings);

    var rows = [
      ["Rent", rent, "#679db8"],
      ["Utilities", utilities, "#8cb4c8"],
      ["Groceries", groceries, "#8cbf9a"],
      ["Transportation", transport, "#b0b889"],
      ["Debt", debtTotal, "#d0b27f"],
      ["Savings", savings, "#9ac091"],
      ["Entertainment", entertainment, "#cfa0a0"],
      ["Emergency cushion", emergency + pet, "#c3ced8"]
    ];
    var max = Math.max.apply(null, rows.map(function (r) { return r[1]; }));
    el("sla-breakdown").innerHTML = rows.map(function (r) {
      var w = Math.max(8, Math.round((r[1] / Math.max(max, 1)) * 100));
      return '<div class="sla-bar-row"><span>' + r[0] + '</span><div class="sla-bar"><div class="sla-bar-fill" style="width:' + w + '%;background:' + r[2] + '"></div></div><strong>' + money(r[1]) + "</strong></div>";
    }).join("");
    el("sla-breathing").textContent = breathing >= 0
      ? "After essential expenses and savings, you'd likely have about " + money(breathing) + "/month of flexible money."
      : "Your plan is short by about " + money(Math.abs(breathing)) + "/month. You may feel trapped without changes.";

    var stressors = [];
    if (rent > netMonthly * 0.35) stressors.push("Housing load is high for your income. Try keeping rent near " + money(netMonthly * 0.35) + " or below.");
    if (car > 0) stressors.push("Car payment is reducing housing flexibility. A lower payment can improve your score quickly.");
    if (student > 0) stressors.push("Student loans are a strong monthly drag. Even a partial refinance helps.");
    if (debt > 0 && debt < 150) stressors.push("Your current debt is manageable, but it still lowers breathing room.");
    if (breathing < 450) stressors.push("Breathing room is thin. One surprise bill could push you into stress mode.");
    if (stressors.length === 0) stressors.push("You have good balance. Keep fixed costs stable and maintain savings momentum.");
    el("sla-hard-top").textContent = stressors[0] || "No major pressure point found.";
    el("sla-hard-second").textContent = stressors[1] || "Your second pressure point is moderate. Keep an eye on it as rent or debt changes.";
    el("sla-hard-third").textContent = stressors[2] || "Right now, your third pressure point is recurring lifestyle drift (food delivery, subscriptions, and impulse spending).";
    if (rent > netMonthly * 0.35) {
      el("sla-hard-fix").textContent = "Test a " + money(200) + " to " + money(350) + " rent drop in the scenario sliders first. It usually gives the fastest relief.";
    } else if (debtTotal > 500) {
      el("sla-hard-fix").textContent = "Test a debt payoff scenario first. Removing one payment can unlock stable monthly breathing room.";
    } else {
      el("sla-hard-fix").textContent = "Test a modest salary increase plus small rent cut. This combination usually improves resilience fastest.";
    }

    var rentCut = +el("sla-rent-cut").value || 0;
    var salaryUp = +el("sla-salary-up").value || 0;
    var debtDrop = +el("sla-debt-drop").value || 0;
    var suburb = el("sla-suburb").checked ? 180 : 0;
    var roommate = el("sla-roommate").checked ? 0.55 : 1;

    var simRent = Math.max(500, (rent - rentCut - suburb) * roommate);
    var simIncome = netMonthly + (salaryUp / 12) * 0.72;
    var simDebt = Math.max(0, debtTotal - debtDrop);
    var simTotal = simRent + utilities + groceries + transport + simDebt + savings + entertainment + emergency + pet;
    var simBreathing = simIncome - simTotal;
    var delta = simBreathing - breathing;
    el("sla-rent-cut-value").textContent = "-" + money(rentCut) + "/month rent";
    el("sla-salary-up-value").textContent = "+" + money(salaryUp) + "/year gross";
    el("sla-debt-drop-value").textContent = "-" + money(debtDrop) + "/month debt";
    el("sla-scenario-before").textContent = roomLabel(breathing);
    el("sla-scenario-after").textContent = roomLabel(simBreathing);
    el("sla-scenario-change").textContent = (delta >= 0 ? money(delta) + "/month better" : money(Math.abs(delta)) + "/month worse");
    el("sla-scenario-text").textContent = simBreathing >= 0
      ? "This scenario is workable. Your monthly buffer can support savings plus moderate surprises."
      : "This scenario is still tight. You likely need one more change before solo living feels stable.";
    if (delta >= 0) {
      el("sla-scenario-delta").textContent = "That is an improvement of about " + money(delta) + "/month. At this pace, saving and emergencies should feel less stressful.";
    } else {
      el("sla-scenario-delta").textContent = "This change reduces breathing room by about " + money(Math.abs(delta)) + "/month. Try a bigger rent cut or debt payoff.";
    }

    var monthsCover = Math.max(0, (goal * 6) / Math.max(essentials - savings, 1));
    var layoff = monthsCover >= 4 ? "Likely yes" : "Not yet";
    var medical = breathing >= 400 ? "Likely yes" : "Tight";
    var travel = breathing >= 700 ? "Likely yes" : "Limited";
    var trapped = breathing < 250 || fixedLoad > 0.62 ? "High risk" : breathing < 500 ? "Medium risk" : "Low risk";
    var flex = Math.max(0, Math.min(100, Math.round((breathing / Math.max(netMonthly, 1)) * 200 + 45)));
    function badgeClass(v) {
      if (v === "Likely yes" || v === "Not likely") return "sla-badge sla-badge--good";
      if (v === "Tight" || v === "Limited" || v === "Not yet") return "sla-badge sla-badge--warn";
      return "sla-badge sla-badge--bad";
    }
    var p2p = breathing < 250 ? "Mostly yes" : "Not likely";
    el("sla-stress-test").innerHTML =
      "<li><span><strong>Could you survive a layoff?</strong></span><span class='" + badgeClass(layoff) + "'>" + layoff + "</span></li>" +
      "<li><span><strong>Could you handle a medical bill?</strong></span><span class='" + badgeClass(medical) + "'>" + medical + "</span></li>" +
      "<li><span><strong>Can you still travel?</strong></span><span class='" + badgeClass(travel) + "'>" + travel + "</span></li>" +
      "<li><span><strong>Are you paycheck-to-paycheck?</strong></span><span class='" + badgeClass(p2p) + "'>" + p2p + "</span></li>";
    el("sla-flex-score").textContent = "Financial flexibility score: " + flex + "/100";
    var flexBar = el("sla-flex-bar");
    if (flexBar) flexBar.style.width = flex + "%";
    var headline = el("sla-stress-headline");
    if (headline) {
      headline.textContent = trapped === "High risk"
        ? "High pressure: stabilize before moving"
        : trapped === "Medium risk"
        ? "Mixed readiness: improve one key lever"
        : "Healthy readiness: solo living looks sustainable";
    }
    var trappedEl = el("sla-trapped");
    if (trappedEl) {
      trappedEl.textContent = "Would you feel financially trapped? " + trapped + ".";
      trappedEl.className = "sla-trapped-pill " + (trapped === "Low risk" ? "sla-trapped-pill--good" : trapped === "Medium risk" ? "sla-trapped-pill--warn" : "sla-trapped-pill--bad");
    }

    el("sla-safe-rent").textContent = money(netMonthly * 0.28);
    el("sla-stretch-rent").textContent = money(netMonthly * 0.35);
    el("sla-risky-rent").textContent = money(netMonthly * 0.43);
  }

  function init() {
    var ids = [
      "sla-salary","sla-city","sla-debt","sla-goal","sla-life",
      "sla-student","sla-car","sla-pet","sla-remote",
      "sla-rent-cut","sla-salary-up","sla-debt-drop","sla-suburb","sla-roommate"
    ];
    ids.forEach(function (id) {
      var node = el(id);
      if (!node) return;
      node.addEventListener("input", run);
      node.addEventListener("change", run);
    });
    el("sla-run").addEventListener("click", run);
    var presetButtons = document.querySelectorAll(".sla-preset-btn");
    presetButtons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var p = btn.getAttribute("data-preset");
        if (p === "rent") {
          el("sla-rent-cut").value = 300; el("sla-salary-up").value = 0; el("sla-debt-drop").value = 0; el("sla-suburb").checked = false; el("sla-roommate").checked = false;
        } else if (p === "salary") {
          el("sla-rent-cut").value = 0; el("sla-salary-up").value = 12000; el("sla-debt-drop").value = 0; el("sla-suburb").checked = false; el("sla-roommate").checked = false;
        } else if (p === "debt") {
          el("sla-rent-cut").value = 0; el("sla-salary-up").value = 0; el("sla-debt-drop").value = 300; el("sla-suburb").checked = false; el("sla-roommate").checked = false;
        } else if (p === "hybrid") {
          el("sla-rent-cut").value = 200; el("sla-salary-up").value = 0; el("sla-debt-drop").value = 100; el("sla-suburb").checked = true; el("sla-roommate").checked = false; el("sla-remote").checked = true;
        } else {
          el("sla-rent-cut").value = 150; el("sla-salary-up").value = 5000; el("sla-debt-drop").value = 100; el("sla-suburb").checked = false; el("sla-roommate").checked = false; el("sla-remote").checked = false;
        }
        run();
      });
    });
    run();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
