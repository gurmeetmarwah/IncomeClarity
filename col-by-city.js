/**
 * Cost of living hub — search, compare, filters, breakdown chart.
 */
(function () {
  const US = { rent: 1500, groceries: 400, utilities: 200, transport: 350, healthcare: 420, taxes: 180 };

  const catalogEl = document.getElementById('col-catalog');
  if (!catalogEl) return;

  let catalog = [];
  try {
    catalog = JSON.parse(catalogEl.textContent);
  } catch (e) {
    return;
  }

  const searchInput = document.getElementById('col-search-input');
  const searchBtn = document.getElementById('col-search-go');
  const searchHelp = document.getElementById('col-search-help');
  const searchList = document.getElementById('col-search-list');
  const compareA = document.getElementById('col-compare-a');
  const compareB = document.getElementById('col-compare-b');
  const compareBtn = document.getElementById('col-compare-go');
  const cityGrid = document.getElementById('col-city-grid');
  const breakdownCity = document.getElementById('col-breakdown-city');
  const breakdownBars = document.getElementById('col-breakdown-bars');
  const filterChips = document.querySelectorAll('[data-col-filter]');
  const sortSelect = document.getElementById('col-sort');
  const showMoreBtn = document.getElementById('col-show-more');
  const INITIAL_CITY_LIMIT = 6;

  const COMPARE_MAP = {
    'nyc-vs-chicago': '/living/housing/cost-of-living-by-city/compare/nyc-vs-chicago',
    'austin-vs-denver': '/living/housing/cost-of-living-by-city/compare/austin-vs-denver',
    'dallas-vs-atlanta': '/living/housing/cost-of-living-by-city/compare/dallas-vs-atlanta',
    'seattle-vs-phoenix': '/living/housing/cost-of-living-by-city/compare/seattle-vs-phoenix',
  };

  const stateEntries = (() => {
    const bySlug = new Map();
    catalog.forEach((c) => {
      const m = c.path.match(/\/cost-of-living-by-city\/([^/]+)\/[^/]+$/);
      if (!m) return;
      const slug = m[1];
      if (!['california', 'texas', 'florida', 'new-york'].includes(slug)) return;
      if (!bySlug.has(slug)) {
        const name = slug === 'new-york'
          ? 'New York'
          : slug.charAt(0).toUpperCase() + slug.slice(1);
        bySlug.set(slug, {
          id: slug,
          name,
          label: name,
          path: `/living/housing/cost-of-living-by-city/${slug}`,
          isState: true,
        });
      }
    });
    return [...bySlug.values()];
  })();

  function fillDatalistEl(el) {
    if (!el || el.tagName !== 'DATALIST') return;
    const allLabels = [...stateEntries, ...catalog].map((c) => c.label);
    el.innerHTML = allLabels.map((label) => `<option value="${label}"></option>`).join('');
  }

  fillDatalistEl(searchList);
  if (compareA && compareA.list) fillDatalistEl(document.getElementById(compareA.getAttribute('list')));
  if (compareB && compareB.list) fillDatalistEl(document.getElementById(compareB.getAttribute('list')));
  if (breakdownCity) {
    breakdownCity.innerHTML =
      '<option value="">Choose a city…</option>' +
      catalog.map((c) => `<option value="${c.id}">${c.label}</option>`).join('');
  }

  function normalize(text) {
    return (text || '').trim().toLowerCase().replace(/[^a-z0-9]+/g, ' ');
  }

  function findByLabel(label) {
    const q = (label || '').trim().toLowerCase();
    return catalog.find((c) => c.label.toLowerCase() === q || c.name.toLowerCase() === q || c.id === q)
      || stateEntries.find((s) => s.label.toLowerCase() === q || s.id === q);
  }

  function findBestMatch(query) {
    const q = normalize(query);
    if (!q) return null;
    const exact = findByLabel(query);
    if (exact) return exact;

    const haystack = [...stateEntries, ...catalog];
    const startsWith = haystack.find((c) => normalize(c.label).startsWith(q) || normalize(c.name).startsWith(q));
    if (startsWith) return startsWith;
    return haystack.find((c) => normalize(c.label).includes(q) || normalize(c.name).includes(q)) || null;
  }

  function goToCity(c) {
    if (c && c.path) window.location.href = c.path;
  }

  function runSearch() {
    if (!searchInput) return;
    const c = findBestMatch(searchInput.value);
    if (!c) {
      if (searchHelp) searchHelp.textContent = 'No match found. Try a city like Austin or a state like Texas.';
      return;
    }
    if (searchHelp) searchHelp.textContent = `Opening ${c.label}...`;
    goToCity(c);
  }

  if (searchInput) {
    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        runSearch();
      }
    });
  }
  if (searchBtn) searchBtn.addEventListener('click', runSearch);

  const comparePreset = document.getElementById('col-compare-preset');
  if (comparePreset) {
    comparePreset.addEventListener('change', () => {
      const url = COMPARE_MAP[comparePreset.value];
      if (url) window.location.href = url;
    });
  }

  if (compareBtn) {
    compareBtn.addEventListener('click', () => {
      const a = findByLabel(compareA && compareA.value);
      const b = findByLabel(compareB && compareB.value);
      if (!a || !b) return;
      const key = [a.compareKey, b.compareKey].sort().join('-');
      const known =
        COMPARE_MAP[`${a.compareKey}-vs-${b.compareKey}`] ||
        COMPARE_MAP[`${b.compareKey}-vs-${a.compareKey}`];
      if (known) {
        window.location.href = known;
        return;
      }
      window.location.href = a.path + '?compare=' + encodeURIComponent(b.id);
    });
  }

  function pctDiff(val, base) {
    return Math.round(((val - base) / base) * 100);
  }

  function renderBreakdown(cityId) {
    if (!breakdownBars) return;
    const c = catalog.find((x) => x.id === cityId);
    if (!c) {
      breakdownBars.innerHTML = '<p class="col-breakdown-empty">Select a city to see how costs stack up vs the U.S. average.</p>';
      return;
    }
    const cats = [
      { key: 'housing', label: 'Housing', us: US.rent },
      { key: 'transport', label: 'Transportation', us: US.transport },
      { key: 'groceries', label: 'Groceries', us: US.groceries },
      { key: 'utilities', label: 'Utilities', us: US.utilities },
      { key: 'healthcare', label: 'Healthcare', us: US.healthcare },
      { key: 'taxes', label: 'Taxes (est.)', us: US.taxes },
    ];
    breakdownBars.innerHTML = cats
      .map((cat) => {
        const val = c[cat.key] || 0;
        const pct = pctDiff(val, cat.us);
        const max = Math.max(val, cat.us) * 1.15;
        const wCity = Math.round((val / max) * 100);
        const wUs = Math.round((cat.us / max) * 100);
        const sign = pct >= 0 ? '+' : '';
        return `
          <div class="col-bar-row">
            <span class="col-bar-row__label">${cat.label}</span>
            <div class="col-bar-track" aria-hidden="true">
              <span class="col-bar col-bar--us" style="width:${wUs}%"></span>
              <span class="col-bar col-bar--city" style="width:${wCity}%"></span>
            </div>
            <span class="col-bar-row__val">${sign}${pct}% vs US</span>
          </div>`;
      })
      .join('');
  }

  if (breakdownCity) {
    breakdownCity.addEventListener('change', () => renderBreakdown(breakdownCity.value));
    if (catalog[0]) {
      breakdownCity.value = catalog[0].id;
      renderBreakdown(catalog[0].id);
    }
  }

  function applyFilters() {
    if (!cityGrid) return;
    const active = document.querySelector('[data-col-filter].is-active');
    const filter = active ? active.getAttribute('data-col-filter') : 'all';
    const cards = [...cityGrid.querySelectorAll('.col-explore-card')];
    let visibleCount = 0;
    cards.forEach((card) => {
      const tags = (card.getAttribute('data-tags') || '').split(',');
      const show = filter === 'all' || tags.includes(filter);
      card.dataset.match = show ? '1' : '0';
      if (!show) {
        card.hidden = true;
        return;
      }
      const expanded = showMoreBtn && showMoreBtn.getAttribute('aria-expanded') === 'true';
      visibleCount += 1;
      card.hidden = !expanded && visibleCount > INITIAL_CITY_LIMIT;
    });
    if (showMoreBtn) {
      const totalMatches = cards.filter((c) => c.dataset.match === '1').length;
      const expanded = showMoreBtn.getAttribute('aria-expanded') === 'true';
      showMoreBtn.hidden = totalMatches <= INITIAL_CITY_LIMIT;
      showMoreBtn.textContent = expanded ? 'Show fewer cities' : `Show more cities (${Math.max(0, totalMatches - INITIAL_CITY_LIMIT)})`;
    }
  }

  filterChips.forEach((chip) => {
    chip.addEventListener('click', () => {
      filterChips.forEach((c) => c.classList.remove('is-active'));
      chip.classList.add('is-active');
      applyFilters();
    });
  });

  function sortCards() {
    if (!cityGrid || !sortSelect) return;
    const cards = [...cityGrid.querySelectorAll('.col-explore-card')];
    const mode = sortSelect.value;
    cards.sort((a, b) => {
      const av = parseFloat(a.getAttribute(`data-${mode}`) || '0');
      const bv = parseFloat(b.getAttribute(`data-${mode}`) || '0');
      return mode === 'rent' ? av - bv : bv - av;
    });
    cards.forEach((c) => cityGrid.appendChild(c));
    applyFilters();
  }

  if (sortSelect) sortSelect.addEventListener('change', sortCards);
  if (showMoreBtn) {
    showMoreBtn.addEventListener('click', () => {
      const expanded = showMoreBtn.getAttribute('aria-expanded') === 'true';
      showMoreBtn.setAttribute('aria-expanded', expanded ? 'false' : 'true');
      applyFilters();
    });
  }

  applyFilters();
})();
