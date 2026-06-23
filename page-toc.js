/**
 * Sitewide table of contents — hero placement next to calculators when possible,
 * auto-built from page headings otherwise. Scroll-spy and mobile collapse included.
 */
(function () {
  'use strict';

  var MIN_SECTIONS = 3;
  var COMPACT_MQ = window.matchMedia('(max-width: 899px)');
  var CALC_SELECTORS = [
    '.ha-calc-shell',
    '.ra-calc-shell',
    '.mc-calc-shell',
    '.cs-calc-shell',
    '.ss-calc-shell',
    '.income-calc-shell',
    '.rvb-calc-shell',
    '.fl-calc-shell',
    '[class*="calc-shell"]'
  ].join(', ');

  var HERO_HUB_SELECTORS = '.debt-hub-hero';

  function slugify(text) {
    return text
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '')
      .slice(0, 48);
  }

  function isSkippedPage() {
    if (document.body.hasAttribute('data-no-toc')) return true;
    var path = window.location.pathname;
    if (path === '/' || path === '/index.html') return true;
    if (/\/(privacy-policy|terms|contact)(\/|\.html|$)/.test(path)) return true;
    if (!document.querySelector('main')) return true;
    return false;
  }

  function collectFromHeadings(main) {
    var used = {};
    var items = [];
    var headings = main.querySelectorAll('h2');

    for (var i = 0; i < headings.length; i++) {
      var h = headings[i];
      if (h.closest('.site-footer, .faq-item, .ha-city-toc, .take-home-guide-toc, .methodology-toc, .eeat-trust, .page-toc')) {
        continue;
      }
      var label = (h.textContent || '').trim();
      if (!label || /^on this page$/i.test(label)) continue;

      var id = h.id;
      if (!id) {
        var base = slugify(label) || 'section';
        var n = 1;
        id = base;
        while (used[id] || document.getElementById(id)) {
          id = base + '-' + n;
          n += 1;
        }
        h.id = id;
      }
      used[id] = true;
      var el = h.closest('section') || h;
      items.push({ id: id, label: label, el: el });
    }
    return items;
  }

  function collectFromLinks(nav) {
    var items = [];
    nav.querySelectorAll('a[href^="#"]').forEach(function (a) {
      var id = a.getAttribute('href').slice(1);
      if (!id) return;
      var label = (a.textContent || '').trim().replace(/\s*\(guide\)\s*$/i, '');
      if (!label) return;
      var target = document.getElementById(id);
      items.push({
        id: id,
        label: label,
        el: target ? (target.closest('section') || target) : null
      });
    });
    return items;
  }

  function buildTocMarkup(items, kicker) {
    var list = items
      .map(function (item) {
        return (
          '<li><a href="#' +
          item.id +
          '" class="ha-city-toc__link" data-ha-toc-link>' +
          item.label +
          '</a></li>'
        );
      })
      .join('');

    var aside = document.createElement('aside');
    aside.className = 'ha-city-toc ha-city-toc--hero page-toc';
    aside.id = 'page-toc';
    aside.innerHTML =
      '<div class="ha-city-toc__card">' +
      '<button type="button" class="ha-city-toc__toggle" aria-expanded="true" aria-controls="page-toc-panel">' +
      '<span class="ha-city-toc__toggle-text">' +
      '<span class="ha-city-toc__title">On this page</span>' +
      '<span class="ha-city-toc__kicker">' +
      (kicker || 'Guides, breakdowns, FAQs &amp; more') +
      '</span>' +
      '</span>' +
      '<svg class="ha-city-toc__toggle-icon" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">' +
      '<path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 111.06 1.06l-4.24 4.25a.75.75 0 01-1.06 0L5.21 8.29a.75.75 0 01.02-1.08z" clip-rule="evenodd"/>' +
      '</svg>' +
      '</button>' +
      '<nav class="ha-city-toc__panel" id="page-toc-panel" aria-label="On this page">' +
      '<ul class="ha-city-toc__list">' +
      list +
      '</ul>' +
      '</nav>' +
      '</div>';
    return aside;
  }

  function initToggle(toc) {
    var toggle = toc.querySelector('.ha-city-toc__toggle');
    var panel = toc.querySelector('.ha-city-toc__panel');
    if (!toggle || !panel) return;

    function setOpen(open) {
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      panel.hidden = !open;
      toc.classList.toggle('ha-city-toc--open', open);
    }

    setOpen(true);
    COMPACT_MQ.addEventListener('change', function (e) {
      if (!e.matches) setOpen(true);
    });
    toggle.addEventListener('click', function () {
      if (!COMPACT_MQ.matches) return;
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
  }

  function initScrollSpy(toc, items, topId) {
    var links = toc.querySelectorAll('[data-ha-toc-link]');

    function setActive(id) {
      links.forEach(function (a) {
        a.classList.toggle('is-active', a.getAttribute('href') === '#' + id);
      });
    }

    function scrollTarget(link) {
      var id = link.getAttribute('href').slice(1);
      var target = document.getElementById(id);
      if (!target) return null;
      return target.closest('section') || target;
    }

    var observed = [];
    items.forEach(function (item) {
      var el = item.el || scrollTarget(links[observed.length]);
      if (el) observed.push({ id: item.id, el: el });
    });

    if (observed.length && 'IntersectionObserver' in window) {
      var visible = new Map();
      var observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            var match = observed.find(function (o) {
              return o.el === entry.target;
            });
            if (!match) return;
            if (entry.isIntersecting) visible.set(match.id, entry.intersectionRatio);
            else visible.delete(match.id);
          });
          if (visible.size) {
            var bestId = null;
            var bestRatio = -1;
            visible.forEach(function (ratio, id) {
              if (ratio > bestRatio) {
                bestRatio = ratio;
                bestId = id;
              }
            });
            if (bestId) setActive(bestId);
          } else if (window.scrollY < 120 && topId) {
            setActive(topId);
          }
        },
        { rootMargin: '-72px 0px -55% 0px', threshold: [0, 0.1, 0.25, 0.5] }
      );
      observed.forEach(function (o) {
        observer.observe(o.el);
      });
      if (topId) setActive(topId);
    }

    links.forEach(function (link) {
      link.addEventListener('click', function (e) {
        var target = scrollTarget(link);
        if (!target) return;
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        var id = link.getAttribute('href').slice(1);
        history.replaceState(null, '', '#' + id);
        setActive(id);
      });
    });
  }

  function findCalcShell(main) {
    var el = main.querySelector(CALC_SELECTORS);
    if (!el) return null;
    if (el.matches('form')) {
      return el.closest('[class*="calc-shell"], .income-calc-shell, .rvb-calc-shell, .fl-calc-shell') || el.parentElement;
    }
    return el;
  }

  function findMountAnchor(main) {
    var calc = findCalcShell(main);
    if (calc) return calc;
    return main.querySelector(HERO_HUB_SELECTORS);
  }

  function mountBesideCalc(calcShell, toc) {
    var grid = calcShell.closest('.ha-hero-grid');
    if (!grid) {
      grid = document.createElement('div');
      grid.className = 'ha-hero-grid';
      calcShell.parentNode.insertBefore(grid, calcShell);
      grid.appendChild(calcShell);
    }
    if (!grid.querySelector('.ha-city-toc, .page-toc')) {
      grid.appendChild(toc);
    }
    var hero = calcShell.closest('section, .col-hero-inner, .ss-hero, .cs-hero');
    if (hero && hero.classList) {
      hero.classList.add('ha-hero', 'page-toc-hero');
    }
    var container = calcShell.closest('.container');
    if (container && container.classList) {
      container.classList.add('page-toc-hero-container');
    }
  }

  function mountAfterHeroContent(toc, main) {
    var anchors = [
      main.querySelector('.ss-quick-answer'),
      main.querySelector('.col-stat-row'),
      main.querySelector('.take-home-guide-at-a-glance'),
      main.querySelector('.take-home-guide-header'),
      main.querySelector('article > header'),
      main.querySelector('.col-hero-inner .container'),
      main.querySelector('section .container'),
      main.querySelector('section')
    ];

    for (var i = 0; i < anchors.length; i++) {
      var anchor = anchors[i];
      if (!anchor) continue;
      var wrap = document.createElement('div');
      wrap.className = 'page-toc-band';
      wrap.appendChild(toc);
      if (anchor.classList && anchor.classList.contains('container')) {
        anchor.appendChild(wrap);
      } else if (anchor.parentNode) {
        anchor.parentNode.insertBefore(wrap, anchor.nextSibling);
      } else {
        main.insertBefore(wrap, main.firstChild);
      }
      return;
    }
    main.insertBefore(toc, main.firstChild);
  }

  function run() {
    if (isSkippedPage()) return;

    var main = document.querySelector('main');
    var existing = document.querySelector('.ha-city-toc');
    var legacy = document.querySelector('.take-home-guide-toc, .methodology-toc');
    var items;
    var topId = null;

    if (existing) {
      items = collectFromLinks(existing);
      if (!items.length) items = collectFromHeadings(main);
      initToggle(existing);
      initScrollSpy(existing, items, document.getElementById('ha-calculator') ? 'ha-calculator' : items[0] && items[0].id);
      document.body.classList.add('page-toc-active');
      return;
    }

    if (legacy) {
      items = collectFromLinks(legacy);
      if (items.length < MIN_SECTIONS) return;
      var tocFromLegacy = buildTocMarkup(items, 'Jump to any section on this page');
      legacy.replaceWith(tocFromLegacy);
      var anchor = findMountAnchor(main);
      if (anchor) mountBesideCalc(anchor, tocFromLegacy);
      else mountAfterHeroContent(tocFromLegacy, main);
      initToggle(tocFromLegacy);
      initScrollSpy(tocFromLegacy, items, items[0] && items[0].id);
      document.body.classList.add('page-toc-active');
      return;
    }

    items = collectFromHeadings(main);
    if (items.length < MIN_SECTIONS) return;

    var kicker = 'Jump to any section on this page';
    if (main.querySelector(CALC_SELECTORS)) {
      kicker = 'Guides, breakdowns, tools &amp; more';
    }

    var toc = buildTocMarkup(items, kicker);
    var mountAnchor = findMountAnchor(main);
    if (mountAnchor) {
      mountBesideCalc(mountAnchor, toc);
      topId = document.getElementById('ha-calculator') ? 'ha-calculator' : items[0].id;
    } else {
      mountAfterHeroContent(toc, main);
      topId = items[0].id;
    }

    initToggle(toc);
    initScrollSpy(toc, items, topId);
    document.body.classList.add('page-toc-active');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
})();
