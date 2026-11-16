(function () {
  'use strict';
  var menuButton = document.querySelector('[data-menu-toggle]');
  var menu = document.getElementById('site-menu');
  function setMenu(open) {
    if (!menuButton || !menu) return;
    menu.classList.toggle('is-open', open);
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
  }
  if (menuButton && menu) {
    menuButton.addEventListener('click', function () {
      setMenu(menuButton.getAttribute('aria-expanded') !== 'true');
    });
    menu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () { setMenu(false); });
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
        setMenu(false);
        menuButton.focus();
      }
    });
    if (window.matchMedia) {
      var desktop = window.matchMedia('(min-width: 801px)');
      if (desktop.addEventListener) desktop.addEventListener('change', function () { setMenu(false); });
    }
  }

  var products = Array.from(document.querySelectorAll('[data-product]'));
  if (!products.length) return;
  var filters = Array.from(document.querySelectorAll('[data-filter]'));
  var count = document.querySelector('[data-count]');
  function selectFilter(value) {
    filters.forEach(function (button) {
      button.setAttribute('aria-pressed', String(button.dataset.filter === value));
    });
    products.forEach(function (card) {
      card.hidden = value !== 'todos' && card.dataset.category !== value;
    });
    if (count) count.textContent = String(products.filter(function (card) { return !card.hidden; }).length);
  }
  filters.forEach(function (button) {
    button.addEventListener('click', function () { selectFilter(button.dataset.filter); });
  });

  var dialog = document.getElementById('product-dialog');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  var image = document.getElementById('dialog-image');
  var title = document.getElementById('dialog-title');
  var description = document.getElementById('dialog-description');
  var material = document.getElementById('dialog-material');
  var quote = document.getElementById('dialog-quote');
  var position = document.getElementById('dialog-position');
  var closeButton = document.querySelector('[data-close-dialog]');
  var currentCard = null;
  var lastTrigger = null;
  function visibleProducts() {
    return products.filter(function (card) { return !card.hidden; });
  }
  function showProduct(card, trigger) {
    if (!card) return;
    if (card.hidden) selectFilter('todos');
    currentCard = card;
    image.src = card.dataset.image;
    image.alt = card.dataset.title + ' — visualização ilustrativa';
    title.textContent = card.dataset.title;
    description.textContent = card.dataset.details;
    material.textContent = card.dataset.material;
    quote.href = card.querySelector('[data-quote]').href;
    var visible = visibleProducts();
    position.textContent = String(visible.indexOf(card) + 1) + ' de ' + String(visible.length);
    if (!dialog.open) {
      lastTrigger = trigger || card.querySelector('[data-open-product]');
      dialog.showModal();
      closeButton.focus();
    }
  }
  function moveProduct(step) {
    var visible = visibleProducts();
    if (!visible.length) return;
    var next = (visible.indexOf(currentCard) + step + visible.length) % visible.length;
    showProduct(visible[next]);
  }
  document.querySelectorAll('[data-open-product]').forEach(function (link) {
    link.addEventListener('click', function (event) {
      var card = products.find(function (item) { return item.id === link.dataset.openProduct; });
      if (!card) return;
      event.preventDefault();
      showProduct(card, link);
    });
  });
  closeButton.addEventListener('click', function () { dialog.close(); });
  dialog.addEventListener('close', function () {
    if (lastTrigger && typeof lastTrigger.focus === 'function') lastTrigger.focus();
    lastTrigger = null;
  });
  dialog.addEventListener('click', function (event) {
    if (event.target !== dialog) return;
    var rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right ||
        event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
  dialog.addEventListener('keydown', function (event) {
    if (event.key === 'ArrowLeft') { event.preventDefault(); moveProduct(-1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); moveProduct(1); }
  });
  document.querySelector('[data-prev-product]').addEventListener('click', function () { moveProduct(-1); });
  document.querySelector('[data-next-product]').addEventListener('click', function () { moveProduct(1); });
  function openFromHash() {
    var id;
    try { id = decodeURIComponent(window.location.hash.slice(1)); } catch (error) { return; }
    var card = products.find(function (item) { return item.id === id; });
    if (card) showProduct(card);
  }
  window.addEventListener('hashchange', openFromHash);
  openFromHash();
}());
