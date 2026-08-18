(async function () {
  const parts = [];
  for (let i = 0; i < 6; i++) {
    const response = await fetch(`./assets/mesa/${i}.txt?v=1`);
    if (!response.ok) throw new Error(`Erro ao carregar parte ${i}`);
    parts.push(await response.text());
  }
  const image = document.getElementById('hero-product');
  if (image) image.src = 'data:image/jpeg;base64,' + parts.join('');
})();
