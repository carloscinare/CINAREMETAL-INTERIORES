# CINARÉ Metal & Interiores

Site estático publicado por GitHub Pages a partir da branch `main`.

## Atualizar conteúdo

- Os nove modelos, descrições e relações estão em `produtos.json`.
- A página inicial usa o conteúdo de `templates/inicio.html`.
- `python scripts/prepare_images.py` prepara variantes WebP e imagens de partilha a partir dos originais aprovados (requer Pillow). Os originais são mantidos.
- `python scripts/build.py` gera as páginas, o catálogo do navegador e o sitemap. Publicar os ficheiros gerados juntamente com os dados, scripts e imagens.
- O comportamento está em `app.js`; a apresentação base em `site.css` e as funcionalidades novas em `features.css`.

## Funcionalidades

Cada modelo tem uma página estática com metadados de partilha e ligações para peças relacionadas. Os favoritos guardam apenas os identificadores dos modelos no `localStorage` deste navegador. A aplicação valida os identificadores antes de os apresentar.

O pedido guiado prepara uma mensagem para `+351 913 591 464`. As medidas são opcionais; preço, prazo e acabamentos finais são combinados no orçamento. O site não envia formulários para um servidor: o visitante revê a mensagem e continua no WhatsApp para confirmar o envio.

A ampliação usa a imagem original, suporta controlos de zoom, rato, arrasto, teclado e gestos com dois dedos. As imagens da coleção continuam identificadas como ilustrações.

As ligações antigas do catálogo com fragmentos, por exemplo `mobiliario-industrial.html#estante-industrial`, continuam a abrir a página do modelo.
