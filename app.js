(function () {
  'use strict';
  const products = window.CinareProducts || [];
  const projects = window.CinareProjects || [];
  const catalog = new Map(products.map(p => [p.id, p]));
  const allModels = new Map([...products, ...projects].map(p => [p.id, p]));
  const root = new URL(document.body.dataset.root || './', window.location.href);
  const local = path => new URL(path, root).href;
  const wa = message => 'https://wa.me/351913591464?text=' + encodeURIComponent(message);
  const esc = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const paths = {
    heart: '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8Z"/>',
    share: '<path d="M12 15V3m-4 4 4-4 4 4M5 12v8h14v-8"/>',
    arrow: '<path d="M5 19 19 5M5 5h14v14"/>',
    right: '<path d="M4 12h16m-6-6 6 6-6 6"/>'
  };
  const svg = name => '<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + paths[name] + '</svg>';
  const announcement = document.querySelector('[data-announcement]');
  let announcementTimer;
  function announce(message) {
    if (!announcement) return;
    announcement.textContent = message; announcement.classList.add('is-visible');
    window.clearTimeout(announcementTimer);
    announcementTimer = window.setTimeout(() => announcement.classList.remove('is-visible'), 4500);
  }
  const menuButton = document.querySelector('[data-menu-toggle]');
  const menu = document.getElementById('site-menu');
  function setMenu(open) {
    if (!menu || !menuButton) return;
    menu.classList.toggle('is-open', open);
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
  }
  if (menuButton && menu) {
    menuButton.addEventListener('click', () => setMenu(menuButton.getAttribute('aria-expanded') !== 'true'));
    menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') { setMenu(false); menuButton.focus(); } });
    const desktop = window.matchMedia('(min-width: 1041px)');
    if (desktop.addEventListener) desktop.addEventListener('change', () => setMenu(false));
  }
  // Keep links shared before individual product pages existed working.
  if (document.body.dataset.page === 'catalog' && window.location.hash) {
    let id = '';
    try { id = decodeURIComponent(window.location.hash.slice(1)); } catch (e) { /* Ignore invalid fragments. */ }
    if (catalog.has(id)) { window.location.replace(local('modelos/' + id + '.html')); return; }
  }
  document.querySelectorAll('[data-js]').forEach(el => { el.hidden = false; });
  const storageKey = 'cinare:favoritos:v1';
  function readFavorites() {
    try {
      const value = JSON.parse(window.localStorage.getItem(storageKey) || '[]');
      return new Set(Array.isArray(value) ? value.filter(id => catalog.has(id)) : []);
    } catch (e) { return new Set(); }
  }
  let favorites = readFavorites();
  const favoritesGrid = document.querySelector('[data-favorites-grid]');
  function cardMarkup(p) {
    const v = p.image.variants.find(v => v.width >= 640) || p.image.variants.at(-1);
    const srcset = p.image.variants.map(v => local(v.path) + ' ' + v.width + 'w').join(', ');
    const href = local('modelos/' + p.id + '.html');
    return '<article class="product-card" data-product="' + p.id + '"><div class="product-media"><a class="product-photo" href="' + href + '" aria-label="Ver ' + esc(p.name) + '"><img src="' + local(v.path) + '" srcset="' + srcset + '" sizes="(max-width:560px) calc(100vw - 36px), (max-width:800px) 46vw, 380px" width="' + p.image.width + '" height="' + p.image.height + '" alt="' + esc(p.name) + ' — visualização ilustrativa" loading="lazy" decoding="async"></a><div class="product-tools"><button class="icon-button favorite-toggle" type="button" data-favorite="' + p.id + '" aria-pressed="true" aria-label="Remover ' + esc(p.name) + ' dos favoritos">' + svg('heart') + '</button><button class="icon-button" type="button" data-share="' + p.id + '" aria-label="Partilhar ' + esc(p.name) + '">' + svg('share') + '</button></div></div><div class="product-copy"><span class="product-category">' + esc(p.categoryLabel) + '</span><h3><a href="' + href + '">' + esc(p.name) + '</a></h3><p class="product-description">' + esc(p.description) + '</p><p class="product-material">' + esc(p.material) + ' · Por medida</p><div class="product-actions"><a class="btn btn-dark" href="' + local('orcamento.html?modelo=' + p.id) + '">Pedir orçamento ' + svg('arrow') + '</a><a class="text-link" href="' + href + '">Ver peça ' + svg('right') + '</a></div></div></article>';
  }
  function updateFavorites() {
    document.querySelectorAll('[data-favorite-count]').forEach(el => { el.textContent = String(favorites.size); el.hidden = !favorites.size; });
    document.querySelectorAll('.favorites-nav').forEach(el => el.setAttribute('aria-label', 'Favoritos: ' + favorites.size));
    if (favoritesGrid) {
      favoritesGrid.innerHTML = [...favorites].filter(id => catalog.has(id)).map(id => cardMarkup(catalog.get(id))).join('');
      document.querySelector('[data-favorites-empty]').hidden = favorites.size > 0;
      document.querySelector('[data-favorites-count]').textContent = favorites.size ? favorites.size + (favorites.size === 1 ? ' peça guardada' : ' peças guardadas') : '';
    }
    document.querySelectorAll('[data-favorite]').forEach(button => {
      const p = catalog.get(button.dataset.favorite);
      if (!p) return;
      const saved = favorites.has(p.id);
      button.hidden = false; button.setAttribute('aria-pressed', String(saved));
      button.setAttribute('aria-label', (saved ? 'Remover ' : 'Guardar ') + p.name + (saved ? ' dos favoritos' : ' nos favoritos'));
      const label = button.querySelector('[data-favorite-label]');
      if (label) label.textContent = saved ? 'Guardado nos favoritos' : 'Guardar favorito';
    });
    document.querySelectorAll('[data-share]').forEach(el => { el.hidden = false; });
  }
  updateFavorites();
  window.addEventListener('storage', e => { if (e.key === storageKey || e.key === null) { favorites = readFavorites(); updateFavorites(); } });
  const filters = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('#catalog-grid [data-product]')];
  filters.forEach(button => button.addEventListener('click', () => {
    filters.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    cards.forEach(card => { card.hidden = button.dataset.filter !== 'todos' && card.dataset.category !== button.dataset.filter; });
    const count = cards.filter(c => !c.hidden).length;
    const output = document.querySelector('[data-count]'), label = document.querySelector('[data-count-label]');
    if (output) output.textContent = String(count);
    if (label) label.textContent = count === 1 ? 'modelo' : 'modelos';
  }));
  function openDialog(dialog) { if (!dialog.open) { if (typeof dialog.showModal === 'function') dialog.showModal(); else dialog.setAttribute('open', ''); } }
  function closeDialog(dialog) { if (typeof dialog.close === 'function') dialog.close(); else dialog.removeAttribute('open'); }
  const shareDialog = document.getElementById('share-dialog');
  const zoomDialog = document.getElementById('zoom-dialog');
  [shareDialog, zoomDialog].filter(Boolean).forEach(dialog => dialog.addEventListener('click', e => {
    if (e.target !== dialog) return;
    const r = dialog.getBoundingClientRect();
    if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) closeDialog(dialog);
  }));
  let shareTrigger = null, shareData = null;
  function shareProduct(p, trigger) {
    if (!shareDialog) return;
    shareData = {title: p.name + ' — CINARÉ', text: p.description, url: p.url}; shareTrigger = trigger;
    document.getElementById('share-title').textContent = 'Partilhar ' + p.name.toLowerCase();
    document.getElementById('share-url').value = p.url;
    document.getElementById('share-whatsapp').href = 'https://wa.me/?text=' + encodeURIComponent(shareData.title + '\n' + p.url);
    document.querySelector('[data-share-status]').textContent = '';
    document.querySelector('[data-native-share]').hidden = typeof navigator.share !== 'function';
    openDialog(shareDialog);
  }
  if (shareDialog) {
    document.querySelector('[data-close-share]').addEventListener('click', () => closeDialog(shareDialog));
    shareDialog.addEventListener('close', () => { if (shareTrigger?.isConnected) shareTrigger.focus(); });
    document.querySelector('[data-copy-share]').addEventListener('click', async () => {
      const input = document.getElementById('share-url'), status = document.querySelector('[data-share-status]');
      let copied = false;
      try { if (navigator.clipboard?.writeText) { await navigator.clipboard.writeText(input.value); copied = true; } } catch (e) { /* Keep the local copy fallback. */ }
      if (!copied) { input.focus(); input.select(); try { copied = document.execCommand('copy'); } catch (e) { /* Leave the URL selected. */ } }
      status.textContent = copied ? 'Ligação copiada. Já a podes enviar a quem quiseres.' : 'A ligação está selecionada. Usa a opção Copiar do teu dispositivo.';
    });
    document.querySelector('[data-native-share]').addEventListener('click', async () => {
      if (!shareData || typeof navigator.share !== 'function') return;
      try { await navigator.share(shareData); closeDialog(shareDialog); } catch (e) { if (e.name !== 'AbortError') document.querySelector('[data-share-status]').textContent = 'Podes copiar a ligação ou partilhar pelo WhatsApp.'; }
    });
  }
  const zoomImage = document.getElementById('zoom-image'), stage = document.querySelector('[data-zoom-stage]');
  let zoomTrigger = null, scale = 1, offset = {x: 0, y: 0}, pinch = null;
  const pointers = new Map(), clamp = (n, low, high) => Math.min(high, Math.max(low, n));
  function drawZoom() {
    if (!stage || !zoomImage) return;
    offset.x = clamp(offset.x, -stage.clientWidth * (scale - 1) / 2, stage.clientWidth * (scale - 1) / 2);
    offset.y = clamp(offset.y, -stage.clientHeight * (scale - 1) / 2, stage.clientHeight * (scale - 1) / 2);
    zoomImage.style.transform = 'translate(' + offset.x + 'px,' + offset.y + 'px) scale(' + scale + ')';
    stage.classList.toggle('is-zoomed', scale > 1);
    document.querySelector('[data-zoom-level]').textContent = Math.round(scale * 100) + '%';
    document.querySelector('[data-zoom-out]').disabled = scale <= 1;
    document.querySelector('[data-zoom-in]').disabled = scale >= 4;
  }
  function zoomTo(value, clientX, clientY) {
    const next = clamp(value, 1, 4);
    if (Number.isFinite(clientX) && Number.isFinite(clientY)) {
      const r = stage.getBoundingClientRect(), x = clientX - r.left - r.width / 2, y = clientY - r.top - r.height / 2;
      offset.x = (offset.x - x) * next / scale + x; offset.y = (offset.y - y) * next / scale + y;
    }
    scale = next; drawZoom();
  }
  function openZoom(p, trigger) {
    if (!zoomDialog || !p.image) return;
    zoomTrigger = trigger; scale = 1; offset = {x: 0, y: 0}; pointers.clear(); pinch = null;
    document.getElementById('zoom-title').textContent = p.name;
    const loading = document.querySelector('[data-zoom-loading]');
    loading.hidden = false; loading.textContent = 'A carregar imagem…';
    zoomImage.onload = () => { loading.hidden = true; drawZoom(); };
    zoomImage.onerror = () => { loading.textContent = 'Não foi possível carregar a imagem. Podes abrir o original pela ligação abaixo.'; };
    zoomImage.alt = p.name + ' — visualização ilustrativa'; zoomImage.src = local(p.image.source);
    document.getElementById('zoom-original').href = local(p.image.source);
    openDialog(zoomDialog); drawZoom(); document.querySelector('[data-close-zoom]').focus();
  }
  if (zoomDialog && stage) {
    document.querySelector('[data-close-zoom]').addEventListener('click', () => closeDialog(zoomDialog));
    document.querySelector('[data-zoom-in]').addEventListener('click', () => zoomTo(scale + .5));
    document.querySelector('[data-zoom-out]').addEventListener('click', () => zoomTo(scale - .5));
    document.querySelector('[data-zoom-reset]').addEventListener('click', () => { offset = {x: 0, y: 0}; zoomTo(1); });
    zoomDialog.addEventListener('close', () => { pointers.clear(); if (zoomTrigger?.isConnected) zoomTrigger.focus(); });
    stage.addEventListener('wheel', e => { e.preventDefault(); zoomTo(scale * (e.deltaY < 0 ? 1.12 : 1 / 1.12), e.clientX, e.clientY); }, {passive: false});
    stage.addEventListener('pointerdown', e => {
      if (e.pointerType === 'mouse' && e.button !== 0) return;
      pointers.set(e.pointerId, {x: e.clientX, y: e.clientY}); stage.setPointerCapture(e.pointerId);
      if (pointers.size === 2) { const [a, b] = [...pointers.values()]; pinch = {distance: Math.hypot(a.x - b.x, a.y - b.y), x: (a.x + b.x) / 2, y: (a.y + b.y) / 2}; }
    });
    stage.addEventListener('pointermove', e => {
      const previous = pointers.get(e.pointerId);
      if (!previous) return;
      pointers.set(e.pointerId, {x: e.clientX, y: e.clientY});
      if (pointers.size >= 2) {
        const [a, b] = [...pointers.values()], current = {distance: Math.hypot(a.x - b.x, a.y - b.y), x: (a.x + b.x) / 2, y: (a.y + b.y) / 2};
        if (pinch?.distance > 0) { zoomTo(scale * current.distance / pinch.distance, current.x, current.y); offset.x += current.x - pinch.x; offset.y += current.y - pinch.y; drawZoom(); }
        pinch = current;
      } else if (scale > 1) { offset.x += e.clientX - previous.x; offset.y += e.clientY - previous.y; drawZoom(); }
    });
    function endPointer(e) { pointers.delete(e.pointerId); pinch = null; }
    stage.addEventListener('pointerup', endPointer); stage.addEventListener('pointercancel', endPointer);
    zoomDialog.addEventListener('keydown', e => {
      if (['+', '=', '-', '0'].includes(e.key)) { e.preventDefault(); if (e.key === '0') { offset = {x: 0, y: 0}; zoomTo(1); } else zoomTo(scale + (e.key === '-' ? -.5 : .5)); }
      const delta = {ArrowLeft: [40, 0], ArrowRight: [-40, 0], ArrowUp: [0, 40], ArrowDown: [0, -40]}[e.key];
      if (delta && scale > 1) { e.preventDefault(); offset.x += delta[0]; offset.y += delta[1]; drawZoom(); }
    });
    window.addEventListener('resize', () => { if (zoomDialog.open) drawZoom(); });
  }
  document.addEventListener('click', event => {
    if (!(event.target instanceof Element)) return;
    const favoriteButton = event.target.closest('[data-favorite]');
    if (favoriteButton) {
      const p = catalog.get(favoriteButton.dataset.favorite);
      if (!p) return;
      const saved = !favorites.has(p.id);
      if (saved) favorites.add(p.id); else favorites.delete(p.id);
      let persisted = true;
      try { window.localStorage.setItem(storageKey, JSON.stringify([...favorites])); } catch (e) { persisted = false; }
      updateFavorites();
      announce((saved ? p.name + ' guardada nos favoritos.' : p.name + ' removida dos favoritos.') + (persisted ? '' : ' O navegador só permite manter esta seleção durante a visita.'));
      if (favoritesGrid && !saved) document.getElementById('favorites-title').focus();
      return;
    }
    const shareButton = event.target.closest('[data-share]');
    if (shareButton) { const p = catalog.get(shareButton.dataset.share); if (p) shareProduct(p, shareButton); return; }
    const zoomLink = event.target.closest('[data-zoom]');
    if (zoomLink) { const p = allModels.get(zoomLink.dataset.zoom); if (p && zoomDialog) { event.preventDefault(); openZoom(p, zoomLink); } }
  });
  const quoteForm = document.getElementById('quote-form');
  if (quoteForm) {
    const steps = [...quoteForm.querySelectorAll('[data-quote-step]')];
    const fields = Object.fromEntries(['model', 'width', 'depth', 'height', 'help', 'finish', 'city', 'notes'].map(id => [id, document.getElementById('quote-' + id)]));
    const nextButton = quoteForm.querySelector('[data-quote-next]'), backButton = quoteForm.querySelector('[data-quote-back]');
    let step = 0;
    const query = new URLSearchParams(window.location.search).get('modelo');
    if (allModels.has(query) || query === 'projeto-personalizado') fields.model.value = query;
    function chosenName() { return allModels.get(fields.model.value)?.name || (fields.model.value === 'projeto-personalizado' ? 'Outro projeto por medida' : 'Projeto por medida — ideia por definir'); }
    function buildMessage() {
      const selected = allModels.get(fields.model.value), lines = ['Olá! Gostaria de pedir um orçamento à CINARÉ.', '', 'Peça / projeto: ' + chosenName()];
      if (selected) lines.push('Modelo: ' + selected.url);
      const labels = {width: 'largura', depth: 'profundidade', height: 'altura'};
      const dimensions = ['width', 'depth', 'height'].filter(key => fields[key].value.trim()).map(key => labels[key] + ' ' + fields[key].value.trim().replace('.', ',') + ' cm');
      lines.push(fields.help.checked ? 'Medidas: preciso de ajuda para as definir.' : dimensions.length ? 'Medidas aproximadas: ' + dimensions.join('; ') + '.' : 'Medidas: a definir.');
      lines.push('Acabamento pretendido: ' + (fields.finish.value.trim() || 'a definir') + '.');
      if (fields.city.value.trim()) lines.push('Localidade: ' + fields.city.value.trim());
      if (fields.notes.value.trim()) lines.push('Observações: ' + fields.notes.value.trim());
      return lines.join('\n');
    }
    function updateMessage() { const message = buildMessage(); document.getElementById('quote-message').value = message; document.getElementById('quote-whatsapp').href = wa(message); }
    function updateModel() {
      const p = allModels.get(fields.model.value), figure = document.querySelector('[data-quote-product]'), link = document.querySelector('[data-quote-model-link]');
      document.querySelector('[data-quote-model]').textContent = p ? p.name : 'Um projeto teu.';
      document.querySelector('[data-quote-model-description]').textContent = p ? p.description : 'Partilha a tua ideia. A solução, o preço e o prazo são definidos contigo no orçamento.';
      figure.hidden = !p;
      if (p) {
        const v = p.image.variants.find(v => v.width >= 640) || p.image.variants.at(-1), img = document.getElementById('quote-model-image');
        img.src = local(v.path); img.srcset = p.image.variants.map(v => local(v.path) + ' ' + v.width + 'w').join(', ');
        img.sizes = '(max-width:800px) 88vw, 380px'; img.width = p.image.width; img.height = p.image.height; img.alt = p.name + ' — visualização ilustrativa';
        link.href = catalog.has(p.id) ? local('modelos/' + p.id + '.html') : local('index.html#servicos'); link.textContent = 'Ver ' + p.name.toLowerCase();
      } else { link.href = local('mobiliario-industrial.html'); link.textContent = 'Explorar os modelos'; }
      document.getElementById('quote-direct').href = wa('Olá! Gostaria de pedir um orçamento para: ' + chosenName() + '.');
      updateMessage();
    }
    function validDimensions() {
      let first = null;
      ['width', 'depth', 'height'].forEach(key => {
        const input = fields[key], value = input.value.trim(), valid = fields.help.checked || !value || (/^\d+(?:[.,]\d+)?$/.test(value) && Number(value.replace(',', '.')) > 0);
        input.setAttribute('aria-invalid', String(!valid)); document.getElementById(key + '-error').hidden = valid;
        if (!valid && !first) first = input;
      });
      if (first) first.focus(); return !first;
    }
    function showStep(value, focus = true) {
      step = clamp(value, 0, 2); steps.forEach((panel, i) => { panel.hidden = i !== step; });
      quoteForm.querySelectorAll('[data-step-label]').forEach((label, i) => { label.classList.toggle('is-complete', i < step); if (i === step) label.setAttribute('aria-current', 'step'); else label.removeAttribute('aria-current'); });
      backButton.hidden = step === 0; nextButton.hidden = step === 2;
      quoteForm.querySelector('[data-step-status]').textContent = 'Passo ' + (step + 1) + ' de 3';
      if (focus) steps[step].querySelector('legend').focus(); updateMessage();
    }
    function nextStep() { if (step === 1 && !validDimensions()) return; showStep(step + 1); }
    nextButton.addEventListener('click', nextStep); backButton.addEventListener('click', () => showStep(step - 1));
    fields.model.addEventListener('change', updateModel);
    fields.help.addEventListener('change', () => { ['width', 'depth', 'height'].forEach(key => { fields[key].disabled = fields.help.checked; }); validDimensions(); updateMessage(); });
    quoteForm.addEventListener('input', updateMessage);
    quoteForm.addEventListener('submit', e => { e.preventDefault(); if (step < 2) nextStep(); });
    quoteForm.hidden = false; updateModel(); showStep(0, false);
  }
}());
